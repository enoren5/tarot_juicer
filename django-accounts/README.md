````markdown
# django-accounts

**django-accounts** is a reusable Django app providing authentication and account management functionality, including login, logout, portal access, and protection-based redirection. This package is designed to be easily integrated into multiple Django projects with minimal setup.

---

## Features

- Login and logout views with templates.
- Portal view protected via a custom decorator.
- Session timeout functionality.
- Template and static asset packaging for easy customization.
- Models for authentication toggles and passphrases.
- Works on Windows, MacOS, and Linux.

---

## Requirements

- Python 3.13.1
- Django 5.2.7

---

## Installation

### Local Editable Install

```bash
cd /path/to/django-accounts
python3 -m pip install -e .
````

> **Note:** For Windows, use `python` instead of `python3` if `python3` is not available.

---

## Quick Start

1. Add the app to `INSTALLED_APPS` in your Django settings:

```python
INSTALLED_APPS = [
    # ...
    "django_accounts",
]
```

2. Include the URLs in your project `urls.py`:

```python
from django.urls import path, include

urlpatterns = [
    # ...
    path("accounts/", include("django_accounts.urls")),
]
```

3. Run migrations and collect static files:

```bash
python manage.py migrate
python manage.py collectstatic
```

---

## Models

### `AuthToggle`

Used for controlling access and session timeout settings.

| Field          | Type       | Default | Description                                          |
| -------------- | ---------- | ------- | ---------------------------------------------------- |
| `is_protected` | Boolean    | False   | Protects certain routes for authenticated users only |
| `faravahar`    | Boolean    | False   | Custom flag (can be used for template context)       |
| `nuclear`      | Boolean    | True    | Custom flag (can be used for template context)       |
| `timeout`      | Integer    | 1       | Session timeout in minutes                           |
| `email`        | EmailField | ''      | Default email (used in templates/context)            |

### `PassPhrase`

Simple model to store a passphrase.

| Field        | Type      | Default                 | Description                |
| ------------ | --------- | ----------------------- | -------------------------- |
| `passphrase` | CharField | `"YourMagicPassphrase"` | Stores a single passphrase |

---

## Forms

* `LoginForm` (default Django authentication login form is used)

---

## Views

### Class-Based Views

| View         | URL                 | Description                                                                                       |
| ------------ | ------------------- | ------------------------------------------------------------------------------------------------- |
| `Gateway`    | `/accounts/`        | Login view with session management and protected redirect. Uses `accounts/gateway.html` template. |
| `EndSession` | `/accounts/logout/` | Logs the user out and redirects to `index`. Uses `accounts/logged_out.html` template.             |

### Function-Based Views

| View     | URL                 | Description                                                                      |
| -------- | ------------------- | -------------------------------------------------------------------------------- |
| `portal` | `/accounts/portal/` | Protected portal page that requires authentication. Uses `landings/portal.html`. |

---

## URL Patterns

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.Gateway.as_view(), name='index'),
    path('portal/', views.portal, name='portal'),
    path('logout/', views.EndSession.as_view(), name='logout'),
]
```

---

## Custom Decorators

### `protected_redirect`

A decorator used to protect routes and redirect unauthenticated users:

```python
from django.shortcuts import redirect
from .models import AuthToggle

def protected_redirect(view_func):
    .......
```

---

## Templates

All templates are under `django_accounts/templates/`. Key templates include:

```
templates/
    accounts/
        gateway.html
        logged_out.html
```

---

## Static Files

* CSS: `django_accounts/static/css/`
* Images: `django_accounts/static/img/`

---

## Usage Example

### Login Redirect for Protected Portal

```python
from django_accounts.custom_decorator import protected_redirect

@protected_redirect
def portal(request):
    # Your portal logic here
    return render(request, 'landings/portal.html')
```

---

## Settings / Customization

* The session timeout is defined by `AuthToggle.timeout` (in minutes).
* Route protection is controlled by `AuthToggle.is_protected`.

No additional settings are required.

---

## Supported Platforms

* **Windows**
* **MacOS**
* **Linux**

> Make sure Python 3.13.1 and Django 5.2.7 are installed. For Windows, use `python` instead of `python3` if needed.

---

## License

MIT License. See `LICENSE` file for details.

