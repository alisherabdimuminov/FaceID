from django.contrib import admin

from .models import (
    Coordinate,
    Area,
    Employee,
    Report,
    Department,
)


@admin.register(Coordinate)
class CoordinateModelAdmin(admin.ModelAdmin):
    list_display = ["name", "longitude", "latitude", ]


@admin.register(Department)
class CoordinateModelAdmin(admin.ModelAdmin):
    list_display = ["name", ]


@admin.register(Area)
class AreaModelSerializer(admin.ModelAdmin):
    list_display = ["name",]


@admin.register(Employee)
class EmployeeModelAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "middle_name", ]
    
    fieldsets = (
        ("Ish ma'lumotlari", {
            "fields": ("department", "position", "specialist", "scientific_title", "academic_degree", )
        }),
        ("Shaxsiy ma'lumotlar", {
            "fields": ("first_name", "last_name", "middle_name", "gender", "nationality", "image", "birth_date", )
        }),
        ("Manzil", {
            "fields": ("state", "province", "district", "address", )
        }),
        ("Passport ma'lumotlari", {
            "fields": ("passport_number", "passport_pinfl", )
        }),
        ("Aloqa", {
            "fields": ("email", "phone", )
        }),
    )


@admin.register(Report)
class ReportModelAdmin(admin.ModelAdmin):
    list_display = ["status", "employee", "created"]
