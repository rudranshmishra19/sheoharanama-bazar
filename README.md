# RealNorth 🛒

**Production-ready Django e-commerce backend** built with PostgreSQL, DRF REST APIs, JWT authentication, and clean architecture. Deployed and live.

[![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-092E20?style=flat&logo=django&logoColor=white)](https://djangoproject.com/)
[![DRF](https://img.shields.io/badge/DjangoREST-404040?style=flat&logoColor=white)](https://djangorestframework.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=flat&logo=postgresql&logoColor=white)](https://postgresql.org/)
[![Render](https://img.shields.io/badge/Deployed%20on-Render-46E3B7?style=flat&logo=render&logoColor=white)](https://render.com/)

## 🚀 Live Demo

🔗 [https://sheoharanama-bazar.onrender.com/](https://sheoharanama-bazar.onrender.com/)

---

## ✨ Features

- **JWT Authentication** — Register, login, token refresh, password reset
- **Product Catalog** — Browse products with categories, filtering, and search
- **Shopping Cart** — Add/remove items, update quantities
- **Order Management** — Place orders, track status, view order history
- **Admin Dashboard** — Manage products, users, and orders
- **Responsive Design** — Works on desktop, tablet, and mobile

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.x |
| Backend | Django, Django REST Framework |
| Database | PostgreSQL |
| Authentication | JWT (SimpleJWT) |
| Static Files | WhiteNoise |
| Deployment | Render |
| Frontend | HTML, CSS, JavaScript |

---

## 📸 Screenshots

| Home Page | Product Detail | Shopping Cart |
|-----------|---------------|---------------|
| ![Home](screenshots/home.png) | ![Product](screenshots/product.png) | ![Cart](screenshots/cart.png) |

---

## 📁 Project Structure

```
RealNorth/
├── store/              # Main app (models, views, serializers, urls)
│   ├── api/            # DRF API views and serializers
│   ├── models.py       # Database models
│   └── tests.py        # Unit tests
├── mysite/             # Project settings and root urls
├── static/             # CSS, JS, Images
├── media/              # User uploaded files
├── requirements.txt
└── manage.py
```

---

## ⚙️ Quick Start

### 1. Clone & Setup

```bash
git clone https://github.com/rudranshmishra19/RealNorth.git
cd RealNorth

# Create virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Variables

```bash
cp .env.example .env
```

Fill in your `.env` file:

```env
SECRET_KEY=your_django_secret_key
DEBUG=True
DATABASE_URL=postgres://store_user:your_password@localhost:5432/store_db
ALLOWED_HOSTS=localhost,127.0.0.1
```

### 3. Database Setup (PostgreSQL)

```bash
# Open PostgreSQL console
psql -U postgres

# Run these commands
CREATE DATABASE store_db;
CREATE USER store_user WITH PASSWORD 'your_password';
ALTER ROLE store_user SET client_encoding TO 'utf8';
ALTER ROLE store_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE store_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE store_db TO store_user;
\q
```

### 4. Run the App

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Visit `http://127.0.0.1:8000/`

---

## 📡 API Endpoints

### Auth
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/register/` | Register new user |
| POST | `/auth/token/` | Login and get JWT token |
| POST | `/auth/token/refresh/` | Refresh JWT token |

### Products
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/products/` | List all products |
| GET | `/api/products/<id>/` | Get single product |
| GET | `/api/products/?search=name` | Search products |

### Cart
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/carts/` | Get user cart |
| POST | `/api/cart-items/` | Add item to cart |
| PUT | `/api/cart-items/<id>/` | Update cart item |
| DELETE | `/api/cart-items/<id>/` | Remove cart item |

### Orders
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/orders/` | List user orders |
| POST | `/api/orders/` | Place new order |
| GET | `/api/orders/<id>/` | Get order details |
| POST | `/api/orders/<id>/cancel/` | Cancel an order |

---

## 👤 Author

**Rudransh Mishra**
- LinkedIn: [rudransh-mishra](https://www.linkedin.com/in/rudransh-mishra-8b39a3265)
- GitHub: [rudranshmishra19](https://github.com/rudranshmishra19)

---

## 📄 License

MIT License
