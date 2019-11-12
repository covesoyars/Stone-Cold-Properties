# Stone-Cold-Properties


### How to activate venv (do this first):
  1. go to same folder as djangoenv
  2. source djangoenv/bin/activate

### How to run the app on your computer while connecting to cloud sql:
  1. open stone_cold_props/stone_cold_props/settings.py and find the DATABASES dictionary around line 77
  2. change the port number to something higher than what it is
  3. go to root (stone_cold_props/) and run the command:
      ./cloud_sql_proxy -instances=database-258713:us-central1:instance-508=tcp:<SAME_PORT_NUMBER_IN_SETTINGS> -credential_file=keys/<NAME_OF_KEY_FILE> &
  4. Leave this running in background - this is the connection to the cloud
  5. still in root, run command python manage.py runserver
  6. Leave this running also, in another tab, 
  
### Project structure:
```
.
├── cloud_sql_proxy
├── db.sqlite3
├── keys
│   └── <NAME_OF_KEY_FILE>
├── manage.py
├── property_app
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-37.pyc
│   │   ├── admin.cpython-37.pyc
│   │   ├── apps.cpython-37.pyc
│   │   ├── models.cpython-37.pyc
│   │   ├── urls.cpython-37.pyc
│   │   └── views.cpython-37.pyc
│   ├── admin.py
│   ├── apps.py
│   ├── migrations
│   │   ├── 0001_initial.py
│   │   ├── 0002_auto_20191112_1439.py
│   │   ├── __init__.py
│   │   └── __pycache__
│   │       ├── 0001_initial.cpython-37.pyc
│   │       ├── 0002_auto_20191112_1439.cpython-37.pyc
│   │       └── __init__.cpython-37.pyc
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
└── stone_cold_props
    ├── __init__.py
    ├── __pycache__
    │   ├── __init__.cpython-37.pyc
    │   ├── settings.cpython-37.pyc
    │   ├── urls.cpython-37.pyc
    │   └── wsgi.cpython-37.pyc
    ├── settings.py
    ├── urls.py
    └── wsgi.py
```
