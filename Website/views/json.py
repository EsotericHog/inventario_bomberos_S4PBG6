from django.shortcuts import render
from django.urls import reverse
from django.db.models import Count
from django.http import JsonResponse
from django.contrib import messages
from django.http import HttpResponse, Http404, HttpResponseRedirect
from ..models import Region, Comune, FireStation, Profile, Category, Inventory, InventoryMetadata, FireTruck, Compartment, MaintenanceProgram

#Obtener regiones
def get_regions(request):
    regions = list(Region.objects.values())

    if (len(regions) > 0):
        data = {'message':"Success", 'regions': regions}
    else:
        data = {'message':"Not Found"}

    return JsonResponse(data)


#Obtener comunas
def get_comunes(request, regions_id):
    comunes = list(Comune.objects.filter(regions_id=regions_id).values())

    if (len(comunes) > 0):
        data = {'message':"Success", 'comunes': comunes}
    else:
        data = {'message':"Not Found"}

    return JsonResponse(data)


#Obtener estaciones de bomberos
def get_fireStations(request, comunes_id):
    stations = list(FireStation.objects.filter(comunes_id=comunes_id).values())

    if (len(stations) > 0):
        data = {'message':"Success", 'stations': stations}
    else:
        data = {'message':"Not Found"}

    return JsonResponse(data)


#Obtener perfiles de usuario (exceptuando el de administrador)
def get_profiles(request):
    profiles = list(Profile.objects.exclude(id=6).values())

    if (len(profiles) > 0):
        data = {'message':"Success", 'profiles': profiles}
    else:
        data = {'message':"Not Found"}

    return JsonResponse(data)


##Obtener metadata de insumos
#def get_items_meta(request):
#    fire_trucks = FireTruck.objects.filter(fire_stations=request.session.get('fire_station_id'))
#    total_compartments = Compartment.objects.filter(fire_trucks__in=fire_trucks)
#    items = list(Inventory.objects.filter(compartments__in=total_compartments).select_related('inventorymetadata'))
#    
#    items_metadata = [
#        {
#            'id': item.id,
#            'name': item.inventorymetadata.name,
#            'description': item.inventorymetadata.description,
#        }
#        for item in items
#    ]
#
#    if(len(items_metadata) > 0):
#        data = {'message':"success", 'items': items_metadata}
#    else:
#        data = {'message':"Not Found"}
#
#    return JsonResponse(data)


#Obtener categorías de insumos
def get_categories(request):
    categories = list(Category.objects.all().values())

    if (len(categories) > 0):
        data = {'message':"Success", 'categories': categories}
    else:
        data = {'message':"Not Found"}

    return JsonResponse(data)


#Obtener unidades
def get_fire_trucks(request):
    firetrucks = list(FireTruck.objects.filter(fire_stations_id=request.session.get('fire_station_id')).exclude(id = 3).values())

    if (len(firetrucks) > 0):
        data = {'message':"Success", 'firetrucks': firetrucks}
    else:
        data = {'message':"Not Found"}

    return JsonResponse(data)


#Obtener gavetas
def get_compartments(request, vehicle_id):
    compartments = list(Compartment.objects.filter(fire_trucks_id=vehicle_id).values())

    if (len(compartments) > 0):
        data = {'message':"Success", 'compartments': compartments}
    else:
        data = {'message':"Not Found"}

    return JsonResponse(data)


#Obtener insumos contenedores
def get_container_items(request):
    category = Category.objects.filter(name = "CONTENEDORES Y BOLSOS").get()
    fire_station = FireTruck.objects.filter(id = request.session.get('fire_station_id')).get()
    container_items = list(InventoryMetadata.objects.filter(inventory__categories_id = category.id, inventory__compartments__fire_trucks__fire_stations=fire_station.id).values())

    if (len(container_items) > 0):
        data = {'message': "Success", 'containers': container_items}
    else:
        data = {'message': "Not Found"}
    return JsonResponse(data)


#Obtener programas de mantenimiento
def get_maintenance_programs(request):
    programs = list(MaintenanceProgram.objects.all().values())

    if (len(programs) > 0):
        data = {'message':"Success", 'programs': programs}
    else:
        data = {'message':"Not Found"}

    return JsonResponse(data)