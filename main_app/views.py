from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models.functions import ExtractMonth
from django.db.models import Count
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from.models import Employee, Vacation, Absence, Department, Role, AbsenceChangeRequests
from .forms import EmployeeSignUpForm, LoginForm
import calendar

# Management
@login_required(login_url=('/login/'))
def index(request):
    
    deduction = None
    department = None


    if request.user.department and request.user.department.isdigit():
    
        department = Department.objects.get(pk = request.user.department)
    
    absences = Absence.objects.filter(employee_id = request.user.id, active=True)
    
    if department:
        deduction = request.user.salary - request.user.eligible_salary


    base_pay = department.salary

    additional_hours = request.user.additional_hours

    yearsOfExperienceCost = request.user.yearsOfExperienceCost
    
    pending_vacations = request.user.vacation_set.filter(status='Pending').count()
    accepted_vacations = request.user.vacation_set.filter(status='Accepted').count()
    rejected_vacations = request.user.vacation_set.filter(status='Rejected').count()
    
    excused_absences = absences.filter(excused=True).count()
    unexcused_absences = absences.filter(excused=False).count()
    
    absences_by_month = (
        Absence.objects
        .filter(employee_id=request.user.id)
        .annotate(month=ExtractMonth('date'))
        .values('month')
        .annotate(total=Count('id'))
        .order_by('month')
    )
    
    months = [absence['month'] for absence in absences_by_month]
    totals = [absence['total'] for absence in absences_by_month]

    context = {
        'user' : request.user,
        'absences_count' : len(absences),
        'deduction' : deduction,
        'department_name' : department.department,
        'role_name' : department.role.role,
        "additionals" : (request.user.yearsOfExperienceCost if request.user.yearsOfExperienceCost is not None else 0) + (request.user.additional_hours if request.user.additional_hours is not None else 0),
        "base_pay" : department.salary,
        "pending_vacations" : pending_vacations,
        "accepted_vacations" : accepted_vacations,
        "rejected_vacations" : rejected_vacations,
        "excused_absences" : excused_absences,
        "unexcused_absences" : unexcused_absences,
        'months': months,
        'totals': totals,
        
    }
    return render(request,'main/index.html',context)

# ------------------------------------------------------------------------------------------------

@login_required(login_url=('/login/'))
def vacation(request):
    user = request.user
    vacations = Vacation.objects.filter(employee = user)
    
    if request.method == 'POST':
        vac_id = request.POST.get('vac_id')
        if vac_id:
            adv = get_object_or_404(Vacation, id=vac_id)

            adv.start_date = request.POST.get('start_date', adv.start_date) if request.POST.get('start_date') else adv.start_date
            adv.end_date = request.POST.get('end_date', adv.end_date) if request.POST.get('end_date') else adv.end_date
            adv.vacation_type = request.POST.get('vacation_type', adv.vacation_type) if request.POST.get('vacation_type') else adv.vacation_type
            adv.save()
    
    context = {
        'vacations' : vacations,
    }

    return render(request,'main/vacation.html',context)


@login_required(login_url=('/login/'))
def add_vacation(request):

    if request.method == 'POST':

        # Get The Data
        adv_start_date = request.POST.get('start_date')
        adv_end_date = request.POST.get('end_date')
        adv_type = request.POST.get('vacation_type') 


        vac = Vacation.objects.create(
            employee = request.user,
            start_date = adv_start_date,
            end_date = adv_end_date,
            vacation_type = adv_type
        )
        
        vac.save()
        return redirect('vacations')
    return render(request)


