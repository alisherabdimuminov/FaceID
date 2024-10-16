from uuid import uuid4
from django.db import models


REPORT_STATUS = (
    ("passed", "Passed"),
    ("failed", "Failed"),
)

class Coordinate(models.Model):
    name = models.CharField(max_length=100)
    longitude = models.CharField(max_length=20)
    latitude = models.CharField(max_length=20)

    def __str__(self) -> str:
        return self.name


class Area(models.Model):
    name = models.CharField(max_length=100)
    coordinates = models.ManyToManyField(Coordinate, related_name="area_coordinates")

    def __str__(self) -> str:
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name


class Employee(models.Model):
    uuid = models.CharField(default=uuid4, editable=False, max_length=100)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    position = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)
    passport_number = models.CharField(max_length=10)
    passport_pinfl = models.CharField(max_length=10)
    image = models.ImageField(upload_to="images/employees")

    def __str__(self) -> str:
        return self.first_name + " " + self.last_name


class Report(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=REPORT_STATUS)
    longitude = models.CharField(max_length=20)
    latitude = models.CharField(max_length=20)
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="images/reports")
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.status


# class Application(models.Model):
#     employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True)
#     name = models.CharField(max_length=100)
#     file = models.FileField()
#     description = models.TextField(null=True, blank=True)
#     created = models.DateTimeField(auto_now_add=True)
#     updated = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.name
