from django.urls import path
from . import views

urlpatterns = [

    path("dashboard/", views.dashboard, name="dashboard"),

    path(
        "department/<int:dept_id>/",
        views.department_employees,
        name="department_employees"
    ),

    path(
        "apply-leave/",
        views.apply_leave,
        name="apply_leave"
    ),
    
    path("leaves/", views.leave_requests, name="leave_requests"),

    path(
        "leave/<int:leave_id>/<str:status>/",
        views.update_leave_status,
        name="update_leave_status"
    ),

    path(
        "emp-dashboard",
        views.emp_dashboard,
        name="emp_dashboard"
    ),
]

