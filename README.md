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

|               |                                  |                                        |                                     |                                                         |
| ------------- | -------------------------------- | -------------------------------------- | ----------------------------------- | ------------------------------------------------------- |
|               | **Frontend (user view)**         | **Frontend (customer view - web app)** | **Backend (main page - web app)**   | **Backend (customer profile - web app)**                |
| **Toushal**   | Base template                    | Base template + navigation             |                                     | Get + display all details associated to that login user |
|               | Navbar + Footer Component        | User personal details                  |                                     | Update + save details associated to that login user     |
|               | About-Contact Us Page            | User reservation details               |                                     | Delete associated login user                            |
|               | Privacy Policy Page              | User Reviews                           |                                     | Change password associated to that login user           |
|               | Review Page                      | User order details                     |                                     |                                                         |
|               | Login + Signup Page              | User Settings                          |                                     |                                                         |
|               | Reset password                   |                                        |                                     |                                                         |
|               | User profile Management Page     |                                        |                                     |                                                         |
| **Isha**      | Home Page                        |                                        | Signup                              |                                                         |
|               | Menu Page                        |                                        | Login                               |                                                         |
| **Methilesh** | Order Page                       |                                        | Add/remove menu to cart + checkout  |                                                         |
| **Nilesh**    | Reservation - login v/s no login |                                        | Reservation - save data to database |                                                         |
| **Hayilsing** |                                  |                                        | Database                            |                                                         |
|               |                                  |                                        | reset user password                 |                                                         |
|               |                                  |                                        | Signup                              |                                                         |
|               |                                  |                                        | Login                               |                                                         |

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