# Django Blog Project

A simple Django blog application with user authentication, post creation, editing, and commenting features.

## Features

- User registration and authentication
- Create, read, update, and delete (CRUD) blog posts
- Comment on posts
- Image upload for posts
- User-friendly interface

## Tech Stack

- **Backend**: Django 6.0.3
- **Database**: SQLite (development), PostgreSQL (production)
- **Frontend**: HTML, CSS, Bootstrap
- **Image Processing**: Pillow
- **Deployment**: Render

## Prerequisites

- Python 3.11+
- pip (Python package manager)
- Git

## Local Setup

### 1. Clone the repository

```bash
git clone <your-github-repo-url>
cd blogproject
```

### 2. Create virtual environment

```bash
python -m venv venv
```

### 3. Activate virtual environment

**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Run migrations

```bash
python manage.py migrate
```

### 6. Create superuser

```bash
python manage.py createsuperuser
```

### 7. Run development server

```bash
python manage.py runserver
```

Access the application at `http://localhost:8000`

## File Structure

```
blogproject/
├── blogapp/                 # Main Django app
│   ├── migrations/         # Database migrations
│   ├── templates/          # HTML templates
│   ├── admin.py           # Admin configuration
│   ├── models.py          # Database models
│   ├── views.py           # View functions
│   └── forms.py           # Django forms
├── blogproject/            # Project configuration
│   ├── settings.py        # Project settings
│   ├── urls.py            # URL routing
│   ├── wsgi.py            # WSGI configuration
│   └── asgi.py            # ASGI configuration
├── media/                  # User-uploaded files
├── templates/              # Base templates
├── manage.py              # Django management script
├── requirements.txt       # Python dependencies
├── Procfile               # Process file for Render
├── render.yaml            # Render deployment config
├── runtime.txt            # Python version
└── README.md             # This file
```

## Environment Variables

Create a `.env` file in the root directory (refer to `.env.example`):

```
DEBUG=False
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1,your-domain.com
DATABASE_URL=your-database-url
```

## Deployment on Render

### 1. Push to GitHub

```bash
git add .
git commit -m "Initial commit"
git push origin main
```

### 2. Connect to Render

1. Go to [Render.com](https://render.com)
2. Sign up or log in
3. Click "New +" and select "Web Service"
4. Connect your GitHub account
5. Select this repository
6. Configure deployment settings:
   - **Name**: blogproject
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt && python manage.py collectstatic --no-input`
   - **Start Command**: `gunicorn blogproject.wsgi`

### 3. Set Environment Variables

In Render dashboard:
1. Go to Environment
2. Add the following variables:
   - `DEBUG`: `False`
   - `SECRET_KEY`: Generate a strong secret key
   - `ALLOWED_HOSTS`: Your Render domain + localhost
   - `DATABASE_URL`: (Render PostgreSQL URL if using)

### 4. Deploy

Click "Deploy" to start the deployment process.

## Creating a Strong SECRET_KEY

Generate a new Django secret key:

```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

## Static Files

Static files are collected and served using WhiteNoise. In production, ensure:
```bash
python manage.py collectstatic --no-input
```

## Database Migrations

To run migrations in production (Render):

This is handled automatically in the `Procfile` with the `release` command.

## Troubleshooting

### 500 Internal Server Error
- Check Render logs for detailed error messages
- Ensure all environment variables are set correctly
- Run migrations on the production database

### Static files not loading
- Run `python manage.py collectstatic`
- Check STATIC_URL and STATIC_ROOT settings

### Database connection issues
- Verify DATABASE_URL is correct
- Check database service status on Render

## Contributing

1. Create a feature branch (`git checkout -b feature/AmazingFeature`)
2. Commit changes (`git commit -m 'Add some AmazingFeature'`)
3. Push to branch (`git push origin feature/AmazingFeature`)
4. Open a Pull Request

## License

This project is open source and available under the MIT License.

## Support

For support, please create an issue in the repository.
