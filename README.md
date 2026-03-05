# Team members
| Team Name          | ID      |
|--------------------|---------|
| Toushal Sampat     | 2413826 |
| Nilesh Khoosee     | 2413908 |
| Hayilsing Nemchand | 2412971 |
| Methilesh Ramsahye | 2413415 |
| Isha Narain        | 2413288 |

# Contribution
## To be marked individually

| Frontend (user view) |                                   |
|----------------------|-----------------------------------|
| Toushal              | Base template                     |
|                      | Navbar + Footer Component         |
|                      | About-Contact Us Page             |
|                      | Privacy Policy Page               |
|                      | Review Page                       |
|                      | Login + Signup Page               |
|                      | Reset password                    |
|                      | User profile Management Page      |
|                      |                                   |
| Isha                 | Home Page                         |
|                      | Menu Page                         |
|                      |                                   |
| Methilesh            | Order Page                        |
|                      |                                   |
| Nilesh               | Reservation - login v/s no login  |


| Frontend (admin view - admin site) |                         |
|------------------------------------|-------------------------|
| Toushal                            | Base Template + Navbar  |
|                                    | Customer Details Page   |
|                                    |                         |
| Nilesh                             | Reservation page        |
|                                    |                         |
| Isha                               | Edit Menu Page          |
|                                    |                         |
| Methilesh                          | Order Page              |

| Frontend (customer view - web app) |                             |
|------------------------------------|-----------------------------|
| Toushal                            | Base template + navigation  |
|                                    | User personal details       |
|                                    | User reservation details    |
|                                    | User Reviews                |
|                                    | User order details          |
|                                    | User Settings               |


| Backend (main page - web app) |                                      |
|-------------------------------|--------------------------------------|
| Hayilsing                     | Database                             |
|                               | reset user password                  |
|                               |                                      |
| Hayilsing + Isha              | Signup                               |
|                               | Login                                |
|                               |                                      |
| Methilesh                     | Add/remove menu to cart + checkout   |
|                               |                                      |
| Nilesh                        | Reservation - save data to database  |

| Backend (admin site) |                                                             |
|----------------------|-------------------------------------------------------------|
| Toushal              | Customer details - get/search + view/update/delete user     |
|                      | Review details - get + view/delete reviews                  |
|                      |                                                             |
| Nilesh               | Reservation details - get/search + view/update reservation  |
|                      |                                                             |
| Methilesh            | Order details - get/search + view/update orders             |
|                      |                                                             |
| Isha                 | Edit Menu - get/search + add/update/delete menu             |

| Backend (customer profile - web app) |                                                          |
|--------------------------------------|----------------------------------------------------------|
| Toushal                              | Get + display all details associated to that login user  |
|                                      | Update + save details associated to that login user      |
|                                      | Delete associated login user                             |
|                                      | Change password associated to that login user            |

# Context File for WebRestaurant Project

## Project Overview

**WebRestaurant** is a collaborative Django-based restaurant web application built with Django 5.2.8. The project allows users to interact with a restaurant website while providing an admin control panel with maintenance mode functionality.

### Architecture

- **Backend**: Django 5.2.8 (Python-based web framework)
- **Database**: SQLite3 (default)
- **Frontend**: HTML templates with integrated static files (CSS/JS)
- **Project Structure**: Multi-app Django project with separate apps for web interface and control panel

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
   *Only to run if **db.sqlite3** file not present*
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