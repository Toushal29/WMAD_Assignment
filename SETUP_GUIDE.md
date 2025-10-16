# WMAD_Assignment Project Setup Guide

## Step 3: Set Up the Virtual Environment
1. **Create the Virtual Environment**:
   - In the `WMAD_Assignment` directory:
   ```bash
   python -m venv .venv
   ```

2. **Activate the Virtual Environment**:
   - Activate it:
   ```bash
   .\.venv\Scripts\activate 
   ```
   - Verify with `(.venv)` in the terminal prompt.

3. **Install Django**:
   - Install Django:
   ```bash
   pip install django
   ```

4. **Save Dependencies**:
   - Generate `requirements.txt`:
   ```bash
   pip freeze > requirements.txt
   ```

## Step 4: Create the Django Project and App
1. **Create the Django Project**:
   - Start the project:
   ```bash
   django-admin startproject WMAD_project
   ```

2. **Create an App**:
   - Create the `restaurant_app` app:
   ```bash
   python manage.py startapp restaurant_app
   ```

   - Add to `INSTALLED_APPS` in `WMAD_project/settings.py`:
   ```python
    INSTALLED_APPS = [
        ...
        'restaurant_app',
    ]
   ```

3. **Apply Initial Migrations**:
   - Set up the SQLite database:
   ```bash
   python manage.py migrate
   ```

4. **Test the Project**:
   - Run the server:
   ```bash
   python manage.py runserver
   ```
   
   - Visit `http://127.0.0.1:8000/` to verify the Django welcome page.
   - Stop with `Ctrl + C`.

## Step 5: Configure GitHub Integration in VS Code
1. **Install VS Code and GitHub Extension**:
   - Install VS Code if not already installed.
   - Install the **GitHub Pull Requests and Issues** extension (`Ctrl + Shift + X`, search for it).

2. **Clone the Repository**:
   - Open VS Code, press `Ctrl + Shift + P`, run `GitHub: Clone Repository`.
   - Enter `https://github.com/Toushal29/WMAD_Assignment.git`.
   - Choose `C:\Users\...\...\...<directoryName>` as the destination.

3. **Copy Project Files**:
   - Copy all project files (except `.venv`) to the cloned repository folder.
   - Ensure `manage.py`, `WMAD_project/`, `restaurant_app/`, `requirements.txt`, and `.gitignore` are included.

4. **Update `.gitignore`**:
   - Edit `.gitignore` to include:
     venv/
     __pycache__/
     *.pyc
     *.pyo
     *.sqlite3
     *.log
     .vscode/
     .env
     *.tmp
     *.bak
     *.cache
     build/

<hr>

## Step 6: Upload Initial Project to GitHub
1. **Commit Files in VS Code**:
   - Open the Source Control view (`Ctrl + Shift + G`).
   - Stage all files (`+` or **Stage All Changes**).
   - Commit with message: "Initial Django project setup".
   - Click **Publish Branch** to push to the `main` branch.

2. **Create a Development Branch**:
   - In VS Code, run `Git: Create Branch` (`Ctrl + Shift + P`).
   - Name it `development`.
   - Push to GitHub: **Publish Branch**.

## Step 7: Collaboration Workflow
1. **Your Contributions (Without Git)**:
   - Make changes in VS Code (e.g., edit `restaurant/views.py`).
   - Update `requirements.txt` if new packages are installed:
     ```bash
     pip freeze > requirements.txt
     ```
   - If models change, generate migrations:
     ```bash
     python manage.py makemigrations
     python manage.py migrate
     ```
   - In VS Code:
     - Switch to `development` branch (bottom-left branch selector).
     - Create a feature branch (e.g., `feature/your-feature`).
     - Stage, commit, and push changes.
     - Create a pull request on GitHub from `feature/your-feature` to `development`.
   - Alternatively, use GitHub’s web interface:
     - Go to `https://github.com/Toushal29/WMAD_Assignment.git`.
     - Switch to `development` branch.
     - Upload files via **Add file** > **Upload files**.
     - Commit or create a new branch and pull request to `development`.

2. **Collaborators’ Contributions**:
   - Collaborators clone the repository, set up `venv`, and work on feature branches (see `README.md`).
   - They create pull requests to `development`.
   - Review and merge pull requests on GitHub.
   - Download updates from `development` as a ZIP or via VS Code, then run `python manage.py migrate` if new migrations are included.

