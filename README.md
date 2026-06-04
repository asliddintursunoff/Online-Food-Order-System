# 🍔 Online Food Order System

A RESTful backend API for an online food ordering platform, built with **Django 6** and **Django REST Framework**. It exposes a clean, documented API for managing food items, orders, and related resources.

---

## 🚀 Features

- RESTful API built with Django REST Framework
- Auto-generated interactive API documentation via **drf-spectacular** (Swagger / Redoc)
- Image upload support via **Pillow**
- Flexible query filtering with **django-filter**
- Modular Django app structure under `apps/`
- Settings managed from `config/settings.py`

---

## 🛠️ Tech Stack

| Layer        | Technology                        |
|--------------|-----------------------------------|
| Language     | Python 3.x                        |
| Framework    | Django 6.0.5                      |
| REST API     | Django REST Framework 3.17.1      |
| API Docs     | drf-spectacular 0.29.0 (OpenAPI)  |
| Filtering    | django-filter 25.2                |
| Image Support| Pillow 12.2.0                     |
| Database     | SQLite (default)                  |

---

## 📁 Project Structure

```
Online-Food-Order-System/
├── apps/               # Django applications (food items, orders, users, etc.)
├── config/
│   └── settings.py     # Project settings
├── manage.py           # Django management CLI
├── requirements.txt    # Python dependencies
└── .gitignore
```

---

## ⚙️ Getting Started

### Prerequisites

- Python 3.10+
- pip

### 1. Clone the repository

```bash
git clone https://github.com/asliddintursunoff/Online-Food-Order-System.git
cd Online-Food-Order-System
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv

# macOS / Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply migrations

```bash
python manage.py migrate
```

### 5. (Optional) Create a superuser

```bash
python manage.py createsuperuser
```

### 6. Run the development server

```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`

---

## 📖 API Documentation

Once the server is running, interactive API docs are available at:

| Format  | URL                                |
|---------|------------------------------------|
| Swagger | `http://127.0.0.1:8000/api/schema/swagger-ui/` |
| Redoc   | `http://127.0.0.1:8000/api/schema/redoc/`      |
| Schema  | `http://127.0.0.1:8000/api/schema/`            |

> Exact URL paths may vary depending on the URL configuration in `config/urls.py`.

---

## 📦 Dependencies

```
asgiref==3.11.1
Django==6.0.5
django-filter==25.2
djangorestframework==3.17.1
drf-spectacular==0.29.0
pillow==12.2.0
PyYAML==6.0.3
sqlparse==0.5.5
```

Install all at once with `pip install -r requirements.txt`.

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Commit your changes: `git commit -m "Add some feature"`
4. Push to the branch: `git push origin feature/your-feature-name`
5. Open a Pull Request

---

## 📄 License

This project is open source. Add a license file (e.g. MIT) to clarify usage terms.

---

## 👤 Author

**Asliddintursunoff**
- GitHub: [@asliddintursunoff](https://github.com/asliddintursunoff)
