from django.urls import path, include

from users.views import login
from .views import check_location, check_passport, faceid


urlpatterns = [
    path("", include("employees.urls")),
    path("auth/login/", login, name="login"),
    path("location/", check_location, name="location"),
    path("passport/", check_passport, name="passport"),
    path("faceid/", faceid, name="faceid"),
]
