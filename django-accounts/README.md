# django-accounts

Reusable Django app that provides user/account functionality (models, forms, views, templates and admin) so the same code can be used across multiple Django projects.

## Features

- Login / logout / registration views and templates
- Profile management forms and views
- Admin integration and model admin classes
- Static assets and templates packaged with the app
- Migrations included

## Installation (local editable)

From the repository root or the package folder:

```bash
cd /home/rabi/Desktop/HalSoft/Gateway/django-accounts
python3 -m pip install -e .
```

## Quick start

1. Add the app to INSTALLED_APPS in your Django settings:

```py
INSTALLED_APPS = [
    # ...
    "django_accounts",  # or the package name you chose
]
```

2. If the package provides a custom user model, set AUTH_USER_MODEL:

```py
AUTH_USER_MODEL = "django_accounts.User"
```

3. Include URLs in your project `urls.py`:

```py
path("accounts/", include("django_accounts.urls")),
```

4. Run migrations and collect static files:

```bash
python manage.py migrate
python manage.py collectstatic
```

## Configuration

- Templates are provided under `templates/django_accounts/`. Override them by creating the same paths in your project templates directory.
- Static files are provided under `static/django_accounts/`. Override or extend as needed.
