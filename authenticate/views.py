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


# def user_login(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             user = authenticate(request, username=cd['username'], password=cd['password'])
#             if user is not None:
#                 if user.is_active:
#                     login(request, user)
#                     messages.success(request, 'You have successfully logged in.')
#                     # return HttpResponse('Authenticated successfully')
#                     url = resolve_url('/')
#                     return redirect(url)
#                 else:
#                     messages.error(request, 'Account not enabled.')
#                     url = resolve_url('login')
#                     return redirect(url)
#             else:
#                 messages.error(request, 'Invalid username or password.')
#                 url = resolve_url('login')
#                 return redirect(url)
#     else:
#         form = LoginForm()
#         context = {
#             'form': form,
#         }
#         add_context_data(context, 'Login')
#         return render(request, 'registration/login.html', context)
#
#
# def user_logout(request):
#     logout(request)
#     context = {}
#     add_context_data(context, 'Logout')
#     return render(request, 'registration/logged_out.html', context)
#
#
# def password_change(request):
#     if request.method == 'POST':
#         form = PasswordChangeForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             user = authenticate(request, username=cd['username'], password=cd['password'])
#             if user is not None:
#                 if user.is_active:
#                     login(request, user)
#                     url = resolve_url('password_change_done')
#                     return redirect(url)
#                 else:
#                     messages.error(request, 'Account not enabled.')
#                     url = resolve_url('login')
#                     return redirect(url)
#             else:
#                 messages.error(request, 'Invalid username or password.')
#                 url = resolve_url('login')
#                 return redirect(url)
#     else:
#         form = PasswordChangeForm(request.POST)
#         context = {
#             'form': form,
#         }
#         add_context_data(context, 'Password Change')
#         return render(request, 'registration/password_change.html', context)
#
#
# def password_change_done(request):
#     context = {}
#     add_context_data(context, 'Password Change Done')
#     return render(request, 'registration/password_change_done.html', context)


# def home(request):
#     si = Sys_Settings()
#     context = {
#         'title': 'Auth Home',
#         'orgname': si.orgname,
#         'supportlink': si.supportlink
#     }
#     return render(request, 'auth-home.html', context=context)
#
#
# def login_user(request):
#     if request.method == 'POST':
#         if request.POST['submit'] == 'register':
#             redirect_url = resolve_url('signup')
#             return redirect(redirect_url)
#         elif request.POST['submit'] == 'reset':
#             redirect_url = resolve_url('password-reset')
#             return redirect(redirect_url)
#
#
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
#         if user is None:
#             messages.success(request, 'Username or password is incorrect')
#             redirect_url = resolve_url('login')
#             return redirect(redirect_url)
#         else:
#             session_id = request.session._get_or_create_session_key()
#             sid = Session_Info_Data(session_id)
#             sid.set_session_data('login', username)
#
#             login(request, user)
#             messages.success(request, 'You are now logged in')
#             return redirect('/')
#
#     else:
#         session_id = request.session._get_or_create_session_key()
#         sid = Session_Info_Data(session_id)
#         sid.remove_session_data('signup')
#         sid.remove_session_data('login')
#
#
#         si = Sys_Settings()
#         context = {
#             'title': 'Auth Home',
#             'orgname': si.orgname,
#             'supportlink': si.supportlink
#         }
#
#         return render(request, 'auth-login.html', context=context)
#

# def password_reset(request):
#     if request.method == 'POST':
#         email = request.POST['email']
#         # determine if email exists in user database
#         try:
#             users = User.objects.filter(email=email)
#             if len(users) > 1:
#                 messages.success(request, 'More than one user with this email')
#                 return redirect('/')
#             elif len(users) == 0:
#                 messages.success(request, 'No user with this email')
#                 return redirect('/')
#             else:
#                 user = users[0]
#                 # generate a random password
#                 password = base64.b64encode(os.urandom(24)).decode('utf-8')
#                 user.set_password(password)
#                 user.save()
#                 # send email with new password
#                 send_password_reset_email(user)
#                 messages.success(request, 'Password reset, email sent')
#                 return redirect('/')
#         except User.DoesNotExist:
#             user = None
#         if user is None:
#             messages.success(request, 'Email address not found')
#             return redirect('/')
#
#     else:
#         si = Sys_Settings()
#         form = PasswordResetForm()
#         context = {
#             'title': 'Password Reset',
#             'orgname': si.orgname,
#             'supportlink': si.supportlink,
#             'form': form
#         }
#         return render(request, 'password_reset_form.html', context=context)
#
#
# def logout_user(request):
#     if user_logged_in:
#         logout(request)
#         messages.success(request, 'You are now logged out')
#         return redirect('/')
#     else:
#         messages.success(request, 'You are not logged in')
#         return redirect('/')
#
#
# def signup_user(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         password1 = request.POST['password1']
#         first_name = request.POST['first_name']
#         last_name = request.POST['last_name']
#         email = request.POST['email']
#
#         form_data = {
#             'username': username,
#             'password': password,
#             'password1': password1,
#             'first_name': first_name,
#             'last_name': last_name,
#             'email': email
#         }
#         # convert form_data to a string
#         form_data_string = str(form_data)
#         session_id = request.session._get_or_create_session_key()
#         sid = Session_Info_Data(session_id)
#         sid.set_session_data('signup', form_data_string)
#
#         # load valid_domain from environment variable VALID_DOMAIN
#         valid_domain = os.environ.get('VALID_DOMAIN', '')
#
#         # check if email is valid
#         # check to see if email domain = valid_domain
#         if not email.endswith(valid_domain):
#             messages.success(request, 'Email domain is not valid')
#             redirect_url = resolve_url('signup')
#             return redirect(redirect_url)
#
#         if password == password1:
#             user = User.objects.create_user(username=username, password=password,
#                                             first_name=first_name, last_name=last_name, email=email)
#             try:
#                 user.save()
#                 messages.success(request, 'User created')
#                 return redirect('/')
#             except Exception as e:
#                 messages.success(request, e)
#                 redirect_url = resolve_url('signup')
#                 return redirect(redirect)
#         else:
#             messages.success(request, 'Passwords do not match')
#             redirect_url = resolve_url('signup')
#             return redirect(redirect_url)
#
#         user = authenticate(request, username=username, password=password)
#         if user is None:
#             messages.success(request, 'Username or password is incorrect')
#             redirect_url = resolve_url('login')
#             return redirect(redirect_url)
#         else:
#             login(request, user)
#             messages.success(request, 'You are now logged in')
#             redirect_url = resolve_url('/')
#             return redirect(redirect_url)
#     else:
#         si = Sys_Settings()
#         # check to see if session form_data exists
#         session_id = request.session._get_or_create_session_key()
#         sid = Session_Info_Data(session_id)
#         form_data_string = sid.get_session_data('signup')
#         # convert form_data from a string to a dictionary
#         if not form_data_string:
#             form_data = {
#                 'username': '',
#                 'password': '',
#                 'password1': '',
#                 'first_name': '',
#                 'last_name': '',
#                 'email': '',
#             }
#         else:
#             form_data = eval(form_data_string)
#
#         context = {
#             'title': 'Auth Home',
#             'orgname': si.orgname,
#             'supportlink': si.supportlink,
#             'form_data': form_data,
#         }
#         return render(request, 'auth-signup.html', context=context)

