from typing import List

from django.urls import path


def get_urls(views) -> List[path]:
    return [
        path(
            'login/',
            views.JWTLoginAPIVIew.as_view(),
            name='api-jwt-login',
        ),
        path(
            'refresh_token/',
            views.JWTRefreshAPIVIew.as_view(),
            name='api-jwt-refresh',
        ),
        path(
            'logout/',
            views.JWTLogoutAPIVIew.as_view(),
            name='api-jwt-logout',
        ),
    ]
