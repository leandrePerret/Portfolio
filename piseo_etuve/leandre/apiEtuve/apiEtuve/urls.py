from django.contrib import admin
from django.urls import path, re_path
from pages.views import *

handler404 = 'pages.views.custom_404' #Redirection des pages non trouvées vers la fonction custom_404 de pages\views.py

urlpatterns = [
    path('', index, name='index'),
    path('index/', index, name='index'),
    path('consign/<str:host>/<int:port>/<str:temperature>/<int:second>/', consign, name='consign'),
    path('consign/<str:host>/<int:port>/<str:temperature>/<int:second>/<int:type>/', consign, name='consign'),
    path('read/<str:host>/<int:port>/', read, name='read'),
    path('readTemperature/<str:host>/<int:port>/', readTemperature, name='readTemperature'),
    path('readConsign/', readConsign, name='readConsign'),
    #Liste de toutes les URL connues par l'API et des fonctions correspondantes.
]   
"""
re_path(r"^index/$", index, name='index'),
re_path(r"^api/consign/$", badConsign, name='badConsign'),
re_path(r"^api/read/$", badRead, name='badRead'),
re_path(r"^api/readTemperature/$", badReadTemperature, name='badReadTemperature'),
re_path(r"^api/readConsign/$", badReadConsign, name='badReadConsign'),
"""