from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect, resolve_url
from django.contrib.auth import authenticate, login, logout, user_logged_in, user_logged_out
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, PasswordChangeForm
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

from authenticate.forms import LoginForm
from home.models import Sys_Settings
from .forms import UserRegistrationForm, UserProfileForm


def add_context_data(context, title):
    si = Sys_Settings()
    context['title'] = title
    context['orgname'] = si.orgname
    context['supportlink'] = si.supportlink
    return


def register(request):
    si = Sys_Settings()
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # determine if email domain is allowed.
            email = user_form.cleaned_data['email']
            domain = email.split('@')[1]
            if domain not in si.allowed_domains:
                messages.error(request, 'Your email domain ' + domain + ' is not allowed.')
                return redirect('register')

            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(
                user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            return render(request,
                          'registration/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'registration/registration_form.html', {'form': user_form})


def user_profile(request):
    si = Sys_Settings()
    if request.method == 'POST':
        user_form = UserProfileForm(instance=request.user, data=request.POST)
        if user_form.is_valid():
            email = user_form.cleaned_data['email']
            domain = email.split('@')[1]
            if domain not in si.allowed_domains:
                messages.error(request, 'Your email domain ' + domain + ' is not allowed.')
                return redirect('profile')

            user_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserProfileForm(instance=request.user)
    return render(request, 'registration/profile.html', {'form': user_form})
