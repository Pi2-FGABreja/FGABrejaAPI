# FGABreja-API

[ ![Codeship Status for Pi2-FGABreja/FGABrejaAPI](https://codeship.com/projects/654e6ba0-4420-0133-1881-762794313feb/status?branch=master)](https://codeship.com/projects/104267)

[![Code Climate](https://codeclimate.com/github/Pi2-FGABreja/FGABrejaAPI/badges/gpa.svg)](https://codeclimate.com/github/Pi2-FGABreja/FGABrejaAPI)
[![Coverage Status](https://coveralls.io/repos/Pi2-FGABreja/FGABrejaAPI/badge.svg?branch=master&service=github)](https://coveralls.io/github/Pi2-FGABreja/FGABrejaAPI?branch=master)


### Setting up development environment

```
$ sudo apt-get install python3 python3-pip
$ sudo pip3 install -r requirements.txt
```

```
$ cp settings/databases settings/databases.py
$ cp settings/security settings/security.py
```

```
$ python3 manage.py makemigrations
$ python3 manage.py migrate
$ python3 manage.py runserver
```
