from django.urls import path

from .views import (
    EmployeeListAPIView,
    EmployeeRetrieveAPIView,
    edit_employee,
    create_employee,
    delete_employee,

    ReportsListAPIView,
    ReportRetrieveAPIView,

    DepartmentsListAPIView,
    add_department,
    edit_department,
    delete_department,
)


urlpatterns = [
    path("employees/", EmployeeListAPIView.as_view(), name="employees"),
    path("employees/employee/<str:uuid>/", EmployeeRetrieveAPIView.as_view(), name="employee"),
    path("employees/employee/<str:uuid>/edit/", edit_employee, name="edit_employee"),
    path("employees/employee/<str:uuid>/delete/", delete_employee, name="delete_employee"),
    path("employees/create/", create_employee, name="create_employee"),

    path("reports/", ReportsListAPIView.as_view(), name="reports"),
    path("reports/report/<int:pk>/", ReportRetrieveAPIView.as_view(), name="report"),

    path("departments/", DepartmentsListAPIView.as_view(), name="departments"),
    path("departments/create/", add_department, name="add_department"),
    path("departments/department/<int:id>/edit/", edit_department, name="edit_department"),
    path("departments/department/<int:id>/delete/", delete_department, name="delete_department"),
]

