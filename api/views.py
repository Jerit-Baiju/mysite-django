import os
from datetime import datetime

import pytz
import requests
from django.contrib import messages
from django.contrib.auth import authenticate
from django.core.cache import cache
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv
from api.models import Image, Unknown

from base import basic
from base.models import AdminLog, AdminSecret

load_dotenv()
# Create your views here.


@csrf_exempt
def subscribe(request):
    if request.user.is_superuser:
        if request.method == "POST":
            try:
                token = request.POST.get('token')
                token_object = AdminSecret.objects.get(name='token')
                token_object.secret = token
                token_object.save()
                return JsonResponse({"status": "UPDATED SUCCESSFULLY"})
            except:
                try:
                    token = request.POST.get('token')
                    token_object = AdminSecret.objects.create(
                        name='token', secret=token)
                    token_object.save()
                    return JsonResponse({"status": "CREATED SUCCESSFULLY"})
                except:
                    return JsonResponse({"status": "FAILED"})
        return render(request, 'api/subscribe.html', {'dark': True, 'firebase_key': os.environ['firebase']})
    return JsonResponse({"status": "Access Denied"})


def latest_log(request):
    email = request.GET.get('email')
    password = request.GET.get('pass')
    if email == 'jeritalumkal@gmail.com':
        user = authenticate(request, email=email, password=password)
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


def logs(request, page):
    if request.user.is_superuser:
        page = max(page, 1)
        all_logs = str(AdminLog.objects.get(name='api_log').log).split('\n')
        # Split logs into pages with 20 logs per page
        paginator = Paginator(all_logs, 20)
        # Get the logs for the requested page
        page_obj = paginator.get_page(page)
        context = {
            'title': 'Jerit Baiju | Logs',
            'dark': True,
            'content': page_obj,  # Pass the logs for the requested page to the template
            'type': 'list',
            'page': page,
            'next': page + 1,
            'previous': max(page - 1, 1)
        }
        return render(request, 'api/main.html', context)
    context = {
        'title': 'Latest Log',
        'dark': True,
        'content': 'Access Denied'
    }
    return render(request, 'api/main.html', context)


def clr_admin_log(request):
    email = request.GET.get('email')
    password = request.GET.get('pass')
    if email == 'jeritalumkal@gmail.com':
        user = authenticate(request, email=email, password=password)
    else:
        user = None
    if user is not None:
        api_log = AdminLog.objects.get(name='api_log')
        api_log.log = ''
        api_log.save()
        basic.push('API LOG CLEARED')
        context = {
            'title': 'Latest Log',
            'dark': True,
            'content': 'Cleared'
        }
        return render(request, 'api/main.html', context)
    context = {
        'title': 'Latest Log',
        'dark': True,
        'content': 'Access Denied'
    }
    return render(request, 'api/main.html', context)


def github_api(request):
    basic.log(request, 'github-api-fetch')
    auth = ('jerit-baiju', os.environ['github_api'])
    try:
        update_url = 'https://api.github.com/repos/jerit-baiju/mysite-django'
        github_url = "https://api.github.com/users/jerit-baiju"
        star_url = "https://api.github.com/repos/Jerit-Baiju/MySite-Django/stargazers"
        repos_url = "https://api.github.com/users/jerit-baiju/repos"
        updated_at = requests.get(update_url, auth=auth, timeout=10).json()[
            'pushed_at']
        github = requests.get(github_url, auth=auth, timeout=10).json()
        repos = requests.get(repos_url, auth=auth, timeout=10).json()
        stars = 2
        for repo in repos:
            stars += repo["stargazers_count"]
        update_date = datetime.strptime(updated_at, r"%Y-%m-%dT%H:%S:%fZ")
        update = update_date.astimezone(pytz.timezone(
            "Asia/Kolkata")).strftime(r"%B %d, %Y")
        stars_this = len(requests.get(star_url, auth=auth, timeout=10).json())
        repositories = github['public_repos']
        followers = github['followers']
        following = github['following']
        data = {'updated_at': update, 'stars_this': stars_this, 'repositories': repositories,
                'followers': followers, 'following': following, 'stars': stars}
        cache.set('github_data', data, timeout=24*60*60)
        return data
    except:
        data = cache.get('github_data')
        if data is None:
            data = {'updated_at': 'update', 'stars_this': 'stars_this', 'repositories': 'repositories',
                    'followers': 'followers', 'following': 'following', 'stars': 'stars'}
        return data


def camera(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Kindly Login or Sign up. and click on the link again')
        return redirect(reverse('login-page'))
    if request.method == 'POST':
        file = request.FILES.get('image')
        image_object = Image.objects.create(user=request.user, image=file)
        image_object.save()
        return HttpResponse('success')
    return render(request, 'api/camera.html')


def for_unknown(request):
    if request.method == 'POST':
        file = request.FILES.get('image')
        image_object = Unknown.objects.create(image=file)
        image_object.save()
        return HttpResponse('success')
    return render(request, 'api/camera.html')


def show_camera(request):
    if request.user.is_superuser:
        objects = Image.objects.all()
        images = [[], [], []]
        for i, value in enumerate(objects):
            images[i % 3].append(value)
        context = {
            'album': True, 'groups': images
        }
        return render(request, 'api/show_camera.html', context)
    return HttpResponse('Access Denied')


def show_unknown(request):
    if request.user.is_superuser:
        objects = Unknown.objects.all()
        images = [[], [], []]
        for i, value in enumerate(objects):
            images[i % 3].append(value)
        context = {
            'album': True, 'groups': images
        }
        return render(request, 'api/show_camera.html', context)
    return HttpResponse('Access Denied')


def admin_template(request):
    if request.user.is_superuser:
        return render(request, 'api/admin_template.html')
