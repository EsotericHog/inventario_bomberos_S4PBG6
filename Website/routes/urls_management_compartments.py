from django.urls import path

#Módulos de vistas
from Website.views.views_management_compartments import *

#-----RUTAS DE GESTIÓN DE UNIDADES BOMBERILES-----
urlpatterns = [
    #Lista de gavetas
    path('management_compartments/list_compartments', listCompartmentsView, name="website-ruta_list_compartments"),
    #Lista de gavetas por vehiculo
    path('management_compartments/list_compartments/vehicle_<int:vehicle_id>', listCompartmentForVehicleView, name="website-ruta_list_compartments_for_vehicle"),
    #Agregar gaveta
    path('management_compartments/add_compartment', addCompartmentView, name="website-ruta_add_compartment"),
    #Modificar gaveta
    path('management_compartments/update_compartment/<int:compartment_id>', updateCompartmentView, name="website-ruta_update_compartment"),
    #Eliminar gaveta
    path('management_compartments/delete_compartment/<int:compartment_id>', deleteCompartmentView, name="website-ruta_delete_compartment"),
    #Función - Eliminar gaveta
    path('delete_compartment_function/<int:compartment_id>', deleteCompartment, name="website-ruta_delete_compartment_function"),
]