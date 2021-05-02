from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import (authenticate, login, logout,
                                 update_session_auth_hash)
from django.contrib.auth.decorators import login_required

from .forms import (LoginForm, UserRegistrationForm,
                    UserProfileForm, ChangePasswordForm)


@login_required
def home(request):

    return render(request, "mysite/home.html")


def user_login(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(request.GET.get('next', 'home'))
            else:
                messages.error(request, 'Check your login details and try again',
			                   extra_tags='alert alert-danger alert-dismissible fade show'
			                  )
                return redirect("home")
        

    return render(request, "mysite/login.html", {"form": form})


def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'Registration was successful',
                             extra_tags='alert alert-success alert-dismissible fade show'  # noqa: E501
                            )
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'mysite/register.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('user_login')


def edit_user_info(request):
    form = UserProfileForm(instance=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your changes were successfully saved ',
                             extra_tags='alert alert-success alert-dismissible fade show'  
                            )
            return redirect('home')

    return render(request, 'mysite/edit_user_info.html', {'form': form})


def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully changed!',  
                             extra_tags='alert alert-success alert-dismissible fade show'  
                            )
            return redirect('home')
        else:
            messages.error(request, 'Please correct the error below.',  
                           extra_tags='alert alert-danger alert-dismissible fade show'  
                          )
    else:
        form = ChangePasswordForm(request.user)
    return render(request, 'mysite/change_password.html', {
        'form': form
    })
