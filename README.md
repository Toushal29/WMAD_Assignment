## WebRestaurant
A collaborative Django-based restaurant web application.

## Setup Instructions
1. **Clone the Repository**:
   git clone `https://github.com/Toushal29/WMAD_Assignment.git`
   cd WebRestaurant

2. **Create and Activate a Virtual Environment:**
    python -m venv venv
    venv\Scripts\activate
    # or source venv/bin/activate  # macOS/Linux

3. **Install Dependencies**
    pip install -r requirements.txt

4. **Apply Migration**
    python manage.py migrate

5. **Run the development server**
    python manage.py runserver

    Visit `http://127.0.0.1:8000/` to verify.


## Contributing
1. **Switch to development branch**
    git checkout development

2. **Create a feature branch**
    git checkout -b feature/<your-featureName>
    
3. **Make Changes**
    Edit files (e.g., restaurant/views.py, restaurant/models.py)

    ***If installing new packages:***
        pip install package-name
        pip freeze > requirements.txt

    ***If modifying model:***
        python manage.py makemigrations
        python manage.py migrate

4. **Commit and Push**
    git add .
    git commit -m "<Describe_your_changes>"
    git push origin feature/<your-featureName>

5. **Create a pull request**
    Go to `https://github.com/Toushal29/WMAD_Assignment.git`
    Create a pull request from ***feature/your-featureName*** to development.
    Await review and merge.

6. **Sync with Development:**
    After merges, update your local branch:
    git checkout development
    git pull origin development
    python manage.py migrate  # If new migrations were added