from rest_framework import serializers

from .models import Employee, Report, Area, Coordinate, Department, Application


class ApplicationsSerializer(serializers.ModelSerializer):
    created = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S", required=False)
    class Meta:
        model = Application
        fields = ("employee", "name", "file", "description", "created", )

class DepartmentSerializer(serializers.ModelSerializer):
    employees = serializers.SerializerMethodField("count_employees")
    def count_employees(self, obj):
        return Employee.objects.filter(department=obj.pk).count()
    class Meta:
        model = Department
        fields = ("id", "name", "employees")

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
        fields = ("id", "uuid", "first_name", "last_name", "middle_name", "gender", "nationality", "birth_date", "passport_number", "passport_pinfl", "passport_of_issue", "image", "state", "province", "district", "address", "department", "position", "specialist", "scientific_title", "academic_degree", "phone" )


class EmployeeSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(Department, many=False)
    class Meta:
        model = Employee
        fields = ("id", "first_name", "last_name", "middle_name", "gender", "nationality", "birth_date", "passport_number", "passport_pinfl", "passport_of_issue", "image", "state", "province", "district", "address", "department", "position", "specialist", "scientific_title", "academic_degree", "phone")


class CreateEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ("first_name", "last_name", "middle_name", "gender", "nationality", "birth_date", "passport_number", "passport_pinfl", "passport_of_issue", "image", "state", "province", "district", "address", "department", "position", "specialist", "scientific_title", "academic_degree", "phone")


class EditEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ("first_name", "last_name", "middle_name", "gender", "nationality", "birth_date", "passport_number", "passport_pinfl", "passport_of_issue", "image", "state", "province", "district", "address", "position", "specialist", "scientific_title", "academic_degree", "phone" )



class ReportSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer(Employee, many=False)
    area = AreaSerializer(Area, many=False)
    created = serializers.DateTimeField(format="%H:%M:%S")
    class Meta:
        model = Report
        fields = ("employee", "status", "image", "area", "created", )


class EmployeeReportSerializer(serializers.ModelSerializer):
    attendance = serializers.SerializerMethodField("attendance_func")
    attendance_time = serializers.SerializerMethodField("attendance_time_func")
    attendance_area = serializers.SerializerMethodField("attendance_area_func")

    def attendance_func(self, obj):
        request = self.context.get("request")
        day = request.GET.get("day")
        month = request.GET.get("month")
        year = request.GET.get("year")
        report = Report.objects.filter(employee=obj.pk,created__day=day, created__month=month, created__year=year)
        if report:
            report = report.first()
            return report.status
        return "did_not_come"
    
    def attendance_time_func(self, obj):
        request = self.context.get("request")
        day = request.GET.get("day")
        month = request.GET.get("month")
        year = request.GET.get("year")
        report = Report.objects.filter(employee=obj.pk,created__day=day, created__month=month, created__year=year)
        if report:
            report = report.first()
            return report.created.strftime("%H:%M:%S")
        return None
    
    def attendance_area_func(self, obj):
        request = self.context.get("request")
        day = request.GET.get("day")
        month = request.GET.get("month")
        year = request.GET.get("year")
        report = Report.objects.filter(employee=obj.pk,created__day=day, created__month=month, created__year=year)
        if report:
            report = report.first()
            return report.area.name
        return None

    class Meta:
        model = Employee
        fields = ("id", "uuid", "first_name", "last_name", "phone", "attendance", "attendance_time", "attendance_area")
