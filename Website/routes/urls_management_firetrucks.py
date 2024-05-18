from django.urls import path

#Módulos de vistas
from Website.views.views_management_firetrucks import *

#-----RUTAS DE GESTIÓN DE UNIDADES BOMBERILES-----
urlpatterns = [
    #Lista de unidades
    path('management_firetrucks/list_vehicles', listVehiclesView, name="website-ruta_list_vehicles"),
    #Agregar unidad
    path('management_firetrucks/add_vehicle', addVehicleView, name="website-ruta_add_vehicle"),
    #Modificar unidad
    path('management_firetrucks/update_vehicle/<int:vehicle_id>', updateVehicleView, name="website-ruta_update_vehicle"),
    #Eliminar unidad
    path('management_firetrucks/delete_vehicle/<int:vehicle_id>', deleteVehicleView, name="website-ruta_delete_vehicle"),
    #Función - Eliminar unidad
    path('delete_firetruck_function/<int:vehicle_id>', deleteVehicle, name="website-ruta_delete_vehicle_function"),
]