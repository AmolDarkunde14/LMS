# Library Management System (Backend)

REST API for a Library Management System built with Django Rest Framework (DRF) and PostgreSQL. Features role-based access control, book inventory management, member borrowing transactions, and automated fine calculation.

## Tech Stack
- **Backend:** Python + Django + Django REST Framework
- **Database:** PostgreSQL
- **Authentication:** JWT (via djangorestframework-simplejwt)
- **Containerization:** Docker & Docker Compose (optional)
- **API Documentation:** OpenAPI / Swagger UI (via drf-spectacular)

## Main Features
- **User Management & Auth**: Register users, Login via JWT, 3 Roles: `ADMIN`, `LIBRARIAN`, `MEMBER`.
- **Books API**: Add, update, delete, view, search books (Admin/Librarian managed).
- **Transactions API**: Issue books, Return books, Calculate late fines, View history.

---

## 🚀 Setup Instructions (Local without Docker)

**1. Create a virtual environment and install dependencies**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**2. Setup Environment Variables**
Copy the example file and update `.env` with your PostgreSQL credentials:
```bash
cp .env.example .env
```

**3. Setup Database**
Ensure PostgreSQL is running and you have a database matching the `DB_NAME` in `.env` (default is `lms_db` with user `postgres` and pass `admin`).

**4. Run Migrations & Seed Data**
```bash
python manage.py makemigrations users books transactions
python manage.py migrate
# Seed the database with sample books, admin, librarian, and members
python manage.py seed_data 
```

**5. Start Development Server**
```bash
python manage.py runserver
```
Visit http://127.0.0.1:8000/api/schema/swagger-ui/ for interactive API documentation.

---

## 🐳 Setup Instructions (With Docker)
Just run:
```bash
docker-compose up --build
```
This maps PostgreSQL on `5432` and Django on `8000`. It automatically creates migrations, applies them, and runs the seed script!

---

## 👤 Default Users (from seed_data):
- **Admin**: `admin` / `adminpass`
- **Librarian**: `librarian` / `libpass`
- **Member**: `member1` / `pass123`

---

## 📝 Sample API Requests (Postman / cURL)

### 1. Register Member (Public)
**POST** `/api/users/register/`
```json
{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "strongpassword123",
  "first_name": "John",
  "last_name": "Doe"
}
```

### 2. Login (Get JWT Token)
**POST** `/api/users/login/`
```json
{
  "username": "admin",
  "password": "adminpass"
}
```
*Response returns `access` and `refresh` tokens.* Use `access` token as Bearer Token in subsequent requests.

### 3. List Books (Authenticated)
**GET** `/api/books/`
*Headers: `Authorization: Bearer <your-token>`*

### 4. Search & Filter Books
**GET** `/api/books/?search=Clean+Code&category=Technology`

### 5. Issue a Book (Admin / Librarian)
**POST** `/api/transactions/issue/`
```json
{
  "book_id": 1,
  "member_id": 1
}
```

### 6. View My History (Member)
**GET** `/api/transactions/history/`

### 7. Return a Book (Admin / Librarian)
**POST** `/api/transactions/return/`
```json
{
  "transaction_id": 1
}
```
