from base.models import AdminLog
from base.views import push, log
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from .models import DataStore, Data
# Create your views here.


def latest_log(request):
    username = request.GET.get('user')
    password = request.GET.get('pass')
    if username == 'jerit':
        user = authenticate(request, username=username, password=password)
    else:
        user = None
    if user is not None:
        context = {
            'title': 'Latest Log',
            'dark': True,
            'content': AdminLog.objects.get(name='api_log').latest_log
        }
        return render(request, 'api/main.html', context)
    else:
        context = {
            'title': 'Latest Log',
            'dark': True,
            'content': 'Access Denied'
        }
        return render(request, 'api/main.html', context)


def log(request):
    username = request.GET.get('user')
    password = request.GET.get('pass')
    if username == "jerit":
        user = authenticate(request, username=username, password=password)
    else:
        user = None
    if user is not None:
        context = {
            'title': 'Jerit Baiju | Logs',
            'dark': True,
            'content': str(AdminLog.objects.get(name='api_log').log).split('\n'),
            'type': 'list'
        }
        return render(request, 'api/main.html', context)
    else:
        context = {
            'title': 'Latest Log',
            'dark': True,
            'content': 'Access Denied'
        }
        return render(request, 'api/main.html', context)


def clr_admin_log(request):
    username = request.GET.get('user')
    password = request.GET.get('pass')
    if username == 'jerit':
        user = authenticate(request, username=username, password=password)
    else:
        user = None
    if user is not None:
        log = AdminLog.objects.get(name='api_log')
        log.log = ''
        log.save()
        push('API LOG CLEARED')
        context = {
            'title': 'Latest Log',
            'dark': True,
            'content': 'Cleared'
        }
        return render(request, 'api/main.html', context)
    else:
        context = {
            'title': 'Latest Log',
            'dark': True,
            'content': 'Access Denied'
        }
        return render(request, 'api/main.html', context)


def add_data(request, store):
    key = request.GET.get('value')
    data = request.GET.get('data')
    store_model,_ = DataStore.objects.get_or_create(name=store)
    data_model = Data.objects.create(store=store_model,key=key, data=data)
    store_model.value.add(data_model)
    push('NEW DATA')
    log(request, 'NEW DATA')
    return redirect('https://instagram.com')
