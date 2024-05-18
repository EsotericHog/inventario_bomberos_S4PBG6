from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from ..forms import FireTruckForm
from ..models import FireTruck, Compartment, TypeFireTruck
from ..utilities.functions import getExtension
from ..utilities.decorators import *
from django.db.models import Count, Sum, Max
from django.core.files.storage import FileSystemStorage
import os
from datetime import datetime, date, timedelta
from django.conf import settings
from django.core.files.storage import default_storage

#Vista - Lista de vehículos de la estación
@login_required
def listVehiclesView(request):
    #Obtención de registros de vehículos con un campo adicional que cuenta las gavetas asignadas mediante la relación "compartment"
    #firetrucks = FireTruck.objects.filter(fire_stations_id = request.session.get('fire_station_id')).exclude(id = 3).annotate(total_compartments=Count('compartment', distinct=True), total_items=Count('compartment__inventory'), total_quantity=Sum('compartment__quantity'))
    #count_firetrucks = firetrucks.count()
    #
    #return render(request, 'Website/management_firetrucks/list_vehicles.html', {'firetrucks':firetrucks, 'count_firetrucks':count_firetrucks})

    firetrucks = FireTruck.objects.filter(fire_stations_id = request.session.get('fire_station_id')).exclude(id = 3).annotate(total_compartments=Count('compartment', distinct=True), total_items=Count('compartment__inventory'))
    count_firetrucks = firetrucks.count()

    for truck in firetrucks:
        compartments = Compartment.objects.filter(fire_trucks_id = truck.id)
        truck.max_quantity = sum(compartment.quantity for compartment in compartments)
    
    return render(request, 'Website/management_firetrucks/list_vehicles.html', {'firetrucks':firetrucks, 'count_firetrucks':count_firetrucks})


    for camion in camiones:
        gavetas = Gaveta.objects.filter(camion=camion)
        camion.cantidad_maxima_insumos = sum(gaveta.cantidad for gaveta in gavetas)
    return render(request, 'lista_camiones.html', {'camiones': camiones})


#Vista - Agregar vehículo
@login_required
def addVehicleView(request):
    form = FireTruckForm(request.POST or None, request.FILES or None)
    types = TypeFireTruck.objects.all()

    if request.method == 'POST':
        if form.is_valid():
            #¿La patente existe?
            if (FireTruck.objects.filter(plate=request.POST['plateField']).exists()):
                messages.add_message(request, messages.WARNING, f"La patente ya está en uso.")
                return HttpResponseRedirect(reverse('website-ruta_add_vehicle'))
            #¿Se seleccionó el tipo de unidad?
            if (request.POST['typeFireTruck'] == '0'):
                messages.add_message(request, messages.WARNING, f"Debe seleccionar el tipo de vehículo.")
                return HttpResponseRedirect(reverse('website-ruta_add_vehicle'))
            
            #Validar imagen - Si no se envió una imagen, se asigna la imagen por defecto
            if not request.FILES:
                image_name = "default-firetruck.png"
            else:
                file = request.FILES['imageField']
                if not (getExtension(request.FILES['imageField'])):
                    messages.add_message(request, messages.WARNING, f"El archivo de imagen no es válido. Sólo se permiten archivos jpg, png y jpeg.")
                    return HttpResponseRedirect(reverse('website-ruta_add_vehicle'))
                else:
                    #Guardar imagen
                    fss = FileSystemStorage()
                    current_date = datetime.now()
                    image_name = f"{datetime.timestamp(current_date)}{os.path.splitext(str(request.FILES['imageField']))[1]}"
                    upload = fss.save(f"firetrucks/{image_name}", file)
                    #uploaded_file_url = fss.url(upload)
                
            #Intentar generar registro
            try:
                FireTruck.objects.create(name=request.POST['nameField'], description=request.POST['descriptionField'], plate=request.POST['plateField'], model=request.POST['modelField'], year=request.POST['yearField'], type_fire_trucks_id=request.POST['typeFireTruck'], fire_stations_id=request.session.get('fire_station_id'), image=image_name)
                messages.add_message(request, messages.SUCCESS, f"Unidad creada con éxito. Se requiere asignar gavetas para almacenar insumos.")
                return HttpResponseRedirect(reverse('website-ruta_list_vehicles'))
            except Exception as e:
                messages.add_message(request, messages.WARNING, f"Ocurrió un error inesperado. Por favor, vuelva a intentarlo. {e}, {request.POST}")
                return HttpResponseRedirect(reverse('website-ruta_list_vehicles'))
                
        else:
            messages.add_message(request, messages.WARNING, f"No fue posible crear la unidad. Vuelva a intentarlo. {form.errors}")
            return HttpResponseRedirect(reverse('website-ruta_add_vehicle'))

    return render(request, 'Website/management_firetrucks/add_vehicle.html', {'form':form, 'types':types})


