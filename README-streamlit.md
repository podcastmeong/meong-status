# Papan Status Agent — Demo Streamlit (Siap Deploy)

Aplikasi Streamlit kecil (read-only) yang menampilkan isi bus koordinasi
Pusat Komando: total pesan, inbox per agent, pesan terbaru, aturan rute
R1–R10. Tidak menulis apa pun ke bus.

## Isi folder

| File | Keterangan |
|------|-----------|
| `app.py` | Aplikasi Streamlit |
| `requirements.txt` | `streamlit` |
| `koordinasi.json` | Snapshot data bus per 19 Nov 2026 (contoh; ganti dengan salinan terbaru sebelum deploy) |

## Coba lokal

```bash
pip install -r requirements.txt
streamlit run app.py --server.port 8501
# buka http://localhost:8501
```

## Deploy ke Streamlit Community Cloud (gratis)

Butuh (dari Cipta — TIDAK dibuat di sini):
1. Akun Streamlit Community Cloud (login dengan GitHub).
2. Repo GitHub publik berisi folder ini (mis. repo `podcastmeong/meong-status`).

Langkah:
1. Buat repo GitHub baru, unggah `app.py`, `requirements.txt`, dan
   `koordinasi.json` terbaru (salin dari `pusat-komando/data/`).
2. Di https://share.streamlit.io → New app → pilih repo + branch + `app.py` → Deploy.
3. Aplikasi hidup di `https://<nama-app>.streamlit.app`.

Memperbarui data: salin ulang `koordinasi.json` terbaru ke repo lalu
push — Streamlit me-redeploy otomatis. Alternatif tanpa unggah file:
set secret/env `KOORDINASI_JSON_URL` ke URL mentah file koordinasi.json
di GitHub (`raw.githubusercontent.com/.../koordinasi.json`) — aplikasi
membaca dari URL itu (cache 60 detik).

## Batasan

- **Data bersifat publik** bila aplikasinya publik: siapa pun yang punya
  tautan bisa membaca isi bus. Jangan taruh data sensitif di
  `koordinasi.json` (saat ini isinya hanya ringkasan kerja agent — aman).
- Streamlit Community Cloud: 1 GB resource, aplikasi tidur bila lama
  tidak dibuka (bangun lagi saat dibuka).
- Aplikasi ini hanya menampilkan — untuk menjalankan Siklus Harian atau
  mengirim pesan tetap lewat Pusat Komando / MCP Server.
- Uji lokal (19 Nov 2026): lihat `LAPORAN-ALTERNATIF-GRATIS.md`.
