# Context File for WebRestaurant Project

## Project Overview

**WebRestaurant** is a collaborative Django-based restaurant web application built with Django 5.2.7. The project allows users to interact with a restaurant website while providing an admin control panel with maintenance mode functionality.

### Architecture

- **Backend**: Django 5.2.7 (Python-based web framework)
- **Database**: SQLite3 (default)
- **Frontend**: HTML templates with integrated static files (CSS/JS)
- **Project Structure**: Multi-app Django project with separate apps for web interface and control panel

### Core Apps

1. **web_app**: Main restaurant website interface

   - Home page
   - Menu display
   - Order placement
   - Reservation system
   - Login/Signup
   - About/Contact pages
   - Privacy policy

2. **control_panel**: Administrative control panel
   - Dashboard with server status
   - Maintenance mode toggle
   - Log viewing functionality

## Key Features

### Maintenance Mode

- Custom middleware allows toggling the entire site into maintenance mode
- When enabled, customers see a maintenance page while control panel remains accessible
- Toggle functionality available through the control panel dashboard

### Logging

- Debug logging configured to write to `debug.log` file
- Captures Django-level debug information for troubleshooting

## Project Structure

```
C:.
│   control_panel.log
│   db.sqlite3
│   manage.py
│   menu_items
│   
├───admin_site
│   │   admin.py
│   │   apps.py
│   │   middleware.py
│   │   models.py
│   │   tests.py
│   │   urls.py
│   │   views.py
│   │   __init__.py
│   │
│   ├───migrations
│   │   │   __init__.py
│   │   │
│   │   └───__pycache__
│   │           __init__.cpython-313.pyc
│   │
│   ├───static
│   │   └───admin_site
│   │       └───css
│   │               admin_navbar.css
│   │               orders.css
│   │
│   ├───templates
│   │   └───admin_site
│   │           base_admin.html
│   │           customer_details.html
│   │           dashboard.html
│   │           edit_menu.html
│   │           edit_price.html
│   │           feedback.html
│   │           login.html
│   │           orders.html
│   │           reservation.html
│   │
│   └───__pycache__
│
├───control_panel
│   │   admin.py
│   │   apps.py
│   │   middleware.py
│   │   models.py
│   │   tests.py
│   │   urls.py
│   │   views.py
│   │   __init__.py
│   │
│   ├───migrations
│   │   │   __init__.py
│   │   │
│   │   └───__pycache__
│   │           __init__.cpython-313.pyc
│   │
│   ├───static
│   │   └───control_panel
│   │       ├───css
│   │       │       dashboard.css
│   │       │
│   │       └───images
│   │               logo.png
│   │
│   ├───templates
│   │   └───control_panel
│   │           customer_maintenance.html
│   │           dashboard.html
│   │           logs.html
│   │
│   └───__pycache__
│
├───media
│   └───menu_images
│           briani.jpg
│
├───web_app
│   │   admin.py
│   │   apps.py
│   │   forms.py
│   │   models.py
│   │   tests.py
│   │   urls.py
│   │   views.py
│   │   __init__.py
│   │
│   ├───migrations
│   │   │   0001_initial.py
│   │   │   __init__.py
│   │   │
│   │   └───__pycache__
│   │
│   ├───static
│   │   ├───menu_images
│   │   │       bk_img6.png
│   │   │       food1.webp
│   │   │       food10.webp
│   │   │       food11.webp
│   │   │       food11_egr8qdf.webp
│   │   │       food2.jpg
│   │   │       food3.webp
│   │   │       food5.webp
│   │   │       food6.webp
│   │   │       food7.webp
│   │   │       food8.webp
│   │   │       food9.jpg
│   │   │
│   │   └───web_app
│   │       ├───css
│   │       │       about_contact.css
│   │       │       footer.css
│   │       │       home.css
│   │       │       log_in.css
│   │       │       menu.css
│   │       │       my_orders.css
│   │       │       navbar.css
│   │       │       order.css
│   │       │       password_reset.css
│   │       │       privacy_policy.css
│   │       │       profile.css
│   │       │       signup.css
│   │       │
│   │       ├───images
│   │       │       biryani.jpg
│   │       │       bk_img2.png
│   │       │       bk_img3.png
│   │       │       bk_img5.png
│   │       │       bk_img6.png
│   │       │       food1.webp
│   │       │       food10.webp
│   │       │       food11.webp
│   │       │       food2.jpg
│   │       │       food3.webp
│   │       │       food4.webp
│   │       │       food5.webp
│   │       │       food6.webp
│   │       │       food7.webp
│   │       │       food8.webp
│   │       │       food9.jpg
│   │       │       instagramIcon.png
│   │       │       login.png
│   │       │       logo.png
│   │       │       min_apollo.png
│   │       │       twitterIcon.png
│   │       │       whatsAppIcon.png
│   │       │
│   │       └───js
│   │               login.js
│   │               my_orders.js
│   │               order.js
│   │               signup.js
│   │
│   ├───templates
│   │   ├───registration
│   │   │       custom_change_password.html
│   │   │       custom_change_password_done.html
│   │   │       custom_reset_complete.html
│   │   │       custom_reset_confirm.html
│   │   │       custom_reset_email.html
│   │   │       custom_reset_email.txt
│   │   │       custom_reset_request.html
│   │   │       custom_reset_sent.html
│   │   │       custom_reset_subject.txt
│   │   │       login.html
│   │   │       signup.html
│   │   │
│   │   └───web_app
│   │       ├───account
│   │       │       base_account.html
│   │       │       confirm_delete.html
│   │       │       orders.html
│   │       │       profile.html
│   │       │       reviews.html
│   │       │       settings.html
│   │       │
│   │       ├───components
│   │       │       footer.html
│   │       │       navbar.html
│   │       │
│   │       ├───main_page
│   │       │       about_contact.html
│   │       │       base.html
│   │       │       home.html
│   │       │       menu.html
│   │       │       my_orders.html
│   │       │       order.html
│   │       │       reservation.html
│   │       │
│   │       └───other_pages
│   │               privacy_policy.html
│   │
│   └───__pycache__
│
└───WMAD_project
    │   asgi.py
    │   models.py
    │   settings.py
    │   urls.py
    │   wsgi.py
    │   __init__.py
    │
    └───__pycache__
```

