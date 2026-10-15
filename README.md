# Book Management REST API

REST API untuk manajemen buku, dibangun dengan Flask dan PostgreSQL. Dilengkapi autentikasi JWT, rate limiting, migrasi database, Docker, dan CI/CD otomatis.

[

![CI](https://github.com/yahya-66/book-management-api/actions/workflows/ci.yml/badge.svg)

](https://github.com/yahya-66/book-management-api/actions/workflows/ci.yml)

**Live API:** https://melodious-contentment-production-f0d6.up.railway.app

> Server ini berjalan di trial Railway sehingga bisa nonaktif sewaktu-waktu. Semua endpoint memakai prefix `/api`.

## Alur CI/CD

```
GitHub → GitHub Actions (pytest) → Docker → Railway → PostgreSQL
```

1. Setiap `git push` ke `main` menjalankan GitHub Actions (pytest dengan Python 3.12 dan PostgreSQL 16).
2. Railway membangun image dari `Dockerfile` dan men-deploy otomatis.
3. Variabel rahasia diisi lewat dashboard Railway, bukan dari repo.

## Teknologi

- Flask, SQLAlchemy, Flask-Migrate (Alembic)
- Flask-JWT-Extended (autentikasi), Flask-Limiter (rate limiting)
- Flasgger / Swagger (dokumentasi), python-dotenv
- PostgreSQL, Gunicorn
- Docker, Docker Compose
- GitHub Actions, Railway
- Pytest, Postman

## Struktur Project

```
rest-api/
├── .github/workflows/ci.yml   # pipeline CI
├── migrations/                # migrasi Alembic
├── repositories/              # akses data
├── routes/                    # endpoint (blueprint)
├── services/                  # logika bisnis
├── tests/                     # pytest
├── utils/                     # exceptions & response standar
├── app.py                     # entry point
├── database.py                # model (User, Buku)
├── extensions.py              # limiter
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── README.md
```

## Menjalankan Lokal dengan Docker

1. Clone repository:
```bash
git clone https://github.com/yahya-66/book-management-api.git
cd book-management-api
```

2. Salin file environment, lalu isi nilainya:
```bash
cp .env.example .env
```

3. Jalankan API dan PostgreSQL:
```bash
docker compose up --build
```

4. API tersedia di `http://localhost:5000`.

Menghentikan: `docker compose down` (data tetap tersimpan di volume). Untuk menghapus data juga: `docker compose down -v`.

## Variabel Lingkungan

| Variabel | Keterangan |
|---|---|
| `DB_USER` | Username PostgreSQL |
| `DB_PASSWORD` | Password PostgreSQL |
| `DB_HOST` | Host database (`db` di Docker Compose) |
| `DB_PORT` | Port database (5432) |
| `DB_NAME` | Nama database |
| `JWT_SECRET_KEY` | Kunci rahasia penanda token JWT |

> File `.env`, `.env.production`, dan folder `venv/` tidak boleh di-commit.

## Endpoint

Semua path diawali `/api`.

| Method | Path | Keterangan | Token |
|---|---|---|---|
| POST | `/api/register` | Daftar user baru | Tidak |
| POST | `/api/login` | Login, mendapat token JWT | Tidak |
| POST | `/api/refresh` | Perbarui token | Ya |
| POST | `/api/upload` | Upload file | Ya |
| GET | `/api/users` | Daftar user | Ya |
| GET | `/api/buku` | Daftar buku (pagination) | Ya |
| POST | `/api/buku` | Tambah buku | Ya |

Token dikirim lewat header: `Authorization: Bearer <token>`.

## Contoh Penggunaan

Register:
```bash
curl -X POST http://localhost:5000/api/register \
  -H "Content-Type: application/json" \
  -d '{"username":"user1","password":"password-anda"}'
```

Login:
```bash
curl -X POST http://localhost:5000/api/login \
  -H "Content-Type: application/json" \
  -d '{"username":"user1","password":"password-anda"}'
```

Ambil daftar buku:
```bash
curl http://localhost:5000/api/buku \
  -H "Authorization: Bearer <access_token>"
```

Untuk server online, ganti `http://localhost:5000` dengan alamat Live API di atas.

## Testing

```bash
pip install -r requirements.txt
pytest
```

Tes juga berjalan otomatis di GitHub Actions pada setiap push dan pull request.

## Deployment

- **Platform:** Railway (service API + PostgreSQL terkelola).
- **Build:** dari `Dockerfile` di repo.
- **Start:** saat container hidup, tabel dibuat bila belum ada, lalu Gunicorn berjalan di port yang diberikan Railway (`PORT`).
- **Auto-deploy:** setiap push ke `main`.

## Catatan Pengembangan

- Rate limiting memakai penyimpanan memori; untuk production sebaiknya dipindah ke Redis.
- Cakupan test masih dasar dan bisa ditambah (login, tambah dan hapus buku).