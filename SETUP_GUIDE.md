# WMAD_Assignment Project Setup Guide

## Step 3: Set Up the Virtual Environment
1. **Create the Virtual Environment**:
   - In the `WMAD_Assignment` directory:
    > *python -m venv venv*

2. **Activate the Virtual Environment**:
   - Activate it:
    > *venv\Scripts\activate*
   - Verify with `(venv)` in the terminal prompt.

3. **Install Django**:
   - Install Django:
    > *pip install django*

4. **Save Dependencies**:
   - Generate `requirements.txt`:
    > *pip freeze > requirements.txt*


## Step 4: Create the Django Project and App
1. **Create the Django Project**:
   - Start the project:
    > *django-admin startproject web_restaurant .*

2. **Create an App**:
   - Create the `restaurant` app:
    > *python manage.py startapp restaurant*

   - Add to `INSTALLED_APPS` in `web_restaurant/settings.py`:
    INSTALLED_APPS = [
        ...
        'restaurant',
    ]

3. **Apply Initial Migrations**:
   - Set up the SQLite database:
    > *python manage.py migrate*

4. **Test the Project**:
   - Run the server:
    > *python manage.py runserver*

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
   - Copy all project files (except `venv`) to the cloned repository folder.
   - Ensure `manage.py`, `web_restaurant/`, `restaurant/`, `requirements.txt`, and `.gitignore` are included.

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