# 📰 Django Blog App

A modern, lightweight blog built with **Django**.  
Features a clean, responsive UI with **minimal animations** (subtle hover fades, soft card lifts, and smooth link transitions) to improve polish without distracting users.

---

[![Django](https://img.shields.io/badge/Django-5.x-green)](https://www.djangoproject.com/) [![Python](https://img.shields.io/badge/Python-3.10-blue)](https://www.python.org/) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

---

## ✨ Highlights

- Minimal, modern UI with small, tasteful animations:
  - Card elevation on hover (soft shadow + transform)
  - Subtle link color transitions
  - Smooth pagination / button hover effects
- Core blog features: create, read, update, delete (CRUD)
- User authentication & profiles (profile pictures)
- Responsive layout: two-column desktop, single-column mobile
- Clean templates ready to customize (Tailwind friendly)

---

## 🧭 Features

- ✅ User registration, login, logout, password reset (SMTP)
- ✅ Post creation, editing, deletion
- ✅ Author profiles with avatar
- ✅ Pagination and search-ready structure
- ✅ Accessible, responsive HTML templates
- ✅ Minimal CSS animations that improve UX (not flashy)

---

## 🏗 Tech Stack

- **Backend:** Django (Python)  
- **Frontend:** Tailwind CSS (suggested) or Bootstrap with small custom CSS for animations  
- **Database:** SQLite (default) — easy to switch to PostgreSQL  
- **Email:** SMTP (Gmail or Mailtrap for development)  
- **VCS:** Git & GitHub

---

## ⚙️ Local Setup

1. **Clone**
```bash
git clone https://github.com/Stephendelali/django-blog-app.git
cd django-blog-app
Create & activate virtual environment
deactivate
```
2. Create & activate virtual environment

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
```

3.Install dependencies
```bash
pip install -r requirements.txt

```

Environment variables
Create a .env at project root:
```bash
EMAIL_USER=your_email@gmail.com
EMAIL_PASS=your_app_password
DEBUG=True
SECRET_KEY=your_django_secret_key
```
Migrate & run
```bash
python manage.py migrate
python manage.py createsuperuser   # optional
python manage.py runserver
```

Open: http://127.0.0.1:8000/
