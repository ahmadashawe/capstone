from django.urls import path
from . import views

urlpatterns = [

    # Auth
    path('login/' ,views.login ,name='login'),
    path('logout/' ,views.logout ,name='logout'),
    path('signup/' ,views.signup ,name='signup'),
    path('ajax/get_departments/<int:role_id>/', views.get_departments_for_role, name='ajax_get_departments'),
    path('ajax/get_department/<int:department_id>/', views.get_department_weekly_hours, name='ajax_get_department'),

    # Managements
    path('' ,views.index ,name='index'),

    path('vacation/' ,views.vacation ,name='vacations'),
    path('add-vacation/' ,views.add_vacation ,name='add_vacation'),


    path('absences-change-request/' ,views.absence_change_request ,name='absence_change_request'),
    path('add-absence-change-request/' ,views.add_absence_change_request ,name='add_absence_change_request'),
    path('absences/' ,views.absence ,name='absences'),

]