#Vista - Modificar vehículo
@login_required
def updateVehicleView(request, vehicle_id):
    #Obtener registro a modificar
    vehicle = FireTruck.objects.filter(id=vehicle_id).get()
    #Obtener lista excluyendo el seleccionado para que no detecte valores existentes
    vehicles = FireTruck.objects.exclude(id=vehicle_id)
    #Tipos de vehículo
    types = TypeFireTruck.objects.exclude(id=vehicle.type_fire_trucks_id)
    #Tipo de vehículo seleccionado
    type = TypeFireTruck.objects.filter(id=vehicle.type_fire_trucks_id).get()
    #Valores iniciales para los campos del formulario
    initial_data = {
        'nameField': vehicle.name,
        'descriptionField': vehicle.description,
        'plateField': vehicle.plate,
        'modelField': vehicle.model,
        'yearField': vehicle.year,
    }
    #Formulario
    form = FireTruckForm(request.POST or None, request.FILES or None, initial=initial_data)


    if request.method == 'POST':
        if form.is_valid():
            #¿La patente existe?
            if (FireTruck.objects.filter(plate=request.POST['plateField']).exclude(id=vehicle.id).exists()):
                messages.add_message(request, messages.WARNING, f"La patente ya está en uso.")
                return HttpResponseRedirect(reverse('website-ruta_update_vehicle', args=[vehicle_id]))
            
            #¿Se seleccionó el tipo de unidad?
            if (request.POST['typeFireTruck'] == '0'):
                messages.add_message(request, messages.WARNING, f"Debe seleccionar el tipo de vehículo.")
                return HttpResponseRedirect(reverse('website-ruta_update_vehicle', args=[vehicle_id]))
            
            #Validar imagen - Si no se envió una imagen, se asigna la imagen por defecto
            if not request.FILES:
                image_name = vehicle.image
            else:
                file = request.FILES['imageField']
                if not (getExtension(request.FILES['imageField'])):
                    messages.add_message(request, messages.WARNING, f"El archivo de imagen no es válido. Sólo se permiten archivos jpg, png y jpeg.")
                    return HttpResponseRedirect(reverse('website-ruta_update_vehicle', args=[vehicle_id]))

                # Eliminar imagen anterior
                file_to_delete = os.path.join(settings.MEDIA_ROOT, 'firetrucks', vehicle.image.name)
                #file_to_delete = default_storage.path('firetrucks/' + vehicle.image.name)
                #return HttpResponse(file_to_delete)

                # Verificar si el archivo existe antes de intentar eliminarlo
                if default_storage.exists(file_to_delete) and vehicle.image.name != "default-firetruck.png":
                    default_storage.delete(file_to_delete)
                    
                #Guardar imagen nueva
                fss = FileSystemStorage()
                current_date = datetime.now()
                image_name = f"{datetime.timestamp(current_date)}{os.path.splitext(str(request.FILES['imageField']))[1]}"
                upload = fss.save(f"firetrucks/{image_name}", file)
                #uploaded_file_url = fss.url(upload)
                
            #Intentar generar registro
            try:
                vehicle.name = request.POST.get('nameField')
                vehicle.description = request.POST.get('descriptionField')
                vehicle.plate = request.POST.get('plateField')
                vehicle.model = request.POST.get('modelField')
                vehicle.year = request.POST.get('yearField')
                vehicle.type_fire_trucks_id = request.POST.get('typeFireTruck')
                vehicle.image = image_name

                vehicle.save()
                messages.add_message(request, messages.SUCCESS, f"Vehículo modificado.")
                return HttpResponseRedirect(reverse('website-ruta_list_vehicles'))
            
            except Exception as e:
                messages.add_message(request, messages.WARNING, f"Ocurrió un error inesperado. Por favor, vuelva a intentarlo. {e}, {request.POST}")
                return HttpResponseRedirect(reverse('website-ruta_list_vehicles'))
                
        else:
            messages.add_message(request, messages.WARNING, f"No fue posible crear la unidad. Vuelva a intentarlo. {form.errors}")
            return HttpResponseRedirect(reverse('website-ruta_update_vehicle', args=[vehicle_id]))


    return render(request, 'Website/management_firetrucks/update_vehicle.html', {'form':form, 'types':types, 'type':type, 'id':vehicle.id})


#Vista - Eliminar vehículo
@login_required
def deleteVehicleView(request, vehicle_id):
    firetruck = FireTruck.objects.filter(id=vehicle_id).get()

    return render(request, 'Website/management_firetrucks/delete_vehicle.html', {'firetruck':firetruck})


#Función - Eliminar vehículo
@login_required
def deleteVehicle(request, vehicle_id):
    try:
        firetruck = FireTruck.objects.filter(id=vehicle_id).get()
        firetruck.delete()

        # Eliminar imagen anterior
        file_to_delete = os.path.join(settings.MEDIA_ROOT, 'firetrucks', firetruck.image.name)
        if default_storage.exists(file_to_delete) and firetruck.image.name != "default-firetruck.png":
            default_storage.delete(file_to_delete)

        messages.add_message(request, messages.SUCCESS, f'El vehículo {firetruck.name.title()} ha sido eliminado con éxito')
        return HttpResponseRedirect(reverse('website-ruta_list_vehicles'))
    except Exception:
        messages.add_message(request, messages.ERROR, f'No se ha podido eliminar el vehículo')
        return HttpResponseRedirect(reverse('website-ruta_list_vehicles'))