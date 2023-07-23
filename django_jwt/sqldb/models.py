from django.conf import settings
from django.db import models


class RefreshToken(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='refresh_token',
    )
    token = models.CharField(max_length=200)

    class Meta:
        db_table = 'django_jwt_refreshtoken'

    def __str__(self):
        return f'{self.token}'
