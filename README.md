# 9CrappyMemes
This is my Ohsiha course work.
Program is proof on concept.

## How to install
This section will contain basic installation steps
### Create virtual environment

```

$ mkdir <project dir> && cd <project dir>
$ virtualenv -p python3 .venv
# activate virtualenv
$ source .venv/bin/activate

```

### Download git repository: 

```

$ git clone https://github.com/tahv0/crappymemes.git && cd crappymemes
# install requirements
$ pip install -r requirements.txt

```

### Set keys in settings.py for social-auth-app-django. Doesn't work without 0Auth keys.

### Create superuser, migrate and run server

```

$ ./manage.py createsuperuser
$ ./manage.py makemigrations
$ ./manage.py migrate
$ ./manage.py runserver

```
