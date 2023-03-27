from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('login/', views.login_page, name='login-page'),
    path('logout-admin/', views.logout_page, name='logout-page'),
    path('register/', views.register_page, name='register-page'),

    path('gallery/', views.gallery, name='gallery'),
    path('stats/', views.stats, name='stats'),
    path('about/', views.about, name='about'),

    path('github/', views.github, name='github'),
    path('instagram/', views.instagram, name='instagram'),
    path('whatsapp/', views.whatsapp, name='whatsapp'),
    path('vijayamatha/', views.vijayamatha, name='vijayamatha'),

    path('sitemap.xml', views.sitemap, name='sitemap'),
    path('robots.txt', views.robots, name='robots'),
    path('manifest.json', views.manifest, name='manifest'),
    path('service-worker.js', views.ServiceWorkerView.as_view(), name='service_worker'),
    path('offline.html', views.offline_page, name='offline-page'),
]
