from rest_framework import generics
from django.http import HttpRequest
from rest_framework import decorators
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from .models import Employee, Report, Department
from .serializers import (
    EmployeesSerializer, 
    CreateEmployeeSerializer, 
    EmployeeSerializer, 
    ReportSerializer, 
    DepartmentSerializer,
    EditEmployeeSerializer,
)
from .filters import DateFilterBackend, WithDepartmentFilterBackend


# Departments

class DepartmentsListAPIView(generics.ListAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


# Add department

@decorators.api_view(http_method_names=["POST"])
def add_department(request: HttpRequest):
    print(request.data)
    name = request.data.get("name")
    if not name:
        return Response({
            "status": "error",
            "code": "400",
            "data": None
        })
    department = Department.objects.create(name=name)
    return Response({
        "status": "success",
        "code": "201",
        "data": None
    })


# Edit department

@decorators.api_view(http_method_names=["POST"])
def edit_department(request: HttpRequest, id: int):
    print(request.data)
    name = request.data.get("name")
    department = Department.objects.filter(id=id)
    if not department:
        return Response({
            "status": "error",
            "code": "404",
            "data": None
        })
    department = department.first()
    department.name = name
    department.save()
    return Response({
        "status": "success",
        "code": "201",
        "data": None
    })


# Delete department

@decorators.api_view(http_method_names=["POST"])
def delete_department(request: HttpRequest, id: int):
    print(request.data)
    department = Department.objects.filter(id=id)
    if not department:
        return Response({
            "status": "error",
            "code": "404",
            "data": None
        })
    department = department.first()
    department.delete()
    return Response({
        "status": "success",
        "code": "201",
        "data": None
    })


# Employees

class EmployeeListAPIView(generics.ListAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeesSerializer
    filter_backends = [WithDepartmentFilterBackend, ]
    


# Employee

class EmployeeRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    lookup_field = "uuid"


# Edit employee

@decorators.api_view(http_method_names=["POST"])
def edit_employee(request: HttpRequest, uuid: str):
    employee_obj = get_object_or_404(Employee, uuid=uuid)
    employee = EditEmployeeSerializer(employee_obj, data=request.data)
    if (employee.is_valid()):
        employee.save()
        return Response({
            "status": "success",
            "code": "200",
            "data": None
        })
    return Response({
        "status": "error",
        "code": "400",
        "data": None,
    })


# Create employee

@decorators.api_view(http_method_names=["POST"])
def create_employee(request: HttpRequest):
    employee = CreateEmployeeSerializer(Employee, data=request.data)
    if (employee.is_valid()):
        employee.create(employee.validated_data)
        return Response({
            "status": "success",
            "code": "201",
            "data": None
        })
    print(request.data)
    print(employee.errors)
    return Response({
        "status": "error",
        "code": "400",
        "data": None
    })


# Delete employee

@decorators.api_view(http_method_names=["POST"])
def delete_employee(request: HttpRequest, uuid: str):
    employee = Employee.objects.filter(uuid=uuid)
    if not employee:
        return Response({
            "status": "error",
            "code": "404",
            "data": None,
        })
    employee = employee.first()
    employee.delete()
    return Response({
        "status": "success",
        "code": "200",
        "data": None
    })


# Reports

class ReportsListAPIView(generics.ListAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    filter_backends = [DateFilterBackend]
    filterset_fields = ["created"]


# Report

class ReportRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    lookup_field = "pk"
