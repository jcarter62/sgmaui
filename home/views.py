from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth import user_logged_in
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Sys_Settings, SessionData, UserSetting
from decouple import config


def view_home(request):
    ss = Sys_Settings()

    context = {
        'title': 'Home',
        'orgname': ss.get_orgname,
        'supportlink': ss.get_supportlink,
    }
    return render(request, 'home.html', context=context)

def view_about(request):
    return render(request, 'about.html')

def view_contact(request):
    return render(request, 'contact.html')

def view_faq(request):
    return render(request, 'faq.html')

def view_privacy(request):
    return render(request, 'privacy.html')

def view_terms(request):
    return render(request, 'terms.html')

def view_login(request):
    return render(request, 'login.html')

def view_showenv(request):
    settings = [
        'SQL_DB_NAME', 'SQL_USER', 'SQL_PASSWORD', 'SQL_HOST', 'SQL_PORT', 'DEFAUL_FROM_EMAIL', 'EMAIL_HOST', 'EMAIL_PORT'
    ]

    items = []
    for one_setting in settings:
        try:
            value = config(one_setting, default='Not Set')
        except Exception as e:
            value = e.message.__str__()

        s = "Setting: {} = {}".format(one_setting, value)
        items.append(s)

    context = {
        'items': items
    }

    return render(request, 'showenv.html', context=context)



# path('params/set/<str:session>/<str:key>/<str:value>')
def view_set_param(request, session:str, key:str, value:str):
    code = 0

    if value == 'X-RESET-X':
        value = ''

    try:
        record = None
        for rec in SessionData.objects.all():
            if rec.session == session and rec.key_name == key:
                record = rec
                break
        if record:
            record.key_text = value
            record.save()
            code = 200
        else:
            record = SessionData(
                session=session,
                key_name=key,
                key_text=value
            )
            record.save()
            code = 201
    except Exception as e:
        print(e.message.__str__())
        code = 500

    data = {"result": "OK", "code": code}
    return JsonResponse(data)


# path('params/get/<str:session>/<str:key>')
def view_get_param(request, session, key):
    result = ''
    code = 404
    try:
        record = None
        for rec in SessionData.objects.all():
            if rec.session == session and rec.key_name == key:
                record = rec
                break
        if record:
            result = record.key_text
            code = 200
    except Exception as e:
        print(e.message.__str__())
        code = 500

    if result == '':
        result = ''
        code = 404

    data = {"result": result, "code": code }
    return JsonResponse(data)


def save_parameter(key, value, username):
    # save setting for user in UserSettings table
    try:
        record = None
        for rec in UserSetting.objects.all():
            if rec.username == username and rec.key_name == key:
                record = rec
                break
        if record is not None:
            record.key_text = value
        else:
            record = UserSetting()
            record.username = username
            record.key_name = key
            record.key_text = value
        record.save()
    except Exception as e:
        print(e.message.__str__())
    return

def load_parameter(key, username):
    # load setting for user in UserSettings table
    try:
        record = None
        for rec in UserSetting.objects.all():
            if rec.username == username and rec.key_name == key:
                record = rec
                break
        if record is not None:
            return record.key_text
    except Exception as e:
        pass
    return ''


@login_required
def view_user_settings(request):
    if request.user.is_authenticated:
        username = request.user.username
    else:
        username = ''

    if request.method == 'POST':
        # load the form data
        rows_per_page = request.POST.get('rows_per_page')
        chk = request.POST.get('show_only_active_parcels')
        if chk == 'true':
            show_only_active_parcels = 'True'
        else:
            show_only_active_parcels = 'False'
        save_parameter('rows_per_page', rows_per_page, username)
        save_parameter('show_only_active_parcels', show_only_active_parcels, username)

    rows_per_page = load_parameter('rows_per_page', username)
    show_only_active_parcels = load_parameter('show_only_active_parcels', username) == 'True'

    context = {
        'title': 'User Settings',
        'username': username,
        'rows_per_page': rows_per_page,
        'show_only_active_parcels': show_only_active_parcels,
    }
    return render(request, 'user-settings.html', context=context)



