from rest_framework import serializers

from .models import Employee, Report, Area, Coordinate, Department


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ("id", "name", )

class CoordinateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coordinate
        fields = ("name", "longitude", "latitude", )


class AreaSerializer(serializers.ModelSerializer):
    coordinates = CoordinateSerializer(Coordinate, many=True)
    class Meta:
        model = Area
        fields = ("name", "coordinates", )

    
class EmployeesSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(Department, many=False)
    class Meta:
        model = Employee
        fields = ("uuid", "department", "position", "first_name", "last_name", "middle_name", "passport_number", "passport_pinfl", "image", )


class EmployeeSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(Department, many=False)
    class Meta:
        model = Employee
        fields = ("department", "position", "first_name", "last_name", "middle_name", "passport_number", "passport_pinfl", "image", )


class CreateEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ("department", "position", "first_name", "last_name", "middle_name", "passport_number", "passport_pinfl", "image", )


class EditEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ("position", "first_name", "last_name", "middle_name", "passport_number", "passport_pinfl", )



class ReportSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer(Employee, many=False)
    area = AreaSerializer(Area, many=False)
    created = serializers.DateTimeField(format="%H:%M:%S")
    class Meta:
        model = Report
        fields = ("employee", "status", "image", "area", "created", )
