from django.contrib import admin

from .models import Employee, Report, Area, Coordinate, Department


@admin.register(Employee)
class EmplooyeModelAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "passport_series", "passport_number"]


@admin.register(Report)
class ReportModelAdmin(admin.ModelAdmin):
    list_display = ["employee", "status", "area", "created", ]


@admin.register(Area)
class AreaModelAdmin(admin.ModelAdmin):
    list_display = ["name", ]


@admin.register(Coordinate)
class CoordinateModelAdmin(admin.ModelAdmin):
    list_display = ["name", "longitude", "latitude", ]


@admin.register(Department)
class DepartmentModelAdmin(admin.ModelAdmin):
    list_display = ["name", ]

