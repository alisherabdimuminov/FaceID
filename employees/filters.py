from rest_framework.filters import BaseFilterBackend


class DateFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        day = request.GET.get("day")
        month = request.GET.get("month")
        year = request.GET.get("year")
        if day and month and year:
            return queryset.filter(created__day=day, created__month=month, created__year=year)
        return queryset
    

class WithDepartmentFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        department = request.GET.get("department")
        if department and department != "0":
            return queryset.filter(department__pk=department)
        return queryset
    
class WithEmployeeApplicationFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        employee = request.GET.get("employee")
        if employee:
            return queryset.filter(employee__uuid=employee)
        return queryset
