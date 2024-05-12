from django.core.management import BaseCommand
from ...models import Employee, Department, Absence

def put_absences_inactive():
    for absence in Absence.objects.all():
        absence.active = False
        absence.save()
    
    
class Command(BaseCommand):
    
    help = 'Resets employees salaries'
    
    def handle(self, *args, **options):
        employees = Employee.objects.all()
        
        for employee in employees:
            
            if employee.department:
                
                department = employee.department
                
                if employee.department.isdigit():
                    
                    department = Department.objects.get(pk = employee.department)
                    if department.add_experience_and_overtime and department.year_of_experience_cost:
                        
                        employee.yearsOfExperienceCost = department.year_of_experience_cost * employee.years_of_exp
                        employee.salary = department.salary + employee.yearsOfExperienceCost
                        
                        try:
                            if Department.objects.filter(role_id=employee.role).first().role.role == 'Teaching' :
                                print(employee.hours_worked_per_week)
                                employee.additional_hours = employee.hours_worked_per_week * department.hour_rate * 4
                                
                                employee.salary += employee.additional_hours
                        except Exception as e:
                            print(f'Something went wrong while reseting {employee}' + str(e))
                            
                    else:
                        employee.salary = Department.objects.get(pk = employee.department).salary
                    
                    employee.eligible_salary = employee.salary
                        
                    employee.save()
                    
                    put_absences_inactive()
    

