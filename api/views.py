import base64
from datetime import datetime
from shapely.geometry import Polygon, Point
from deepface import DeepFace

from django.http import HttpRequest
from rest_framework import decorators
from rest_framework.response import Response
from django.core.files.base import ContentFile

from employees.models import Area, Employee, Report



@decorators.api_view(http_method_names=["POST"])
def check_location(request: HttpRequest):
    longitude = request.data.get("longitude")
    latitude = request.data.get("latitude")
    print("logitude:", longitude)
    print("latitude:", latitude)

    areas = Area.objects.all()
    print(areas)
    for area in areas:
        coordinates = []
        for coord in area.coordinates.all():
            coordinates.append((coord.longitude, coord.latitude))
        polygon = Polygon(coordinates)
        point = Point((longitude, latitude))
        point_in_the_area = polygon.contains(point)
        print(polygon)
        print(point)
        print(point_in_the_area)
        if (point_in_the_area):
            return Response({
                "status": "success",
                "code": "200",
                "data": area.pk
            })
    return Response({
        "status": "error",
        "code": "404",
        "data": None
    })


@decorators.api_view(http_method_names=["POST"])
def check_passport(request: HttpRequest):
    passport = request.data.get("passport")
    employee = Employee.objects.filter(passport_number=passport)
    if employee:
        employee = employee.first()
        return Response({
            "status": "success",
            "code": "200",
            "data": employee.pk
        })
    return Response({
        "status": "error",
        "code": "404",
        "data": None
    })


@decorators.api_view(http_method_names=["POST"])
def faceid(request: HttpRequest):
    now = datetime.now()
    base64data = request.data.get("image")
    passport = request.data.get("passport")
    employee = Employee.objects.filter(passport_number=passport)
    format, imgstr = base64data.split(';base64,')
    ext = format.split('/')[-1]
    base64image = ContentFile(base64.b64decode(imgstr), name=f"taken.{ext}")
    print(employee)
    print(request.data)
    if employee:
        employee = employee.first()
        report = Report.objects.filter(employee=employee.pk, created=now)
        print(report)
        if report:
            return Response({
                "status": "error",
                "code": "201",
                "data": None
            })
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
        print(result)
        if result.get("verified"):
            report.status = "passed"
            report.save()
        else:
            report.status = "failed"
            report.save()
        return Response({
            "status": "success",
            "code": "200",
            "data": result.get("verified")
        })
    return Response({
        "status": "error",
        "code": "404",
        "data": None
    })