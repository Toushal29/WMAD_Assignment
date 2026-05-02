# Team members

| Team Name          | ID      |
| ------------------ | ------- |
| Toushal Sampat     | 2413826 |
| Nilesh Khoosee     | 2413908 |
| Hayilsing Nemchand | 2412971 |
| Methilesh Ramsahye | 2413415 |
| Isha Narain        | 2413288 |

### `To be marked individually`


## Development Setup - MOBILE

### Initial Setup

1. **Virtual Environment**:

```bash
python -m venv .venv-mobile
.\.venv-mobile\Scripts\activate  # MOBILE
```

2. **Install Dependencies**:

```bash
pip install -r requirements2.txt
```

3. **Run + Run android version**:

```bash
flet run main.py
```

```bash
flet run --android         #android version
```

---

## Development Setup - WEB

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
   _Only to run if **db.sqlite3** file not present_

```bash
cd .\WMAD_project\
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata menu
```

4. **Run Development Server**:

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` to access the application.