from typing import Iterable
from django.db import models
from django_countries.fields import CountryField
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected')
    ]

VACATION_TYPES = [
    ('Business','Business'),
    ('Death','Death'),
    ('Birth','Birth')
]


from django.contrib.auth.base_user import BaseUserManager


class EmployeeManager(BaseUserManager):
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, password, **extra_fields)

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

class Employee(AbstractUser):
    
    employee_generated_id = models.CharField(max_length= 155,null = True)
    birthdate = models.DateField(null = True)
    pic = models.ImageField(upload_to='Imgs/Profile_Pics',null = True, blank=True)
    joining_date = models.DateField(null = True)
    phone = models.IntegerField(null = True)
    email = models.EmailField(_('email address'), unique=True)
    country = CountryField(blank_label='(select country)', null = True)

    department = models.CharField(max_length=100, null = True)
    role = models.CharField(max_length=100, null = True)
    years_of_exp = models.IntegerField(null = True)

    eligible_salary = models.PositiveIntegerField(null=True, blank=True)
    salary = models.PositiveIntegerField(null=True, blank=True)
    additional_hours = models.PositiveIntegerField(null=True, blank=True)
    yearsOfExperienceCost = models.PositiveIntegerField(null=True, blank=True)

    teach_course = models.CharField(max_length=100, null = True, blank = True)
    hours_worked_per_week = models.IntegerField(null = True, blank = True)

    overtime_hours = models.IntegerField(null = True, blank = True)

    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = EmployeeManager()

    def save(self, ignore_salaries_eq=False, *args, **kwargs):
        
        if not self.pk:  
        
            email_prefix = self.email.split('@')[0]
            self.employee_generated_id = email_prefix
            
            department = Department.objects.get(pk = self.department)
            if department.add_experience_and_overtime and department.year_of_experience_cost:
                
                self.yearsOfExperienceCost = department.year_of_experience_cost * self.years_of_exp
                self.salary = department.salary + self.yearsOfExperienceCost
                if Department.objects.filter(role_id=self.role).first().role.role == 'Teaching' :
                    if self.overtime_hours:
                        self.additional_hours = self.hours_worked_per_week * department.hour_rate * 4 + self.overtime_hours * department.hour_rate * 1.5
                    else :
                        self.additional_hours = self.hours_worked_per_week * department.hour_rate * 4
                    self.salary += self.additional_hours
            else:
                self.salary = Department.objects.get(pk = self.department).salary
        
        if not ignore_salaries_eq:
            self.eligible_salary = self.salary
            
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email
    



class Vacation(models.Model):
    
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    vacation_type = models.CharField(max_length=100, choices = VACATION_TYPES)
    status = models.CharField(max_length = 15, default='Pending' , choices = STATUS_CHOICES)
    
    def __str__(self):
        return f'{self.employee.email}, type : {self.vacation_type} with status : {self.status}'  





class Absence(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    reason = models.TextField()
    date = models.DateField()
    excused = models.BooleanField(default=False)
    active = models.BooleanField(default=True, blank=True, help_text='Keep active to deduct.')

    def save(self, *args, **kwargs):
            
            if self.active:
                
                day_cost = self.employee.salary / 22
                
                if not self.excused:
                    global unexcused_absence_count
                    unexcused_absence_count = Absence.objects.filter(employee=self.employee, active = True, excused=False).count()
                    print(unexcused_absence_count)
                    if unexcused_absence_count > 15:
                        self.employee.eligible_salary = 0
                        self.employee.is_active = False # to permenantly restrict his account as his services are no longer needed
                    
                    else :
                        global deduction
                        deduction = (unexcused_absence_count + 2) * day_cost
                        
                        self.employee.eligible_salary -= deduction
                        if self.employee.eligible_salary < 0 :
                            self.employee.eligible_salary = 0

                else :
                    excused_days = Absence.objects.filter(employee=self.employee, excused=True, active=True).count()

                    try :
                        if deduction :
                            self.employee.eligible_salary += deduction + 1
                            if excused_days + 2 > 30:
                                deduct_percentage = 25
                                self.employee.eligible_salary -= self.employee.salary * deduct_percentage / 100
                            
                    except:
                        if excused_days + 1 > 30:
                            deduct_percentage = 25
                            self.employee.eligible_salary -= self.employee.salary * deduct_percentage / 100
                        
                    
            self.employee.save(ignore_salaries_eq=True)
            
            super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.employee.email}, date : {self.date} and excused status is {self.excused}' 


class AbsenceChangeRequests(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    absence = models.ForeignKey(Absence, on_delete = models.CASCADE)
    request_reason = models.TextField()
    status = models.CharField(max_length=25, choices=STATUS_CHOICES, default="Pending")

    def __str__(self):
        return f"{self.employee} wants to exuse absence #{self.absence.id}, current status is {self.status}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        if self.status == "Accepted":
            absence = self.absence
            if not absence.excused:
                absence.excused = True
                absence.save()


class Role(models.Model) :
    role = models.CharField(max_length = 220)

    def __str__(self):
        return self.role

class Department(models.Model) :
    role = models.ForeignKey(Role, on_delete = models.CASCADE)
    department = models.CharField(max_length = 220)
    salary = models.PositiveIntegerField()
    weekly_hours = models.PositiveIntegerField(null=True)
    year_of_experience_cost = models.PositiveIntegerField(null=True)
    hour_rate = models.PositiveIntegerField(null=True)
    add_experience_and_overtime = models.BooleanField(default=True, null=True, blank=True)
    def save(self, *args, **kwargs):
        if not self.pk:
            self.salary_after_deduction = self.salary
            
        super().save(*args, **kwargs)

    def __str__(self):
        return self.department