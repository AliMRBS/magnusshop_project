
# معرفی پروژه MagnusShop
این پروژه یک وبسایت اینترنتی فروشگاهی است که به منظور تمرین انجام شده است و در حال حاضر به صورت آزمایشی از طریق آدرس [magnusshop.ir](https://magnusshop.ir) در دسترس است.


# راهنمای نصب و راه‌اندازی پروژه


### 1. کلون کردن پروژه از گیت
ابتدا پروژه را از گیت کلون کنید:

```bash
git clone https://github.com/AliMRBS/magnusshop_project.git
```
### 2. ساخت محیط مجازی (اختیاری، توصیه‌شده)

قبل از نصب وابستگی‌ها، پیشنهاد می‌شود یک محیط مجازی ایجاد کنید.
#### در مسیر پروژه، دستور زیر را اجرا کنید:
```bash
python -m venv venv
```
### 3. نصب وابستگی‌ها از فایل `requirements.txt`
برای نصب وابستگی‌ها، دستور زیر را اجرا کنید:

```bash
pip install -r requirements.txt
```

### 4. نصب و راه‌اندازی Redis

#### نصب Redis:
- **ویندوز:** دانلود و نصب [Redis for Windows](https://github.com/microsoftarchive/redis/releases)

#### راه‌اندازی Redis:
- **ویندوز:** اجرای `redis-server.exe`

### 5. نصب PostgreSQL

برای استفاده از PostgreSQL به عنوان دیتابیس، ابتدا باید PostgreSQL را روی سیستم خود نصب کنید.

- **ویندوز:** دانلود و نصب [PostgreSQL](https://www.postgresql.org/download/)

### 6. ایجاد دیتابیس و کاربر در PostgreSQL

پس از نصب PostgreSQL، یک دیتابیس و کاربر جدید ایجاد کنید:

1. از طریق ترمینال وارد PostgreSQL شوید:

```bash
psql -U postgres
```

2. ایجاد دیتابیس:

```sql
CREATE DATABASE magnusshop;
```

3. ایجاد کاربر:

```sql
CREATE USER magnususer WITH PASSWORD 'yourpassword';
```

4. اعطای دسترسی به کاربر برای دیتابیس:

```sql
GRANT ALL PRIVILEGES ON DATABASE magnusshop TO magnususer;
```

### 7. تنظیمات دیتابیس در فایل `settings.py`

در فایل `settings.py`، بخش دیتابیس را به شکل زیر تغییر دهید:

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

### 8. ایمپورت بکاپ دیتابیس

برای مشاهده تمامی قابلیت های سایت یک فایل `backup.sql` در دایرکتوری پروژه قرار داده شده است. برای استفاده از آن دستور زیر را اجرا کنید:

```bash
psql -U magnususer -d magnusshop -f backup.sql
```

### 9. انجام مایگریت‌ها

برای ایجاد جداول دیتابیس، مایگریشن‌ها را اجرا کنید:

```bash
python manage.py migrate
```

### 20. ساخت یک سوپر یوزر

برای دسترسی به پنل مدیریت Django:

```bash
python manage.py createsuperuser
```

### 11. اجرای سرور توسعه Django

```bash
python manage.py runserver
```

پروژه از طریق [`http://127.0.0.1:8000`](http://127.0.0.1:8000) در دسترس است.

برای ورود به بخش مدیریت: [`http://127.0.0.1:8000/admin`](http://127.0.0.1:8000/admin)



# معرفی اپ ها
در این پروژه برای خوانایی بیشتر و قابلیت توسعه پذیری از 6 اپلیکیشن استفاده شده است.

## 1-	اپ shop: 
در این اپ مدل های مربوط به محصولات، دسته بندی محصولات، ویژگی های محصولات و برند ها قرار دارند. بنابراین فرایند های نمایش محصولات، دسته بندی، جستجو، نمایش ویژگی ها، مرتب سازی بر اساس و ... در ویوهای این اپ قرار دارند.


## 2- اپ magnusplus: 
در این اپ مدل های مربوط به پکیج های اشتراک ماهیانه سایت و ویژگی های هر پکیج قرار دارد. و عملیات خرید اشتراک در این مدل مدیریت میشود.


## 3-	اپ account: 
مدل های دیفالت جنگو برای سیستم مدیریت کاربران این پروژه کافی نبود به همین دلیل یک اپ جداگانه برای این کار درنظر گرفته شده است تا قابلیت توسعه پذیری پروژه حفظ شود. درمدل های این اپ اطلاعات هر کاربر مانند اطلاعات هویتی، اطلاعات تماس، آدرس ها و وضعیت اشتراک کاربران ذخیره می شود. همچنین در این اپ فرایند های ورود، خروج، ثبت نام، مدیریت آدرس ها و ویرایش اطلاعات کاربری انجام می شود. اعتبارسنجی های مورد نیاز برای فرم بخش های مختلف نیز انجام شده است. 


## 4-	اپ cart: 
در این اپ کلاس cart قرار دارد که با استفاده از ساخت یک session برای سبد خرید، تعداد و قیمت محصولات سبد خرید کاربر را ذخیره میکند. همچنین فرایندهای افزودن محصول، حذف، ویرایش و ... در این اپ مدیریت می شوند. 


## 5-	اپ payment: 
در این اپ مدل های مربوط به ثبت سفارش قرار دارند و عملیات ایجاد یک سفارش در این اپ صورت میگیرد.


## 6-	اپ finance:
این مدل اطلاعات پرداخت ها و همچنین درگاه های پرداخت مختلف را ذخیره می کند. و در فایل ویوها فرایند ایجاد و وریفای تراکنش صورت میگیرد. (در حال حاضر پروژه به سندباکس درگاه پرداخت [آقای پرداخت](https://aqayepardakht.ir/) متصل است و قابلیت تست پرداخت های موفق و ناموفق را دارد) 



# TODO:
- [x]	Add product comments section
-	[ ] Add articles section to the site
-	[ ] Add product seller model
-	[ ] Add authentication via SMS
-	[ ] Add more payment gateways
-	[ ] Add in-app wallet
-	[ ] Add chat support section


## تکنولوژی‌های استفاده‌شده
- **Backend:** [Django 4.2](https://www.djangoproject.com/)
- **Frontend:** HTML, CSS, JavaScript, [Bootstrap](https://getbootstrap.com/), [Tailwind CSS](https://tailwindcss.com/)
- **Database:** [PostgreSQL 17](https://www.postgresql.org/)
- **Caching:** [Redis](https://redis.io/)
- **Authentication:** Customized Django built-in authentication system and email OTP verification**

## نویسنده
[AliMRBS](https://github.com/AliMRBS/)


