from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Category, CampingItem
from .forms import CategoryForm, CampingItemForm
from django.http import JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator

def is_admin(user):
    return user.is_admin()

@login_required
@user_passes_test(is_admin)
def camping_item_list(request):
    search_query = request.GET.get('search', '')
    order_by = request.GET.get('order_by')

    # Mulai dengan query dasar
    items = CampingItem.objects.filter(
        Q(name__icontains=search_query) |
        Q(description__icontains=search_query)
    )

    # Tambahkan pengurutan
    if order_by == 'asc':
        items = items.order_by('price')
    elif order_by == 'desc':
        items = items.order_by('-price')

    # Lakukan paginasi setelah pengurutan
    paginator = Paginator(items, 10)
    page_number = request.GET.get('page', 1)
    items_page = paginator.get_page(page_number)

    return render(request, 'camping/camping_item_list.html', {
        'items': items_page,
    })

@login_required
@user_passes_test(is_admin)
def camping_item_create(request):
    if request.method == 'POST':
        form = CampingItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('camping_item_list')
    else:
        form = CampingItemForm()
    return render(request, 'camping/new_item.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def camping_item_update(request, pk):
    item = get_object_or_404(CampingItem, pk=pk)
    if request.method == 'POST':
        form = CampingItemForm(request.POST,request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect('camping_item_list')
    else:
        form = CampingItemForm(instance=item)
    return render(request, 'camping/new_item.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def camping_item_delete(request, pk):
    item = get_object_or_404(CampingItem, pk=pk)
    if request.method == 'POST':
        item.delete()
        return JsonResponse({'success': True, 'message': 'Item deleted successfully'})
    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)


@login_required
@user_passes_test(is_admin)
def camping_category(request):
    categories = Category.objects.all()
    return render(request, 'camping/category_item.html', {'categories': categories})

@login_required
@user_passes_test(is_admin)
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'camping/category_add.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def category_item_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST,request.FILES, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'camping/category_add.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        return JsonResponse({'success': True, 'message': 'Item deleted successfully'})
    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)
