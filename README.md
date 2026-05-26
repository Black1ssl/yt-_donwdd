# YouTube Downloader

Aplikasi web sederhana untuk download video YouTube menggunakan Flask dan yt-dlp.

## Fitur

- Download video YouTube dalam format MP4 terbaik
- API sederhana berbasis HTTP
- Deploy mudah ke Render

## Persyaratan

- Python 3.8+
- Flask
- yt-dlp
- gunicorn

## Instalasi Lokal

1. Clone repository:
```bash
git clone https://github.com/Black1ssl/yt-_donwdd.git
cd yt-_donwdd
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Jalankan aplikasi:
```bash
python app.py
```

Aplikasi akan berjalan di `http://localhost:5000`

## Penggunaan

### Contoh Request

```
GET http://localhost:5000/download?url=https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

Ganti URL dengan link video YouTube yang ingin didownload.

### Endpoints

- `GET /` - Informasi API
- `GET /download?url=YOUR_YOUTUBE_URL` - Download video
- `GET /health` - Health check

## Deployment ke Render

1. Push kode ke GitHub
2. Buka [Render Dashboard](https://dashboard.render.com/)
3. Klik **New +** → **Web Service**
4. Pilih repository ini
5. Isi konfigurasi:
   - **Name**: `yt-downloader-kamu`
   - **Region**: Singapore (atau terdekat)
   - **Branch**: main
   - **Language**: Python
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
6. Klik **Deploy Web Service**

Setelah deploy berhasil, URL aplikasi akan muncul di dashboard Render.

## Catatan

- Menggunakan akun free Render, server akan "tidur" setelah 15 menit tidak diakses
- Video akan di-cache di folder `downloads/`
- Disarankan menggunakan instance berbayar untuk production

## Lisensi

MIT
