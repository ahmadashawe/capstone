from django.contrib import admin
from .models import Employee,Absence,Vacation,Role,Department, AbsenceChangeRequests

class AbsenceAdmin(admin.ModelAdmin):
    search_fields = ['employee__email', 'employee__first_name', 'employee__last_name','reason']

class RoleAdmin(admin.ModelAdmin):
    search_fields = ['role']

class DepartmentAdmin(admin.ModelAdmin):
    search_fields = ['role__role','department','salary','weekly_hours','year_of_experience_cost','hour_rate']

class VacationAdmin(admin.ModelAdmin):
    search_fields = ['employee__email', 'employee__first_name', 'employee__last_name', 'vacation_type', 'status']

class AbsenceChangeRequestsAdmin(admin.ModelAdmin):
    search_fields = ['absence__employee__email', 'absence__employee__first_name', 'absence__employee__last_name', 'status', 'absence__id']

admin.site.register(Absence, AbsenceAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Vacation, VacationAdmin)
admin.site.register(AbsenceChangeRequests, AbsenceChangeRequestsAdmin)

class EmployeeAdmin(admin.ModelAdmin):
    search_fields = ['email', 'employee_generated_id', 'first_name', 'last_name']
    help_texts = {
        'name': ('Enter the full name of the employee.'),
    }
admin.site.register(Employee, EmployeeAdmin)
