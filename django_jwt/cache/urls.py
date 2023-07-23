from django_jwt.base.urls import get_urls
from . import views

urlpatterns = get_urls(views)
