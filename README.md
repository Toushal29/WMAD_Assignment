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
|                      | Navbar                            |
|                      | footer                            |
|                      | About-Contact Us                  |
|                      | Privacy Policy                    |
|                      | Login                             |
|                      | Signup                            |
|                      | Reset password                    |
|                      | User profile Management Page      |
|                      |                                   |
| Isha                 | Home                              |
|                      | Menu                              |
|                      |                                   |
| Methilesh            | Order                             |
|                      |                                   |
| Nilesh               | Reservation - login v/s no login  |
|                      |                                   |
|                      |                                   |

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

**WebRestaurant** is a collaborative Django-based restaurant web application built with Django 5.2.7. The project allows users to interact with a restaurant website while providing an admin control panel with maintenance mode functionality.

### Architecture

- **Backend**: Django 5.2.7 (Python-based web framework)
- **Database**: SQLite3 (default)
- **Frontend**: HTML templates with integrated static files (CSS/JS)
- **Project Structure**: Multi-app Django project with separate apps for web interface and control panel

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
│           bolrenverse.jpg
│           briani.jpg
│           briani_hmpKdxd.jpg
│           briani_MLlGnDy.jpg
│           caripoulet.jpg
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
│   │       │       reservation.css
│   │       │       signup.css
│   │       │
│   │       ├───images
│   │       │       biryani.jpg
│   │       │       bk_img2.png
│   │       │       bk_img3.png
│   │       │       bk_img5.png
│   │       │       bk_img6.png
│   │       │       chicken_curry.png
│   │       │       farata_curry.png
│   │       │       instagramIcon.png
│   │       │       login.png
│   │       │       logo.png
│   │       │       mine_frite.png
│   │       │       min_apollo.png
│   │       │       twitterIcon.png
│   │       │       whatsAppIcon.png
│   │       │
│   │       └───js
│   │               login.js
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
│   │       │       reservations.html
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
│   │       │       checkout.html
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
   *Only to run if **db.sqlite3** file not present*
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Run Development Server**:
   ```bash
   python manage.py runserver
   ```
   Visit `http://127.0.0.1:8000/` to access the application.
