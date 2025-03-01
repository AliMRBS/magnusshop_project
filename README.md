# MagnusShop Project Introduction

This project is an e-commerce website created for practice purposes and is currently available as a test version at [magnusshop.ir](https://magnusshop.ir).

# Installation and Setup Guide

### 1. Clone the Project from GitHub

First, clone the project from GitHub:

```bash
git clone https://github.com/AliMRBS/magnusshop_project.git
```

### 2. Create a Virtual Environment (Optional, Recommended)

Before installing dependencies, it is recommended to create a virtual environment.

#### Run the following command in the project directory:

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies from `requirements.txt`

To install the required dependencies, run the following command:

```bash
pip install -r requirements.txt
```

### 4. Install and Set Up Redis

#### Install Redis:

- **Windows:** Download and install [Redis for Windows](https://github.com/microsoftarchive/redis/releases)

#### Start Redis:

- **Windows:** Run `redis-server.exe`

### 5. Install PostgreSQL

To use PostgreSQL as the database, you need to install it on your system.

- **Windows:** Download and install [PostgreSQL](https://www.postgresql.org/download/)

### 6. Create a Database and User in PostgreSQL

After installing PostgreSQL, create a new database and user:

1. Open the terminal and enter PostgreSQL:

```bash
psql -U postgres
```

2. Create a database:

```sql
CREATE DATABASE magnusshop;
```

3. Create a user:

```sql
CREATE USER magnususer WITH PASSWORD 'yourpassword';
```

4. Grant privileges to the user:

```sql
GRANT ALL PRIVILEGES ON DATABASE magnusshop TO magnususer;
```

### 7. Configure Database Settings in `settings.py`

In the `settings.py` file, update the database section as follows:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'magnusshop',
        'USER': 'magnususer',
        'PASSWORD': 'yourpassword',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### 8. Import Database Backup

To explore all the website's features, a `ms_backup.sql` file is provided in the project directory. To import it, run:

```bash
psql -U magnususer -d magnusshop -f ms_backup.sql
```

### 9. Apply Migrations

To create database tables, run the migrations:

```bash
python manage.py migrate
```

### 10. Create a Superuser

To access the Django admin panel:

```bash
python manage.py createsuperuser
```

### 11. Run the Django Development Server

```bash
python manage.py runserver
```

The project will be accessible at [`http://127.0.0.1:8000`](http://127.0.0.1:8000).

To access the admin panel: [`http://127.0.0.1:8000/admin`](http://127.0.0.1:8000/admin)

## Project Features

### 🛍 User Features:

- ✅ **User registration and login** with **email verification** + **temporary code for password reset and change**
- 🔍 **Search, view, and sort products** by categories and filters
- 🛒 **Add products to the shopping cart** (even without login) + **edit and remove products from the cart**
- 🛒 **Complete purchase and redirect to the [Aghaye Pardakht](https://aqayepardakht.ir/) test payment gateway** (login required)
- ✍️ **Submit reviews for products** (only for verified users)
- ⭐ **Purchase Magnus Plus monthly subscriptions**
- 🏠 **Manage user account information** including phone number, shipping addresses, and order details
- 📦 **Track order status and active subscriptions**

### 🔧 Admin Features:

- 📋 **Manage products, categories, brands, orders, payments, reviews, and more**

# TODO:
-   [x]	Add product comments section
-	[ ] Add articles section to the site
-	[ ] Add product seller model
-	[ ] Add authentication via SMS
-	[ ] Add more payment gateways
-	[ ] Add in-app wallet
-	[ ] Add chat support section


## Technologies Used

- **Backend:** [Django](https://www.djangoproject.com/)
- **Frontend:** HTML, CSS, JavaScript, [Bootstrap](https://getbootstrap.com/), [Tailwind CSS](https://tailwindcss.com/)
- **Database:** [PostgreSQL](https://www.postgresql.org/)
- **Caching:** [Redis](https://redis.io/)
- **Authentication:** Customized Django built-in authentication system and email OTP verification

## Author

[Seyed Ali Mirabbasi](https://github.com/AliMRBS/)

