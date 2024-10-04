import base64
import re
from deepface import DeepFace
from shapely.geometry import Polygon, Point

from django.http import HttpRequest
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.core.files.base import ContentFile

from employees.models import Area, Report, Employee


@api_view(http_method_names=["POST"])
def check_location(request: HttpRequest):
    latitude = request.data.get("latitude")
    longitude = request.data.get("longitude")
    print(latitude)
    print(longitude)
    areas = Area.objects.all()
    for area in areas:
        coordinates = []
        for coord in area.coordinates.all():
            coordinates.append((coord.longitude, coord.latitude))
        polygon = Polygon(coordinates)
        point = Point((longitude, latitude))
        point2 = Point((66.922896, 39.672432))
        point_in_the_area = polygon.contains(point)
        point_in_the_area2 = polygon.contains(point2)
        print(polygon)
        print(point)
        print(point_in_the_area)
        print(point_in_the_area2)
        if point_in_the_area:
            return Response({
                "status": "success",
                "code": "1",
                "data": {
                    "area": area.pk,
                    "comment": f"Siz {area.name} dasiz!"

                }
            })
    return Response({
        "status": "success",
        "code": "0",
        "data": {
            "area": 0,
            "comment": "Siz institut hududida emassiz!"
        }
    })


@api_view(http_method_names=["POST"])
def faceid(request: HttpRequest):
    base64data = request.data.get("image")
    passport = request.data.get("passport")
    passport_series, passport_number, _ = re.split("(\d+)", passport)
    employee = Employee.objects.filter(passport_series=passport_series, passport_number=passport_number)
    format, imgstr = base64data.split(';base64,')
    ext = format.split('/')[-1]
    base64image = ContentFile(base64.b64decode(imgstr), name=f"taken.{ext}")
    if employee:
        employee = employee.first()
        report = Report.objects.create(
            employee=employee,
            image=base64image,
            longitude="12",
            latitude="234",
            area=Area.objects.first(),
        )
        result = DeepFace.verify(
            img1_path=employee.image.path,
            img2_path=report.image.path
        )
        if result.get("verified"):
            report.status = "passed"
            report.save()
        else:
            report.status = "failed"
            report.save()
        return Response({
            "status": "success",
            "code": "0",
            "data": {
                "verified": result.get("verified"),
            }
        })
    return Response


@api_view(http_method_names=["POST"])
def get_employee_with_passport(request: HttpRequest):
    passport = request.data.get("passport")
    passport_series, passport_number, _ = re.split("(\d+)", passport)
    employee = Employee.objects.filter(passport_series=passport_series, passport_number=passport_number)
    if (employee):
        employee = employee.first()
        return Response({
            "status": "success",
            "code": "1",
            "data": {
                "user_id": employee.pk
            }
        })
    return Response({
        "status": "success",
        "code": "0",
        "data": None
    })
