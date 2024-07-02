from django.urls import path, include

#Módulos de vistas
from Website.views.home import *
from Website.views.access import *
from Website.views.about import about

urlpatterns = [
    #RUTA PRINCIPAL
    #Inicio
    path('', home, name="website-ruta_home"),

    #Información del proyecto
    path('about', about, name="website-ruta_about"),
]