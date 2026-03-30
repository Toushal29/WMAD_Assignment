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

---

## Development Setup - MOBILE

### Initial Setup

1. **Virtual Environment**:

```bash
python -m venv .venv-mobile
.\.venv-mobile\Scripts\activate  # MOBILE
```

2. **Install Dependencies**:

```bash
pip install flet
```

3. **Create Project + Run**:

```bash
flet create mobile_app
```

```bash
cd mobile_app
pip install flet-geolocator flet-permission-handler httpx
```

```bash
flet run
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