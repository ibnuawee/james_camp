from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Category, CampingItem
from .forms import CategoryForm, CampingItemForm
from django.http import JsonResponse

# Helper function untuk staff/admin
def is_staff_or_admin(user):
    return user.is_staff or user.is_admin()

@login_required
def admin_dashboard(request):
    return render(request, 'layouts/base.html')

@login_required
def staff_dashboard(request):
    return render(request, 'layouts/staff_dashboard.html')

@login_required
def member_dashboard(request):
    return render(request, 'layouts/member_dashboard.html')

# List semua alat camping
@login_required
def camping_item_list(request):
    items = CampingItem.objects.all()
    return render(request, 'camping/camping_item_list.html', {'items': items})

# Tambah alat camping
@login_required
@user_passes_test(is_staff_or_admin)
def camping_item_create(request):
    if request.method == 'POST':
        form = CampingItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('camping_item_list')
    else:
        form = CampingItemForm()
    return render(request, 'camping/new_item.html', {'form': form})

# Edit alat camping
@login_required
@user_passes_test(is_staff_or_admin)
def camping_item_update(request, pk):
    item = get_object_or_404(CampingItem, pk=pk)
    if request.method == 'POST':
        form = CampingItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('camping_item_list')
    else:
        form = CampingItemForm(instance=item)
    return render(request, 'camping/new_item.html', {'form': form})

# Hapus alat camping
@login_required
@user_passes_test(is_staff_or_admin)
def camping_item_delete(request, pk):
    item = get_object_or_404(CampingItem, pk=pk)
    if request.method == 'POST':
        item.delete()
        return JsonResponse({'success': True, 'message': 'Item deleted successfully'})
    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)

# Tambah kategori
@login_required
@user_passes_test(is_staff_or_admin)
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('camping_item_list')
    else:
        form = CategoryForm()
    return render(request, 'camping/category_form.html', {'form': form})
