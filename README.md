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
WMAD_Assignment/
├── README.md
├── SETUP_GUIDE.md
├── requirements.txt
├── .gitignore
└── WMAD_project/
    ├── manage.py
    ├── WMAD_project/ (main project config)
    │   ├── settings.py
    │   ├── urls.py
    │   └── wsgi.py
    ├── web_app/ (main website)
    │   ├── views.py
    │   ├── urls.py
    │   ├── models.py
    │   ├── templates/
    │   └── static/
    └── control_panel/ (admin panel)
        ├── views.py
        ├── urls.py
        ├── models.py
        ├── middleware.py
        └── templates/
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