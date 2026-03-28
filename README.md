# Team members

| Team Name          | ID      |
| ------------------ | ------- |
| Toushal Sampat     | 2413826 |
| Nilesh Khoosee     | 2413908 |
| Hayilsing Nemchand | 2412971 |
| Methilesh Ramsahye | 2413415 |
| Isha Narain        | 2413288 |

# Contribution

## To be marked individually

|               |                                  |                                        |                                        |                                     |                                                            |                                                         |
| ------------- | -------------------------------- | -------------------------------------- | -------------------------------------- | ----------------------------------- | ---------------------------------------------------------- | ------------------------------------------------------- |
|               | **Frontend (user view)**         | **Frontend (customer view - web app)** | **Frontend (admin view - admin site)** | **Backend (main page - web app)**   | **Backend (admin site)**                                   | **Backend (customer profile - web app)**                |
| **Toushal**   | Base template                    | Base template + navigation             | Base Template + Navbar                 |                                     | Customer details - get/search + view/update/delete user    | Get + display all details associated to that login user |
|               | Navbar + Footer Component        | User personal details                  | Customer Details Page                  |                                     | Review details - get + view/delete reviews                 | Update + save details associated to that login user     |
|               | About-Contact Us Page            | User reservation details               |                                        |                                     |                                                            | Delete associated login user                            |
|               | Privacy Policy Page              | User Reviews                           |                                        |                                     |                                                            | Change password associated to that login user           |
|               | Review Page                      | User order details                     |                                        |                                     |                                                            |                                                         |
|               | Login + Signup Page              | User Settings                          |                                        |                                     |                                                            |                                                         |
|               | Reset password                   |                                        |                                        |                                     |                                                            |                                                         |
|               | User profile Management Page     |                                        |                                        |                                     |                                                            |                                                         |
|               |                                  |                                        |                                        |                                     |                                                            |                                                         |
| **Isha**      | Home Page                        |                                        | Edit Menu Page                         | Signup                              | Edit Menu - get/search + add/update/delete menu            |                                                         |
|               | Menu Page                        |                                        |                                        | Login                               |                                                            |                                                         |
|               |                                  |                                        |                                        |                                     |                                                            |                                                         |
| **Methilesh** | Order Page                       |                                        | Order Page                             | Add/remove menu to cart + checkout  | Order details - get/search + view/update orders            |                                                         |
|               |                                  |                                        |                                        |                                     |                                                            |                                                         |
| **Nilesh**    | Reservation - login v/s no login |                                        | Reservation page                       | Reservation - save data to database | Reservation details - get/search + view/update reservation |                                                         |
|               |                                  |                                        |                                        |                                     |                                                            |                                                         |
| **Hayilsing** |                                  |                                        |                                        | Database                            |                                                            |                                                         |
|               |                                  |                                        |                                        | reset user password                 |                                                            |                                                         |
|               |                                  |                                        |                                        | Signup                              |                                                            |                                                         |
|               |                                  |                                        |                                        | Login                               |                                                            |                                                         |

# Context File for WebRestaurant Project

## Project Overview

**WebRestaurant** is a collaborative Django-based restaurant web application built with Django 5.2.8. The project allows users to interact with the restaurant website and includes a custom admin site for restaurant management.

### Architecture

- **Backend**: Django 5.2.8 (Python-based web framework)
- **Database**: SQLite3 (default)
- **Frontend**: HTML templates with integrated static files (CSS/JS)
- **Project Structure**: Multi-app Django project with separate apps for the customer-facing site and the custom admin site

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