## Development Setup

### Initial Setup

1. **Virtual Environment**:

   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate  # Windows
   ```

2. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Database Migrations**:

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Run Development Server**:
   ```bash
   python manage.py runserver
   ```
   Visit `http://127.0.0.1:8000/` to access the application.

### Key Commands

- **Create migrations**: `python manage.py makemigrations`
- **Apply migrations**: `python manage.py migrate`
- **Run server**: `python manage.py runserver`
- **Collect static files**: `python manage.py collectstatic`

## Development Conventions

### Project Workflow

1. Switch to development branch: `git checkout development`
2. Create feature branch: `git checkout -b feature/<featureName>`
3. Make changes
4. If installing new packages: `pip install package-name` then `pip freeze > requirements.txt`
5. If modifying models: `python manage.py makemigrations` then `python manage.py migrate`
6. Commit and push: `git add .` → `git commit -m "message"` → `git push origin feature/<featureName>`
7. Create pull request from feature branch to development
8. After merge: Sync with development branch

### Code Structure

- Separate apps for different functionality (web_app vs control_panel)
- Template structure: `app_name/templates/app_name/page.html`
- Static files: `app_name/static/app_name/`
- URL routing configured via `urls.py` files in each app

## Configuration Details

### Settings

- Debug mode: Enabled (`DEBUG = True`)
- Allowed hosts: `['*']` (not production-ready)
- Static files: Located at `web_app/static/`
- Database: SQLite3 (`db.sqlite3`)
- Custom maintenance mode setting: `MAINTENANCE_MODE = False`

### Middleware

- Custom `MaintenanceMiddleware` handles site-wide maintenance mode
- Standard Django security and session middleware included

### URLs

- Main website accessible at root path (`/`)
- Control panel accessible at `/control/`
- Admin interface at `/admin/`

## Important Files & Locations

- **Settings**: `WMAD_project/settings.py` - Core Django configuration
- **Main URLs**: `WMAD_project/urls.py` - Root URL routing
- **Middleware**: `control_panel/middleware.py` - Maintenance mode logic
- **Control Panel Views**: `control_panel/views.py` - Dashboard and maintenance toggle
- **Web App Views**: `web_app/views.py` - Main site page handlers
- **Requirements**: `requirements.txt` - Python dependencies
- **Log File**: `debug.log` - Debug information (created when application runs)

## Special Features

### Maintenance Mode Implementation

1. Toggle accessible via control panel at `/control/maintenance/toggle/`
2. Configurable via `MAINTENANCE_MODE` setting in `settings.py`
3. Custom middleware renders maintenance page to customers when enabled
4. Control panel (`/control/`) remains accessible during maintenance

### Dashboard Functionality

- Shows server status
- Displays restaurant name ("Saveur Moris")
- Shows maintenance mode status
- Displays recent logs (last 50 lines from debug.log)

## Testing & Quality Assurance

The project includes Django's standard testing framework. Tests would typically be added to the `tests.py` files in each app. For now, there are placeholder test files in both apps.

## Security Considerations

- The project uses Django's built-in security middleware
- Secret key is currently using a default development key and should be changed for production
- Maintenance mode provides a way to take the site offline for updates
- Static files configuration follows Django best practices

## Future Enhancement Areas

Potential areas for improvement:

- Production security settings (proper SECRET_KEY, allowed hosts, etc.)
- Database configuration for production environments
- Enhanced logging configuration
- Additional model fields for restaurant functionality
- Authentication and authorization features
