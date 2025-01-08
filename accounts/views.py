from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import UserRegistrationForm, UserUpdateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect_user(request)
        else:
            messages.error(request, 'Username atau password salah')
            return render(request, 'accounts/login.html', {'error': 'Username atau password salah.'})
    return render(request, 'accounts/login.html')

@login_required
def profile_view(request):
    user = request.user

    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profil berhasil diperbarui.')
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=user)

    return render(request, 'accounts/profile.html', {'form': form, 'user': user})

def redirect_user(request):
    user = request.user
    if user.is_admin():
        return redirect('admin_dashboard')
    elif user.is_staff_user():
        return redirect('admin_dashboard')
    elif user.is_member():
        return redirect('home')
    else:
        return redirect('login')


