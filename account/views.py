from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import SignupForm
from django.contrib.auth.decorators import login_required 

# Create your views here.
def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()

            return redirect("login")

    else:
        form = SignupForm()

    return render(request, "signup.html", {"form": form})


def login_view(request):
    next_url = request.GET.get("next")
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(
            request,
            username=username,
            password=password
        )
        if user:
            login(request, user)

            if next_url:
                return redirect(next_url)
            return redirect("dashboard") if user.is_superuser else redirect('apply_leave')
        
    return render(request, "login.html")


@login_required(login_url='login')
def logout_view(request):

    logout(request)
    return redirect("login")
