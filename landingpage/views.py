from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from camping.models import CampingItem, Category
from django.core.paginator import Paginator

def is_staff_or_admin(user):
    return user.is_staff or user.is_admin()

@login_required
def admin_dashboard(request):
    return render(request, 'layouts/base.html')

@login_required
def staff_dashboard(request):
    return render(request, 'layouts/staff_dashboard.html')

def member_dashboard(request):
    total_items = CampingItem.objects.count()
    total_categories = Category.objects.count()
    items = CampingItem.objects.all()
    paginator = Paginator(items, 6)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'landingpage/home.html', {'page_obj': page_obj, 'total_items': total_items, 'total_categories': total_categories})

def price(request):
    items = CampingItem.objects.all()

    paginator = Paginator(items, 5)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'landingpage/price_item.html', {'page_obj': page_obj})

