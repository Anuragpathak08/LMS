from django.shortcuts import render, get_object_or_404, redirect
from account.models import Department, User
from .models import LeaveRequest
from .forms import LeaveRequestForm
from django.contrib.auth.decorators import login_required ,  user_passes_test


#utility function
def isadmin(user):
    return user.is_superuser


# Create your views here.
@login_required(login_url='login')
@user_passes_test(isadmin, login_url='apply_leave')
def dashboard(request):
    departments = Department.objects.all()
    context = {
        "departments": departments
    }
    print(departments)
    return render(request, "dashboard.html", context)



@login_required(login_url='login')
@user_passes_test(isadmin)
def department_employees(request, dept_id):
    department = get_object_or_404(Department, id=dept_id)
    employees = User.objects.filter(department=department)
    leaves = LeaveRequest.objects.filter(
        user__department=department
    ).select_related("user")
    context = {
        "department": department,
        "employees": employees,
        "leaves": leaves
    }
    return render(request, "department_employees.html", context)



@login_required(login_url='login')
@user_passes_test(isadmin, login_url='apply_leave')
def update_leave_status(request, leave_id, status):

    leave = LeaveRequest.objects.get(id=leave_id)

    leave.status = status
    leave.save()

    return redirect("leave_requests")




@login_required(login_url='login')
@user_passes_test(isadmin, login_url='apply_leave')
def leave_requests(request):

    leaves = LeaveRequest.objects.select_related("user").all().order_by("-created_at")

    context = {
        "leaves": leaves
    }

    return render(request, "leave_requests.html", context)

@login_required(login_url='login')
def emp_dashboard(request):
    department_employees = LeaveRequest.objects.all().filter(user = request.user).all()
    print(department_employees)
    return render(request, 'emp_dashboard.html', context = {'emp_' : department_employees})


@login_required(login_url='login')
def apply_leave(request):
    if request.method == "POST":
        form = LeaveRequestForm(
            request.POST,
            user=request.user
        )
        print(form.is_valid())
        if form.is_valid():
            leave = form.save(commit=False)
            leave.user = request.user
            leave.save()
            return redirect("dashboard")
    else:
        form = LeaveRequestForm(user=request.user)

    context = {
        "form": form
    }
    return render(request, "apply_leave.html", context)



