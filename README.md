# 🗞️ Voxa — Modern Django Blogging Platform

Voxa is a **modern, production-ready blogging platform** built with **Django 5** and designed with a strong focus on **clean UI, performance, and user experience**.

It combines a minimal, premium interface with robust backend features such as authentication, social login, media handling, and deployment-ready configuration.

---

## 🚀 Live Demo

👉 **https://django-blog-app-tlzg.onrender.com/**  
*(Custom domain coming soon)*

---

## 🛠️ Tech Stack

### Backend
- **Django 5.x**
- **Python 3.10+**
- Django Allauth (authentication & social login)
- Django REST Framework (API-ready)

### Frontend
- **Tailwind CSS**
- Custom CSS variables & subtle animations
- Modular JavaScript (ES modules)
- Geist font for clean typography

### Infrastructure
- **PostgreSQL** (Supabase-compatible)
- **Cloudinary** (media storage)
- **WhiteNoise** (static files)
- **Render** (deployment)

---

## ✨ Key Features

### 🧑‍💻 Authentication & Accounts
- Email/password authentication
- Google OAuth 2.0 login
- Secure sessions & CSRF protection
- Modal-based login & registration UX
- Redirect-back logic after authentication

### 📝 Blogging
- Full CRUD for blog posts
- Author profiles with avatars
- Responsive layouts (desktop & mobile)
- Clean, readable typography

### 🎨 UI / UX
- Premium, minimal interface
- Subtle animations (hover, scale, fades)
- Consistent design system using CSS variables (`--voxa-*`)
- Branded navigation & favicon
- Accessibility-friendly markup

### ⚡ Performance & Production
- Template caching
- GZip compression
- Secure cookies in production
- Environment-based settings
- Cloud-ready configuration

---

## 📸 Screenshots
<img width="1922" height="3306" alt="screencapture-django-blog-app-tlzg-onrender-2025-12-20-19_36_01" src="https://github.com/user-attachments/assets/29d12236-90e2-4a90-9401-6a1c1aaa1e4a" />

<img width="1922" height="3130" alt="screencapture-django-blog-app-tlzg-onrender-post-3-2025-12-20-19_33_41" src="https://github.com/user-attachments/assets/27c8046c-2ef9-4560-acad-c8761c6954ac" />

<img width="1922" height="1255" alt="screencapture-django-blog-app-tlzg-onrender-accounts-google-login-2025-12-20-19_37_52" src="https://github.com/user-attachments/assets/f2b5a349-cb1d-44a9-b850-61abafd23d99" />


## ⚙️ Local Development Setup

### 1️⃣ Clone the repository
```bash
git clone https://github.com/Stephendelali/django-blog-app.git
cd django-blog-app
````

### 2️⃣ Create & activate a virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate

````

### 3️⃣ Install dependencies
````bash
pip install -r requirements.txt
````

## 🔐 Environment Variables

### Create a .env file at the project root:
````bash
DEBUG=True
SECRET_KEY=your_django_secret_key

# Email (SMTP)
EMAIL_USER=your_email@gmail.com
EMAIL_PASS=your_email_app_password

# Database
DB_NAME=postgres
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_PORT=6543

# Google OAuth
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_SECRET=your_google_client_secret

# Cloudinary
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
````

## 🗄️ Database & Migrations
````bash
python manage.py migrate
````

## ▶️ Run the development server
````bash
python manage.py runserver
````

# Voxa Project

Open your browser at:  
👉 [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## 🔒 Security Notes

- Secure cookies enabled in production  
- CSRF & session protection configured  
- OAuth redirect URIs must be updated when changing domains  
- Environment variables are required for deployment  

---

## 📦 Deployment

The project is deployment-ready for platforms like:

- Render  
- Vercel (frontend)  
- Railway  
- Fly.io  

Static files are handled via **WhiteNoise**, and media uploads via **Cloudinary**.

---

## 🧭 Roadmap

- Custom domain (`voxa.*`)  
- Post reactions & comments  
- User follow system  
- API-first expansion  
- PWA support  

---

## 📄 License

This project is licensed under the **MIT License**.  
Feel free to fork, modify, and build upon it.

---

## 🙌 Author

**Stephen Delali**  
GitHub: [@Stephendelali](https://github.com/Stephendelali)

