from django.urls import path

#Módulos de vistas
from Website.views.views_management_inventory import *

#-----RUTAS DE GESTIÓN DE UNIDADES BOMBERILES-----
urlpatterns = [
    #Lista de insumos
    path('management_inventory/list_items', listInventoryView, name="website-ruta_list_items"),
    #Lista de insumos por lote
    path('management_inventory/list_items_many', listInventoryManyView, name="website-ruta_list_items_many"),
    #Lista de insumos dados de baja
    path('management_inventory/list_items_cancel', listInventoryCancelView, name="website-ruta_list_items_cancel"),
    #Lista de insumos dentro de lote
    path('management_inventory/list_items_many/<str:name>/', listInventoryDetailView, name="website-ruta_list_items_many_detail"),
    #Agregar insumo
    path('management_inventory/add_item/<int:type>', addInventoryView, name="website-ruta_add_item"),
    #Agregar insumo por lote
    path('management_inventory/add_item_many/<int:type>', addInventoryView, name="website-ruta_add_item_many"),
    #Modificar insumo
    path('management_inventory/update_item/<int:item_id>_<int:template>_<str:batch_name>', updateInventoryView, name="website-ruta_update_item"),
    #Dar de baja insumo
    path('management_inventory/cancel_item/<int:item_id>_<int:template>_<str:batch_name>', cancelInventoryView, name="website-ruta_cancel_item"),
    #Función - Dar de baja insumo
    path('management_inventory/cancel_item/<int:item_id>_<int:template>_<str:batch_name>/done', cancelInventory, name="website-ruta_cancel_item_function"),
]