from django.db import models


STATUS = (
    ("passed", "Passed"),
    ("failed", "Failed"),
)


class Coordinate(models.Model):
    name = models.CharField(max_length=100)
    longitude = models.CharField(max_length=20)
    latitude = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Area(models.Model):
    name = models.CharField(max_length=100)
    coordinates = models.ManyToManyField(Coordinate, related_name="area_coordinates")

    def __str__(self):
        return self.name
    
class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Employee(models.Model):
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    position = models.CharField(max_length=100)
    passport_series = models.CharField(max_length=2)
    passport_number = models.CharField(max_length=7)
    passport_pinfl = models.CharField(max_length=14)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="employees/images")

    def __str__(self):
        return self.first_name + " " + self.last_name


class Report(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=20, choices=STATUS)
    image = models.ImageField(upload_to="reports/images")
    longitude = models.CharField(max_length=20)
    latitude = models.CharField(max_length=20)
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.employee.__str__()
