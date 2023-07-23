from django.conf import settings
from django_jwt.base.utils import return_extra_attrs_func


class SettingsInitializer:
    JWT_ACCESS_SECRET_KEY = settings.SECRET_KEY
    ACCESS_TOKEN_LIFETIME_SECONDS = 60 * 5
    JWT_REFRESH_SECRET_KEY = settings.SECRET_KEY
    REFRESH_TOKEN_LIFETIME_SECONDS = 60 * 60 * 24 * 7
    ALGORITHM = 'HS256'
    """ extra_attrs is a python path to func that needs to perform """
    EXTRA_ATTRS_FUNC = None

    def __init__(self, package_settings):
        if not package_settings:
            return
        for attr in dir(self)[:5]:
            if package_settings.get(attr):
                setattr(self, attr, package_settings.get(attr))
        if package_settings.get('EXTRA_ATTRS_FUNC'):
            self.EXTRA_ATTRS_FUNC = return_extra_attrs_func(self.EXTRA_ATTRS_FUNC)


package_settings = getattr(settings, 'DJANGO_JWT_SETTINGS', None)

DJANGO_JWT_SETTINGS = SettingsInitializer(package_settings)
