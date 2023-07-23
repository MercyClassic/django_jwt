from .models import RefreshToken
from django_jwt.base.service import BaseTokenActions


class JWTSqlDB(BaseTokenActions):
    def save_refresh_token(self, user_id: int, token: str) -> None:
        RefreshToken.objects.create(user_id=user_id, token=token)

    def delete_refresh_token(self, user_id: int, token: str) -> None:
        count_deleted_objects = RefreshToken.objects.filter(token=token).delete()
        """ IF NO TOKEN, THAT MEAN TOKEN WAS DELETED EARLY, MOST LIKELY BY HACKER """
        if count_deleted_objects == 0:
            RefreshToken.objects.filter(user_id=user_id).delete()