3. **Merge to Main**:
   - When `development` is stable, create a pull request from `development` to `main` on GitHub.
   - Review and merge after testing.

## Step 8: Create README for Collaborators
- Create `README.md` (see below) with setup and contribution instructions.
- Commit to `development` via VS Code or GitHub.

## Notes
- **OneDrive**: The project syncs automatically via OneDrive for personal backups.
- **Database**: Run `python manage.py migrate` after pulling new migrations.
- **VS Code**: Select `.\venv\Scripts\python.exe` as the Python interpreter.
- **GitHub**: Use the web interface or VS Code for Git operations.



-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Steps to Start a Django App and Configure Files for Frontend Implementation

This guide outlines the steps to create a Django app and configure necessary files to begin implementing your frontend. Assumes you have Django installed and a project initialized.

## 1. Create a Django App
- Run the following command in your terminal within the Django project directory:
    ```bash
    python manage.py startapp `<your_app_name>`
    ```
    - Replace `<your_app_name>` with your desired app name (e.g., `blog`, `store`).

## 2. Register the App
- Open `<your_project_name>/settings.py`.
- Add your app to the `INSTALLED_APPS` list:
    INSTALLED_APPS = [
    ...
    'your_app_name',
    ]

## 3. Cconfigure URLs
- Create a `urls.py` file in `<your_app_name>`/ directory if it doesn't exist.
- Define app-specific URL patterns in `<your_app_name>/urls.py`:

    ```python
    from django.urls import path
    from . import views

    urlpatterns = [
        path('', views.home, name='home'),  # Example route
    ]
    ```

- Include the app’s URLs in the project’s `<your_project_name>/urls.py`:

    ```python
    from django.contrib import admin
    from django.urls import path, include

    urlpatterns = [
        path('admin/', admin.site.urls),
        path('', include('your_app_name.urls')),  # Include app URLs
    ]
    ```

## 4. Create Views
- In `<your_app_name>/views.py`, define views to handle requests:

    ``` python
    from django.shortcuts import render

    def home(request):
        return render(request, 'your_app_name/home.html')
    ```

> This example renders a template called `home.html`.

## 5. Set up Templates
- Create a templates directory in your app: `<your_app_name>/templates/<your_app_name>/`.
- Create an HTML file (e.g., `home.html`) in the templates directory:

    ```html
    <!DOCTYPE html>
    <html>
    <head>
        <title>My Django App</title>
    </head>
    <body>
        <h1>Welcome to my app!</h1>
    </body>
    </html>
    ```

- Ensure `TEMPLATES` in `settings.py` is configured correctly:
    ```python
    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [],  # Add project-wide template directory if needed
            'APP_DIRS': True,
            ...
        }
    ]
    ```

## 6. Configure Static Files (for CSS, JS, Images)
- Create a `static` directory in your app: `<your_app_name>/static/<your_app_name>/`.
- Add static files (e.g., `styles.css`, `script.js`):
    ```css
    /* your_app_name/static/your_app_name/styles.css */
    body {
        background-color: #f0f0f0;
    }
    ```

- In `settings.py`, ensure static files are configured:
    ```python
    STATIC_URL = '/static/'
    STATICFILES_DIRS = [
        BASE_DIR / "your_app_name/static",
    ]
    ```

- Run the following command to collect static files (for production):
    ```bash
    python manage.py collectstatic
    ```

- In your template, load static files:
    ```html
    {% load static %}
    <link rel="stylesheet" href="{% static 'your_app_name/styles.css' %}">
    ```

## 7. Test the Setup
- Run the development server:
    ```bash
    python manage.py runserver
    ```
- Visit `http://127.0.0.1:8000/` in your browser to verify the app is working.

## 8. Start Frontend Implementation
- Add more HTML templates in `<your_app_name>/templates/<your_app_name>/`.
- Enhance with CSS and JavaScript in `<your_app_name>/static/<your_app_name>`/
- Use Django template tags for dynamic content:
    ```html
    <h1>{{ variable_name }}</h1>
    ```

- Update views to pass data to templates:
    ```python
    def home(request):
        return render(request, 'your_app_name/home.html', {'variable_name': 'Hello, World!'})
    ```


## ***NOTE***
- Ensure migrations are applied if you add models:
    ```bash
    python manage.py makemigrations
    ```

    ```bash
    python manage.py migrate
    ```
- Use a frontend framework (e.g., Bootstrap, React) by including their CDNs or integrating via npm if needed.

- Keep your project structure organized for scalability.