# Django Wafris

## Installation

1. Install `django-wafris` package

```terminal
pip install django-wafris
```

2. Add `INSTALLED_APP` in `settings.py`

```python
INSTALLED_APPS = [
    ...
    "django.contrib.staticfiles",
    "django_wafris",
]
```

3. Add `MIDDLEWARE` in `settings.py`

```python
MIDDLEWARE = [
    "django_wafris.middleware.WafrisMiddleware",
    "django.middleware.security.SecurityMiddleware",
    ...
]
```

4. Declare WAFRIS config in `settings.py`

```python

WAFRIS = {
    "REDIS_URL": "redis://:password@host:port",
}
```


## Example

[wafrisdemo](https://github.com/bkayranci/django-wafris/tree/main/wafrisdemo)

You are able to run a example django app.