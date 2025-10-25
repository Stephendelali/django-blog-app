Django Blog App

A modern, dynamic blog web application built with Django, allowing users to create, edit, and view blog posts with an elegant user interface. The project is designed to be simple, scalable, and beginner-friendly — perfect for learning how to build and deploy Django applications.

Features

Create, Edit, and Delete Posts — Authenticated users can manage their blog content easily.

User Authentication — Secure login, signup, and logout functionality.

Home Page Feed — Displays all published posts in reverse chronological order.

Post Detail Page — Read full articles with formatted content.

Comment System (coming soon) — Allow readers to interact and share thoughts.

Modern UI — Clean, minimal, and responsive design.

Admin Panel — Full control over posts, users, and comments.

Tech Stack
Category	Technology
Framework	Django (Python)
Database	SQLite (default) / PostgreSQL (optional)
Frontend	HTML, CSS, Bootstrap
Version Control	Git & GitHub
Deployment (optional)	Render / Vercel / Heroku
Project Structure
django-blog-app/
├── blog/                  # Blog application
│   ├── templates/blog/    # HTML templates
│   ├── models.py          # Database models
│   ├── views.py           # Logic for each route
│   ├── urls.py            # Blog routes
│   └── forms.py           # Forms for creating/editing posts
├── users/                 # Handles authentication
├── static/                # CSS, JS, images
├── django_env/            # Virtual environment (excluded from repo)
├── manage.py              # Django management script
└── README.md              # Project documentation

Installation & Setup

Follow these steps to run the project locally

Clone the Repository

git clone https://github.com/Stephendelali/django-blog-app.git
cd django-blog-app


Create & Activate a Virtual Environment

python -m venv venv
venv\Scripts\activate    # On Windows
source venv/bin/activate # On Mac/Linux


Install Dependencies

pip install -r requirements.txt


Run Migrations

python manage.py migrate


Create a Superuser (optional)

python manage.py createsuperuser


Run the Server

python manage.py runserver


Open in Browser
Visit: http://127.0.0.1:8000

📸 Screenshots

(You can add images later — e.g., UI previews of your homepage, post page, or admin dashboard)

🧠 Future Improvements

✅ Add comment and like functionality

✅ Add categories and tags

✅ Improve UI design with modern styling

✅ Add search and filter features

✅ Deploy the app online

👨‍💻 Author

Stephen Amankwa
🎓 University of Ghana | Level 300
💡 Passionate about software development, data science & AI