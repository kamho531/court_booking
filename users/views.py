from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterUserForm, UpdateUserForm
from django.contrib.auth.models import User



def register(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
             # authenticate and login
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('booking_calendar')
    else:
        form = RegisterUserForm()
        return render(request, 'registration/register.html', {'form': form})
    
    return render(request, 'registration/register.html', {'form': form})



@login_required
def update_profile(request):
    if request.method == 'POST':
        form = UpdateUserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('update_success')  # Redirect to a profile page or any other page
    else:
        form = UpdateUserForm(instance=request.user)
    return render(request, 'registration/update_profile.html', {'form': form})


def update_success(request):
    return render(request, 'registration/update_success.html')



def custom_login(request):
    user = User.objects.all()
    # check if logging in
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('booking_calendar')
        else:
            messages.success(request, "Error! please try again!")
            return redirect('custom_login')
    else:
        return render(request, 'registration/login.html', {'user': user})



@login_required
def custom_logout(request):
    if request.method == 'POST':
        logout(request)
        return redirect('logout_success')
    return render(request, 'registration/custom_logout.html')



def logout_success(request):
    return render(request, 'registration/logout_success.html')





