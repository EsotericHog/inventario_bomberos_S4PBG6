from django.urls import path

#Módulos de vistas
from Website.views.json import *

urlpatterns = [
    #RUTAS PARA LISTAS JSON
    #Regiones
    path('regions/', get_regions, name="website-ruta_get-regions"),
    #Comunas
    path('comunes/<int:regions_id>', get_comunes, name="website-ruta_get-comunes"),
    #Estaciones
    path('stations/<int:comunes_id>', get_fireStations, name="website-ruta_get-stations"),
    #Roles
    path('profiles/', get_profiles, name="website-ruta_get-profiles"),
    #Categorías
    path('categories/', get_categories, name="website-ruta_get-categories"),
    #Unidades
    path('firetrucks/', get_fire_trucks, name="website-ruta_get-firetrucks"),
    #Unidades
    path('compartments/<int:vehicle_id>', get_compartments, name="website-ruta_get-compartments"),
    #Contenedores de inventario
    path('containers/', get_container_items, name="website-ruta_get-containers"),
    #Programas de mantenimiento
    path('maintenance_programs/', get_maintenance_programs, name="website-ruta_get-programs"),
]