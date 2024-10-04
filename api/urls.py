from django.urls import path

from .views import faceid, check_location, get_employee_with_passport


urlpatterns = [
    path("faceid/", faceid, name="faceid"),
    path("location/", check_location, name="location"),
    path("passport/", get_employee_with_passport, name="passport"),
]
