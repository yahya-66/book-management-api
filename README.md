📚 Book Management REST API

REST API untuk mengelola data buku dan pengguna menggunakan Flask dan PostgreSQL.

Project ini dibuat sebagai project pembelajaran dan portfolio untuk menerapkan konsep backend development, REST API, authentication, authorization, database, dan API testing.

🚀 Features

- User registration
- User login
- Password hashing
- JWT authentication
- Role-based authorization ("admin" / "user")
- CRUD buku
- Pagination
- Filtering berdasarkan judul dan penulis
- Sorting data buku
- Upload file gambar
- PostgreSQL database
- Swagger API documentation
- Environment variables menggunakan ".env"

🛠️ Tech Stack

- Python
- Flask
- Flask-SQLAlchemy
- PostgreSQL
- Flask-JWT-Extended
- Werkzeug
- Flasgger / Swagger
- python-dotenv
- Postman

📁 Project Structure

rest-api/
├── models/
│   ├── buku.py
│   └── user.py
├── routes/
├── services/
├── uploads/
├── app.py
├── database.py
├── requirements.txt
├── .env
├── .env.example
├── .gitignore
└── README.md

«⚠️ File ".env" dan folder "venv/" tidak boleh di-upload ke GitHub karena berisi konfigurasi lokal dan environment pribadi.»

⚙️ Installation

1. Clone Repository

git clone <URL_REPOSITORY>
cd rest-api

2. Create Virtual Environment

python3 -m venv venv
source venv/bin/activate

3. Install Dependencies

pip install -r requirements.txt

4. Configure Environment Variables

Buat file ".env" berdasarkan ".env.example".

DB_USER=
DB_PASSWORD=
DB_HOST=localhost
DB_PORT=5432
DB_NAME=

JWT_SECRET_KEY=

Isi konfigurasi tersebut sesuai dengan PostgreSQL lokal.

«⚠️ Jangan upload ".env" ke GitHub.»

5. Run Application

python app.py

API berjalan pada:

http://127.0.0.1:5000

🔐 Authentication

API menggunakan JWT (JSON Web Token) untuk authentication.

Register

POST /register

Contoh request:

{
    "username": "admin",
    "password": "password123"
}

Login

POST /login

Contoh request:

{
    "username": "admin",
    "password": "password123"
}

Login akan menghasilkan JWT token.

Gunakan token pada endpoint yang membutuhkan authentication:

Authorization: Bearer <JWT_TOKEN>

📚 Book Endpoints

Method| Endpoint| Authentication| Role
GET   | "/buku"     | JWT| User/Admin
GET   | "/buku/<id>"| JWT| User/Admin
POST  | "/buku"     | JWT| Admin
PUT   | "/buku/<id>"| JWT| Admin
DELETE| "/buku/<id>"| JWT| Admin

👤 User Endpoints

Method| Endpoint| Authentication| Role
POST| "/register"| Tidak| -
POST| "/login"   | Tidak| -
GET | "/users"   | JWT  | Admin
POST| "/upload"  | Tidak| -

🔎 Pagination, Filtering & Sorting

Endpoint "/buku" mendukung pagination, filtering, dan sorting.

Pagination

GET /buku?page=1&limit=5

Filtering berdasarkan judul

GET /buku?judul=python

Filtering berdasarkan penulis

GET /buku?penulis=andi

Sorting

GET /buku?sort=judul&order=asc

Parameter dapat dikombinasikan sesuai kebutuhan.

📖 API Documentation

Project menggunakan Swagger untuk dokumentasi API.

Swagger digunakan untuk melihat:

- Endpoint
- HTTP method
- Parameter
- Request
- Response
- Authentication

🗄️ Database

Project menggunakan PostgreSQL sebagai database.

Database

book_management

Tabel utama

users
buku

Flask-SQLAlchemy digunakan sebagai ORM untuk berinteraksi dengan database PostgreSQL.

🧪 API Testing

Endpoint API telah diuji menggunakan Postman, termasuk:

- Register
- Login
- JWT authentication
- User management
- CRUD buku
- Pagination
- Filtering
- Sorting
- Upload file
- Authorization berdasarkan role
- Error handling

🔒 Security

Informasi sensitif seperti:

- Database password
- JWT secret
- Environment configuration

disimpan menggunakan ".env" dan tidak dimasukkan ke repository GitHub.

File ".env" juga dimasukkan ke ".gitignore".

File ".env.example" digunakan sebagai template konfigurasi tanpa menyimpan informasi sensitif.

🎯 Project Goals

Project ini dibuat untuk mempraktikkan:

- REST API development
- Backend programming dengan Python
- Database management
- PostgreSQL
- Authentication & authorization
- JWT
- API testing
- Environment variables
- Version control dengan Git
- Project deployment

👨‍💻 Author

Yahya Nizar

Backend development project untuk pembelajaran dan portfolio.