@login_required(login_url=('/login/'))
def absence_change_request(request):
    user = request.user
    absences = Absence.objects.filter(employee = user, excused = False)
    absence_change_requests = AbsenceChangeRequests.objects.filter(employee=user)
    
    if request.method == 'POST':
        abs_id = request.POST.get('abs_id')
        if abs_id:
            abs = get_object_or_404(AbsenceChangeRequests, id=abs_id)

            abs.absence = Absence.objects.get(id = request.POST.get('absence', abs.absence.id)) if request.POST.get('absence') else abs.absence
            abs.request_reason = request.POST.get('absence_request_reason', abs.request_reason) if request.POST.get('absence_request_reason') else abs.request_reason
            abs.save()
    
    context = {
        'absences' : absences,
        'absence_change_requests' : absence_change_requests
    }

    return render(request,'main/absence_change_request.html',context)


@login_required(login_url=('/login/'))
def add_absence_change_request(request):

    if request.method == 'POST':

        # Get The Data
        abs_request_absence = request.POST.get('absence')
        absence_request_reason = request.POST.get('absence_request_reason') 


        abs = AbsenceChangeRequests.objects.create(
            employee = request.user,
            absence = Absence.objects.get(id = abs_request_absence),
            request_reason = absence_request_reason,
        )
        
        abs.save()
        return redirect('absence_change_request')
    return render(request)

@login_required(login_url=('/login/'))
def absence(request) :
    absences = Absence.objects.filter(employee = request.user)
    context = {
        'absences' : absences
    }
    return render(request, 'main/absence.html', context)

#-------------------------------------------------------------------------------
# Auth

def login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = auth.authenticate(request, email=email, password=password)
            if user is not None:
                auth.login(request, user)
                messages.success(request, 'You have signed in successfully!')
                return redirect('index')
            else:
                
                messages.error(request, 'Invalid credentials.')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field} : {error}')
    else:
        form = LoginForm()

    context = {'form': form}
    return render(request, 'main/login.html', context)

@login_required(login_url=('/login/'))
def logout(request):
    auth.logout(request)
    messages.success(request, "You've Signed Out !")
    return redirect('index')

def signup(request):
    departements = Department.objects.all()
    roles = Role.objects.all()
    if request.method == 'POST':
        form = EmployeeSignUpForm(request.POST, request.FILES)
        if form.is_valid():
            
            employee = Employee(
                first_name=form.cleaned_data.get('first_name'),
                last_name=form.cleaned_data.get('last_name'),
                email=form.cleaned_data.get('email'),
                birthdate=form.cleaned_data.get('birthdate'),
                joining_date=form.cleaned_data.get('joining_date'),
                phone=form.cleaned_data.get('phone'),
                country=form.cleaned_data.get('country'),
                department=form.cleaned_data.get('department'),
                role=form.cleaned_data.get('role'),
                years_of_exp=form.cleaned_data.get('years_of_exp'),
                pic = form.cleaned_data.get('pic'),
                overtime_hours = form.cleaned_data.get('overtime_hours')
            )

            print(employee.role)
            if Department.objects.filter(role_id=employee.role).first().role.role == 'Teaching':

                employee.teach_course = form.cleaned_data.get('teach_course')
                employee.hours_worked_per_week = form.cleaned_data.get('hours_worked_per_week')
            
            
            employee.set_password(form.cleaned_data.get('password1'))
            
            employee.save()  

            
            auth.login(request, employee, backend='django.contrib.auth.backends.ModelBackend')

            
            messages.success(request, "Signed Up Successfully!")
            return redirect('index')  

        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
            return render(request, 'main/signup.html', {'form': form , 'departments' : departements, 'roles' : roles})

    else:
       
        form = EmployeeSignUpForm()

    
    return render(request, 'main/signup.html', {'form': form , 'departments' : departements, 'roles' : roles})


def get_departments_for_role(request, role_id):
    departments = list(Department.objects.filter(role_id=role_id).values('id', 'department'))
    return JsonResponse(departments, safe=False)

def get_department_weekly_hours(request, department_id):
    try:
        department = Department.objects.get(pk = department_id)
        return JsonResponse(department.weekly_hours, safe=False)
    
    except Exception as e:
        return JsonResponse({'error': e}, status=404)

    