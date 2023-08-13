from http.cookies import SimpleCookie

from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from django_jwt.base.jwt import generate_jwt
from django_jwt.sqldb.models import RefreshToken
from .models import AuthUser


class JWTTests(APITestCase):
    def setUp(self) -> None:
        self.user = AuthUser.objects.create_user(
            username='test',
            password='test',
        )

    def parametrized_login(
            self,
            data: dict,
            status_code: int,
            with_token_data: bool,
    ) -> bool:
        response = self.client.post(path=reverse('api-jwt-login'), data=data)
        assert bool(response.cookies.get('refresh_token')) is with_token_data
        assert bool(response.data.get('access_token')) is with_token_data
        return response.status_code == status_code

    def test_login(self):
        assert self.parametrized_login(
            data={
                'username_field': 'wrong username',
                'password': 'test',
            },
            status_code=404,
            with_token_data=False,
        )
        assert self.parametrized_login(
            data={
                'username_field': 'test',
                'password': 'wrong password',
            },
            status_code=401,
            with_token_data=False,
        )
        """ ALL DATA IS VALID """
        assert self.parametrized_login(
            data={
                'username_field': 'test',
                'password': 'test',
            },
            status_code=200,
            with_token_data=True,
        )

    def test_logout(self):
        self.client.cookies = SimpleCookie({'refresh_token': 'Wrong Token'})
        response = self.client.post(reverse('api-jwt-logout'))
        assert response.json() == {'detail': 'Could not validate credentials'}
        assert response.status_code == 401

        generated_jwt = generate_jwt(data={'user_id': 1}, lifetime_seconds=60, secret='JWT')
        RefreshToken.objects.create(user_id=1, token=generated_jwt)

        self.client.cookies = SimpleCookie({'refresh_token': generated_jwt})
        response = self.client.post(reverse('api-jwt-logout'))
        assert response.status_code == 200
        assert not self.client.cookies.get('refresh_token').get('_value')

    def test_refresh_access_token(self):
        self.client.cookies = SimpleCookie({'refresh_token': 'Wrong Token'})
        response = self.client.post(reverse('api-jwt-logout'))
        assert response.json() == {'detail': 'Could not validate credentials'}
        assert response.status_code == 401

        generated_jwt = generate_jwt(data={'user_id': 1}, lifetime_seconds=60, secret='JWT')
        RefreshToken.objects.create(user_id=1, token=generated_jwt)

        self.client.cookies = SimpleCookie({'refresh_token': generated_jwt})
        response = self.client.post(reverse('api-jwt-logout'))
        assert response.status_code == 200
        assert self.client.cookies.get('refresh_token') == response.cookies.get('refresh_token')

    def test_auth_backend(self):
        response = self.client.get(reverse('api-test-auth-backend'))
        assert response.status_code == 401

        generated_jwt = generate_jwt(data={'user_id': 1}, lifetime_seconds=60, secret='JWT')
        RefreshToken.objects.create(user_id=1, token=generated_jwt)

        response = self.client.get(
            reverse('api-test-auth-backend'),
            headers={'Authorization': generated_jwt}
        )
        assert response.status_code == 200
