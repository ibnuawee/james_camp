from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def is_staff_or_admin(user):
    return user.is_staff or user.is_admin()

@login_required
def admin_dashboard(request):
    return render(request, 'layouts/base.html')

@login_required
def staff_dashboard(request):
    return render(request, 'layouts/staff_dashboard.html')

def member_dashboard(request):
    return render(request, 'landingpage/home.html')

