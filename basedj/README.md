# basedj - A base for your next django project (based off [lithium](https://github.com/wsvincent/lithium))
basedj is a batteries-included Django starter project with everything you need to start coding, including user authentication, static files, default styling, debugging, DRY forms, custom error pages, and more. Coming from [lithium](https://github.com/wsvincent/lithium), you also get a full deployment pipline with docker + environs and vendored bootstrap, htmx, and alpine.js


## 🚀 Features
- Django 5.1 & Python 3.13
- Installation via [uv](https://github.com/astral-sh/uv), [Pip](https://pypi.org/project/pip/) or [Docker](https://www.docker.com/)
- User authentication--log in, sign up, password reset--via [django-allauth](https://github.com/pennersr/django-allauth)
- Static files configured with [Whitenoise](http://whitenoise.evans.io/en/stable/index.html)
- Styling with [Bootstrap v5](https://getbootstrap.com/)
- Debugging with [django-debug-toolbar](https://github.com/jazzband/django-debug-toolbar)
- DRY forms with [django-crispy-forms](https://github.com/django-crispy-forms/django-crispy-forms)
- Custom 404, 500, and 403 error pages

## Table of Contents
* **[Installation](#installation)**
  * [uv](#uv)
  * [Pip](#pip)
  * [Docker](#docker)
* [Next Steps](#next-steps)
* [Contributing](#contributing)
* [Support](#support)
* [License](#license)

## 📖 Getting Started
After cloning the repo, setup your environment variables 

```bash
cp .env.example .env
# add your variables to .env

```

### uv
You can use [uv](https://docs.astral.sh/uv/) to create a dedicated virtual environment.

```
$ uv sync
```

Then run `migrate` to configure the initial database. The command `createsuperuser` will create a new superuser account for accessing the admin. Execute the `runserver` command to start up the local server.

```
$ uv run manage.py migrate
$ uv run manage.py createsuperuser
$ uv run manage.py runserver
# Load the site at http://127.0.0.1:8000 or http://127.0.0.1:8000/admin for the admin
```

### Pip
To use Pip, create a new virtual environment and then install all packages hosted in `requirements.txt`. Run `migrate` to configure the initial database. and `createsuperuser` to create a new superuser account for accessing the admin. Execute the `runserver` command to start up the local server.

```
(.venv) $ pip install -r requirements.txt
(.venv) $ python manage.py migrate
(.venv) $ python manage.py createsuperuser
(.venv) $ python manage.py runserver
# Load the site at http://127.0.0.1:8000 or http://127.0.0.1:8000/admin for the admin
```

### Docker

If you are using docker for development, you will need to update `DATABASE_URL` to reflect your postgres database

```bash
DATABASE_URL=postgresql://postgres:postgres@db:5432/postgres
```

The `INTERNAL_IPS` configuration in `django_project/settings.py` must be also be updated:

```python
# config/settings.py
# django-debug-toolbar
import socket
hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
INTERNAL_IPS = [ip[:-1] + "1" for ip in ips]
```

And then proceed to build the Docker image, run the container, and execute the standard commands within Docker.

```
$ docker compose up -d --build
$ docker compose exec web python manage.py migrate
$ docker compose exec web python manage.py createsuperuser
# Load the site at http://127.0.0.1:8000 or http://127.0.0.1:8000/admin for the admin
```

## Next Steps

- Update the [EMAIL_BACKEND](https://docs.djangoproject.com/en/4.0/topics/email/#module-django.core.mail) and connect with a mail provider.
- Make the [admin more secure](https://opensource.com/article/18/1/10-tips-making-django-admin-more-secure).
- `django-allauth` supports [social authentication](https://django-allauth.readthedocs.io/en/latest/socialaccount/index.html) if you need that.

Will Vincent covers all of these steps in tutorials and premium courses over at [LearnDjango.com](https://learndjango.com).

## Vendored packages
- [Bootstrap 5.3.8](https://getbootstrap.com/docs/5.3/getting-started/introduction/)
- [htmx 2.0.8](https://htmx.org/docs/)
- [alpine.js 3.15.8](https://alpinejs.dev/start-here)
- [alpine-ajax 0.12.7](https://alpine-ajax.js.org/reference/)

## ⭐️ Support

Give a ⭐️ if this project helped you!

## License

[The MIT License](LICENSE)
