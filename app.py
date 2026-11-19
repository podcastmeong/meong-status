# Papan Status Agent — Podcast Meong (demo Streamlit)
#
# Menampilkan isi bus koordinasi Pusat Komando (data/koordinasi.json):
# total pesan, inbox per agent, pesan terbaru, dan aturan rute R1–R10.
# READ-ONLY: aplikasi ini tidak menulis apa pun ke bus.
#
# Sumber data (urutan):
#   1. File koordinasi.json di folder yang sama (salinan/snapshot).
#   2. Env KOORDINASI_JSON_URL — URL mentah file koordinasi.json
#      (mis. raw.githubusercontent.com/...) bila deploy di Streamlit Cloud.
#   3. Bila tidak ada keduanya: data contoh kecil bawaan.
#
# Jalankan lokal:
#   streamlit run app.py --server.port 8501
# Deploy: lihat README-streamlit.md (butuh akun Streamlit + repo GitHub
# milik Cipta — tidak dibuat di sini).
import json
import os
from pathlib import Path

import streamlit as st

NAMA_AGENT = {1: "1 · Asisten", 2: "2 · Penjualan", 3: "3 · Pertumbuhan",
              5: "5 · Produksi Produk", 6: "6 · Lomba", 7: "7 · Keuangan",
              8: "8 · Terjemah Inggris", 9: "9 · Game & Aplikasi",
              10: "10 · Riset Produk", 11: "11 · Oyen", 12: "12 · Momo",
              13: "13 · Email", "Muse": "Muse (Komandan)",
              "Sistem": "Sistem (Siklus Harian)"}
AGEN_KUNCI = [1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 12, 13, "Muse"]

ATURAN_RUTE = [
    ("R1", "Brief layak → Produksi", "10 → 5", "product-brief"),
    ("R2", "Draf baru → Penjualan + Terjemah", "5 → 2, 8", "draft-approval"),
    ("R3", "Tenggat lomba ≤7 hari → Produksi", "6 → 5", "contest-entry"),
    ("R4", "Payout jatuh tempo → Muse", "7 → Muse", "finance-entry"),
    ("R5", "Email penting → agent terkait", "13 → terkait", "pemberitahuan"),
    ("R6", "Verdict PERLU PERBAIKAN → Produksi", "11/12 → 5",
     "permintaan-perbaikan"),
    ("R7", "Game selesai → Penjualan + Keuangan", "9 → 2, 7", "pemberitahuan"),
    ("R8", "Terjemahan selesai → Penjualan", "8 → 2", "translation-job"),
    ("R9", "Ringkasan siklus → Muse", "Sistem → Muse", "laporan-harian"),
    ("R10", "Pesan mendesak → eskalasi ke Muse", "Sistem → Muse", "eskalasi"),
]

CONTOH = {"pesan": [
    {"id": "KB-000", "tanggal": "2026-11-19", "waktu": "00:00",
     "dari_agent": "Sistem", "ke_agent": "Muse", "jenis": "laporan-harian",
     "prioritas": "normal", "ringkasan": "Data contoh — salin "
     "koordinasi.json asli ke folder ini untuk data nyata.",
     "isi": {}, "status": "baru", "sumber": "contoh", "kunci": ""}],
    "log": [], "meta": {"siklus_terakhir": "-"}}


@st.cache_data(ttl=60)
def muat_data():
    lokal = Path(__file__).resolve().parent / "koordinasi.json"
    if lokal.exists():
        try:
            return json.loads(lokal.read_text(encoding="utf-8")), "snapshot lokal"
        except (OSError, ValueError):
            pass
    url = os.environ.get("KOORDINASI_JSON_URL", "")
    if url:
        try:
            import urllib.request
            with urllib.request.urlopen(url, timeout=10) as r:
                return json.loads(r.read().decode("utf-8")), "URL: " + url
        except Exception as exc:  # noqa: BLE001
            st.warning("Gagal memuat dari URL: {}".format(exc))
    return CONTOH, "data contoh (bukan data nyata)"


def nama(a):
    return NAMA_AGENT.get(a, str(a))


data, sumber = muat_data()
pesan = data.get("pesan", [])
meta = data.get("meta", {})

st.set_page_config(page_title="Papan Status Agent — Podcast Meong",
                   layout="wide")
st.title("🐱 Papan Status Agent — Podcast Meong")
st.caption("Bus koordinasi Pusat Komando (read-only). Sumber data: {}"
           .format(sumber))

kol1, kol2, kol3 = st.columns(3)
kol1.metric("Total pesan", len(pesan))
kol2.metric("Pesan baru", sum(1 for p in pesan if p.get("status") == "baru"))
kol3.metric("Selesai", sum(1 for p in pesan if p.get("status") == "selesai"))
st.caption("Siklus Harian terakhir: {}".format(
    meta.get("siklus_terakhir", "belum pernah dijalankan")))

st.subheader("📥 Inbox per agent")
baris = []
for agen in AGEN_KUNCI:
    masuk = [p for p in pesan if str(p.get("ke_agent")) == str(agen)]
    baris.append({
        "Agent": nama(agen),
        "Total": len(masuk),
        "Baru": sum(1 for p in masuk if p.get("status") == "baru"),
        "Dikerjakan": sum(1 for p in masuk
                           if p.get("status") == "dikerjakan"),
        "Selesai": sum(1 for p in masuk if p.get("status") == "selesai"),
        "Ditolak": sum(1 for p in masuk if p.get("status") == "ditolak"),
    })
st.dataframe(baris, width="stretch", hide_index=True)

st.subheader("💬 Pesan terbaru")
if pesan:
    tabel = [{"ID": p.get("id"), "Tanggal": p.get("tanggal"),
              "Dari": nama(p.get("dari_agent")),
              "Ke": nama(p.get("ke_agent")), "Jenis": p.get("jenis"),
              "Prioritas": p.get("prioritas"), "Status": p.get("status"),
              "Ringkasan": p.get("ringkasan")}
             for p in sorted(pesan, key=lambda x: x.get("id", ""),
                             reverse=True)[:20]]
    st.dataframe(tabel, width="stretch", hide_index=True)
else:
    st.info("Belum ada pesan di bus — tulisannya di sini: "
            "jalankan Siklus Harian di Pusat Komando.")

st.subheader("🔀 Aturan rute (R1–R10)")
st.dataframe([{"Aturan": r[0], "Nama": r[1], "Rute": r[2], "Jenis": r[3]}
              for r in ATURAN_RUTE], width="stretch",
             hide_index=True)
st.caption("Pesan di bus adalah pengingat/DRAF — bukan perintah otomatis. "
           "Keputusan akhir tetap di tangan Cipta.")
