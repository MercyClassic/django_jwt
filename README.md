**<h1> Django JWT Authorization </h1>**
**<h2> This package provides:</h2>**
- **<h3> Authentication backend </h3>**
- **<h3> Storing refresh token in sql database / cache </h3>**

**<h2> Requirements </h2>**
- **<h3> Django </h3>**
- **<h3> Django Rest Framework </h3>**
- **<h3> PyJWT </h3>**

**<h2> Installation </h2>**
```
pip install git+https://github.com/MercyClassic/django_jwt.git
```
or if you using poetry
```
poetry add git+https://github.com/MercyClassic/django_jwt.git
```
**<h2> Set up </h2>**
**<h3> If you want to store refresh token in db: </h3>**
`settings.py`
```python
INSTALLED_APPS = (
    ...
    'django_jwt.sqldb',
    ...
)
```
`urls.py`
```
urlpatterns += [path('auth/', include('django_jwt.sqldb.urls'))]
```
**<h3> If you want to store refresh token in cache: </h3>**
`settings.py`
```python
INSTALLED_APPS = (
    ...
    'django_jwt.cache',
    ...
)
```
`urls.py`
```
urlpatterns += [path('auth/', include('django_jwt.cache.urls'))]
```
**<h3> Note </h3>**
    **<h4> You should choose only one app </h4>**
    **<h4> If you choose *sqldb* storage, do not forget `python manage.py makemigrations sqldb` </h4>**
    **<h4> If you choose *cache* storage, do not forget define django CACHES settings </h4>**
    **<h4> Right now package provides only REDIS cache, django cache settings example: </h4>**
```python
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'cache://127.0.0.1:6379/0',
    },
}
```
```python
REST_FRAMEWORK = {
    ...
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'django_jwt.JWTAuthenticateBackend',
    ],
    ...
}
```
**<h3> Django JWT Settings </h3>**
```python
DJANGO_JWT_SETTINGS = {
    'JWT_ACCESS_SECRET_KEY': SECRET_KEY,
    'ACCESS_TOKEN_LIFETIME_SECONDS':  60 * 5,
    'JWT_REFRESH_SECRET_KEY': SECRET_KEY,
    'REFRESH_TOKEN_LIFETIME_SECONDS': 60 * 60 * 24 * 7,
    'ALGORITHM': 'HS256',
    'EXTRA_ATTRS_FUNC': None,
}
```

**<h3> The most interesting attribute is `EXTRA_ATTRS_FUNC` </h3>**
**<h4> This attribute allows you to add extra data in request.user (dict) </h4>**
**<h4> You need to make function that returns dict with extra data </h4>**
**<h4> Then you need to pass module and func name to the `EXTRA_ATTRS_FUNC` like this: </h4>**
```python
DJANGO_JWT_SETTINGS = {
    ...
    'EXTRA_ATTRS_FUNC': {'module': 'python.path.to.module', 'func_name': 'func_name'}
    ...
}
```
**<h2> I'm glad you're using my jwt auth package! :) </h2>**
