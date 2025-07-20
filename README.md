## 1. Requirements

Ensure you have the following installed:

- Python 3.10+
- pip
- PostgreSQL
- virtualenv (optional but recommended)


## 2. Clone the Repository

`git clone https://github.com/YusufSyam/wqls-be`

`cd wqls-be`

## 3. Set Up Virtual Environment
`python -m venv env`

`source env/bin/activate  # on Windows: env\Scripts\activate`

## 4. Install Dependencies
`pip install -r requirements.txt`

## 5. Create a .env file in the backend root
```
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME='wqls_db'
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432
```

## 6. Run Migrations
```
python manage.py makemigrations
python manage.py migrate
```

## 7. Create Superuser (for Admin Panel)
`python manage.py createsuperuser`

## 8. Run the Server
`python manage.py runserver`




