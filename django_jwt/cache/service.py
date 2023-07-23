from django_jwt.base.service import BaseTokenActions
from django.core.cache import cache


class JWTCached(BaseTokenActions):
    def save_refresh_token(self, user_id: int, token: str) -> None:
        cache.set(f'{user_id},{token}', True)

    def delete_refresh_token(self, user_id: int, token: str) -> None:
        key = cache.get(f'{user_id},{token}')
        cache.delete(f'{user_id},{token}')
        """ IF NO TOKEN, THAT MEAN TOKEN WAS DELETED EARLY, MOST LIKELY BY HACKER """
        if not key:
            user_tokens = cache.keys(f'*{user_id},*')
            for token in user_tokens:
                cache.delete(token)
