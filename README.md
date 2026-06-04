# 🍔 Online Food Order System - Multi-Tenant

A modern **multi-tenant** RESTful API for online food ordering built with **Django 6** and **Django REST Framework**. Each restaurant operates in its own database schema, ensuring complete data isolation and scalability.

---

## 🌟 Key Features

- **Multi-Tenant Architecture** using `django-tenants` + PostgreSQL schemas
- Each restaurant gets its own isolated schema (data, users, products, orders)
- Public schema for restaurant registration
- Location-based delivery estimation using **PostGIS**
- JWT Authentication with role-based access (Client, Waiter, Deliverer, Admin)
- Complete CRUD for products, categories, orders, and user locations
- Image upload support for food items
- Interactive API documentation (Swagger + ReDoc)
- Advanced filtering and search

---

## 🏗️ Multi-Tenant Architecture

This project implements **schema-based multi-tenancy**:

- **Public Schema**: Used for restaurant registration (`/api/restaurants/register/`)
- **Tenant Schemas**: Each restaurant gets its own schema (e.g., `kfc`, `burger-king`)
- **Tenant Model**: `Restaurant` (inherits from `TenantMixin`)
- **Domain Model**: `RestaurantDomain` for subdomain routing (`kfc.localhost`)

**Benefits:**
- Complete data isolation between restaurants
- Independent users, products, and orders per restaurant
- Scalable and secure

---

## 🛠️ Tech Stack

| Layer              | Technology                                      |
|--------------------|-------------------------------------------------|
| Framework          | Django 6.0.5                                    |
| REST API           | Django REST Framework 3.17.1                    |
| Multi-Tenancy      | django-tenants                                  |
| Database           | PostgreSQL + PostGIS                            |
| Authentication     | SimpleJWT                                       |
| API Docs           | drf-spectacular (Swagger / ReDoc)               |
| Filtering          | django-filter                                   |
| GIS / Locations    | Django GIS + PostGIS                            |
| Image Handling     | Pillow                                          |

---

## 📁 Project Structure

```bash
food_delivery/
├── config/                     # Project settings & URLs
│   ├── settings.py
│   ├── tenant_urls.py
│   └── public_urls.py
├── apps/
│   ├── restaurants/            # Multi-tenancy logic
│   ├── users/                  # Users + Locations
│   ├── products/               # Categories & Menu
│   └── orders/                 # Orders & Status Management
├── manage.py
├── requirements.txt
└── media/                      # Uploaded product images