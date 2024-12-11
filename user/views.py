from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from .forms import UserForm, UserEditForm

User = get_user_model()

@login_required
def user_list(request):
    search_query = request.GET.get('search', '')
    users = User.objects.filter(username__icontains=search_query).order_by('id')

    # Paginator setup
    paginator = Paginator(users, 10)  # 10 users per page
    page_number = request.GET.get('page')
    users_page = paginator.get_page(page_number)

    return render(request, 'user/index.html', {'users': users_page})

@login_required
def user_create(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Set password
            user.save()
            return redirect('user_list')
    else:
        form = UserForm()
    return render(request, 'user/add_user.html', {'form': form})

@login_required
def user_edit(request, pk):
    user = get_object_or_404(User, pk=pk)
    # roles = Role.objects.all()
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = UserEditForm(instance=user)
    return render(request, 'user/edit_user.html', {'form': form})

@login_required
def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
        return redirect('user_list')
    return render(request, 'user_confirm_delete.html', {'user': user})
