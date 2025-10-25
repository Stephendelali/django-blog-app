# 📝 Django Blog App

A modern, fully functional blogging web application built with **Django**.  
This app allows users to create, edit, and delete blog posts, manage profiles, and interact through a clean and intuitive interface.

---

## 🚀 Features

- 🧑‍💻 **User Authentication** — Registration, Login, Logout, Password Reset via Email  
- 📰 **Post Management** — Create, Read, Update, and Delete (CRUD) blog posts  
- 👤 **User Profiles** — Upload profile pictures and manage user details  
- 🕓 **Pagination** — Smooth navigation through posts  
- 💬 **Dynamic Content** — Each post displays the author, date, and content beautifully  
- ⚙️ **Responsive Design** — Works seamlessly across all devices  
- 🔒 **Secure Email Setup** — Password reset and notifications using SMTP configuration  

---

## 🏗️ Tech Stack

| Layer | Technology |
|-------|-------------|
| **Backend** | Django 5.x (Python 3.10+) |
| **Frontend** | HTML5, CSS3, Bootstrap 4 |
| **Database** | SQLite (default), easy to switch to PostgreSQL/MySQL |
| **Email Service** | Gmail SMTP |
| **Version Control** | Git & GitHub |

---

## 💡 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/Stephendelali/django-blog-app.git
cd django-blog-app
2. Set Up a Virtual Environment
bash
Copy code
python -m venv venv
venv\Scripts\activate     # For Windows
# OR
source venv/bin/activate  # For Mac/Linux
3. Install Dependencies
bash
Copy code
pip install -r requirements.txt
4. Configure Environment Variables
Create a .env file in your project root:

ini
Copy code
EMAIL_USER=your_email@gmail.com
EMAIL_PASS=your_app_password
5. Apply Migrations and Run the Server
bash
Copy code
python manage.py migrate
python manage.py runserver
Then visit 👉 http://127.0.0.1:8000/

🧑‍🎨 UI & Design
Clean and responsive Bootstrap layout

Sidebar for announcements and navigation

Custom pages for posts, profile, and authentication

📁 Project Structure
bash
Copy code
django-blog-app/
│
├── blog/                  # Main blog application
│   ├── templates/blog/    # Blog templates (home, detail, etc.)
│   ├── models.py
│   ├── views.py
│   └── urls.py
│
├── users/                 # User management (profile, register, etc.)
│   ├── templates/users/
│   ├── models.py
│   ├── forms.py
│   └── views.py
│
├── django_project/        # Project configuration files
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── static/                # Static files (CSS, JS, images)
├── media/                 # User-uploaded images (profile pics)
├── db.sqlite3             # Local database
├── manage.py
└── requirements.txt
📬 Email Configuration
The app uses Gmail’s SMTP server for password reset:

python
Copy code
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 465
EMAIL_USE_SSL = True
EMAIL_HOST_USER = os.getenv('EMAIL_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_PASS')

🌍 Deployment
This project can be deployed on:

Render

PythonAnywhere

Vercel (with Django adapter)

Heroku (if available)

🤝 Contributing
Fork the repository

Create a feature branch (git checkout -b feature-name)

Commit your changes (git commit -m "Added new feature")

Push to your branch (git push origin feature-name)

Open a Pull Request

📸 Screenshots
Add screenshots of your app interface here (Home, Post Detail, Profile Page, etc.)

👨‍💻 Author
Stephen Amankwa
🎓 Computer Science & Statistics Student — University of Ghana
💼 Aspiring Full-Stack Software Engineer
🌐 GitHub Profile

