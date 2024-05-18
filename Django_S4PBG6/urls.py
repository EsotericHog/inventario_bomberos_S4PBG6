from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    #Ruta Home
    path('', include('Website.routes.urls'), name="app1-rutas_home"),
    #Rutas de acceso
    path('', include('Website.routes.urls_access'), name="app1-rutas_acceso"),
    #Rutas de gestión de usuarios
    path('', include('Website.routes.urls_management_users'), name="app1-rutas_usuarios"),
    #Rutas de gestión de vehículos
    path('', include('Website.routes.urls_management_firetrucks'), name="app1-rutas_vehiculos"),
    #Rutas de gestión de gavetas
    path('', include('Website.routes.urls_management_compartments'), name="app1-rutas_gavetas"),
    #Rutas de gestión de gavetas
    path('', include('Website.routes.urls_management_inventory'), name="app1-rutas_items"),
    #Rutas para json
    path('', include('Website.routes.urls_json'), name="app1-rutas_ajax")
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)