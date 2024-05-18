from ..models import FireTruck, Compartment
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from ..forms import CompartmentForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count
from ..utilities.decorators import administrador


#Vista - Lista de gavetas
@login_required
def listCompartmentsView(request):
    firetrucks = FireTruck.objects.filter(fire_stations_id = request.session.get('fire_station_id')).exclude(id = 3)
    compartments = Compartment.objects.filter(fire_trucks__in=firetrucks).annotate(total_items=Count('inventory'))
    count_compartments = compartments.count()

    #for firetruck in firetrucks:
    #    compartments = firetruck.compartment_set.all().annotate(total_items=Count('inventory'))

    #    for compartment in compartments:
    #        compartment.per = compartment.quantity and (compartment.total_items * 100 / compartment.quantity) or 0

    #    firetruck.compartments_with_per = compartments


    #firetrucks = FireTruck.objects.filter(fire_stations_id=request.session.get('fire_station_id')).exclude(id=3)

    for firetruck in firetrucks:
        firetruck.compartments_with_per = firetruck.compartment_set.all().annotate(total_items=Count('inventory'))

        for compartment in firetruck.compartments_with_per:
            compartment.per = compartment.total_items * 100 / compartment.quantity if (compartment.total_items and compartment.quantity) else 0

    return render(request, 'Website/management_compartments/list_compartments.html', {'firetrucks':firetrucks, 'compartments':compartments, 'total':count_compartments})


#Vista - Compartimento por unidad (Eliminar después)
@login_required
def listCompartmentForVehicleView(request, vehicle_id):
    firetrucks = FireTruck.objects.filter(fire_stations_id = request.session.get('fire_station_id')).exclude(id = 3)
    firetruck = FireTruck.objects.filter(id = vehicle_id).get()
    compartments = Compartment.objects.filter(fire_trucks_id = vehicle_id).annotate(total_items=Count('inventory'))
    count_compartments = compartments.count()

    return render(request, 'Website/management_compartments/list_compartments_for_vehicle.html', {'firetrucks':firetrucks, 'compartments':compartments, 'count_compartments':count_compartments, 'firetruck':firetruck})



#Vista - Agregar gaveta
@login_required
def addCompartmentView(request):
    form = CompartmentForm(request.POST or None, request.FILES or None)
    #firetrucks = FireTruck.objects.filter(fire_stations_id = request.session.get('fire_station_id'))

    if request.method == 'POST':
        if form.is_valid():
            #¿Se seleccionó la unidad bomberil?
            if (request.POST['FireTruck'] == '0'):
                messages.add_message(request, messages.WARNING, f"Debe seleccionar la unidad bomberil.")
                return HttpResponseRedirect(reverse('website-ruta_add_compartment'))
            
            #Se estableció cantidad establecida?
            if(request.POST['quantityField'] == None or request.POST['quantityField'] == ""):
                quantity = 0
            else:
                quantity = request.POST['quantityField']
                
            #Intentar generar registro
            try:
                Compartment.objects.create(name=request.POST['nameField'], description=request.POST['descriptionField'], quantity=quantity, fire_trucks_id = request.POST['FireTruck'])
                messages.add_message(request, messages.SUCCESS, f"Gaveta asignada con éxito.")
                return HttpResponseRedirect(reverse('website-ruta_list_compartments'))
            except Exception as e:
                messages.add_message(request, messages.WARNING, f"Ocurrió un error inesperado. Por favor, vuelva a intentarlo. {e}, {request.POST}")
                return HttpResponseRedirect(reverse('website-ruta_list_compartments'))
                
        else:
            messages.add_message(request, messages.WARNING, f"No fue posible crear la gaveta. Vuelva a intentarlo. {form.errors}")
            return HttpResponseRedirect(reverse('website-ruta_add_compartment'))

    return render(request, 'Website/management_compartments/add_compartment.html', {'form':form})



#Vista - Modificar gaveta
@login_required
def updateCompartmentView(request, compartment_id):
    #Obtener registro a modificar
    compartment = Compartment.objects.filter(id=compartment_id).get()
    #Vehículos
    firetrucks = FireTruck.objects.filter(fire_stations_id = request.session.get('fire_station_id')).exclude(id=compartment.fire_trucks_id)
    firetruck = FireTruck.objects.filter(id=compartment.fire_trucks_id).get()
    #Valores iniciales para los campos del formulario
    initial_data = {
        'nameField': compartment.name,
        'descriptionField': compartment.description,
        'quantity': compartment.quantity,
    }
    #Formulario
    form = CompartmentForm(request.POST or None, request.FILES or None, initial=initial_data)

    if request.method == 'POST':
        if form.is_valid():
            #¿Se seleccionó la unidad bomberil?
            if (request.POST['FireTruck'] == '0'):
                messages.add_message(request, messages.WARNING, f"Debe seleccionar la unidad bomberil.")
                return HttpResponseRedirect(reverse('website-ruta_update_compartment', args=[compartment_id]))
            
            #Se estableció cantidad establecida?
            if(request.POST['quantityField'] == None or request.POST['quantityField'] == ""):
                quantity = 0
            else:
                quantity = request.POST['quantityField']
            
            #Intentar generar registro
            try:
                compartment.name = request.POST.get('nameField')
                compartment.description = request.POST.get('descriptionField')
                compartment.quantity = quantity
                compartment.fire_trucks_id = request.POST.get('FireTruck')

                compartment.save()
                messages.add_message(request, messages.SUCCESS, f"Gaveta modificada.")
                return HttpResponseRedirect(reverse('website-ruta_list_compartments'))
            
            except Exception as e:
                messages.add_message(request, messages.WARNING, f"Ocurrió un error inesperado. Por favor, vuelva a intentarlo. {e}, {request.POST}")
                return HttpResponseRedirect(reverse('website-ruta_list_compartments'))
                
        else:
            messages.add_message(request, messages.WARNING, f"No fue posible crear la unidad. Vuelva a intentarlo. {form.errors}")
            return HttpResponseRedirect(reverse('website-ruta_update_compartment', args=[compartment_id]))


    return render(request, 'Website/management_compartments/update_compartment.html', {'form':form, 'firetrucks':firetrucks, 'firetruck':firetruck, 'compartment':compartment})



#Vista - Eliminar gaveta
@login_required
def deleteCompartmentView(request, compartment_id):
    compartment = Compartment.objects.filter(id=compartment_id).get()

    return render(request, 'Website/management_compartments/delete_compartment.html', {'compartment':compartment})



#Función - Eliminar gaveta
@login_required
def deleteCompartment(request, compartment_id):
    try:
        compartment = Compartment.objects.filter(id=compartment_id).get()
        compartment.delete()

        messages.add_message(request, messages.SUCCESS, f'Gaveta "{compartment.name.title()}" ha sido eliminada con éxito')
        return HttpResponseRedirect(reverse('website-ruta_list_compartments'))
    except Exception:
        messages.add_message(request, messages.ERROR, f'No se ha podido eliminar la gaveta')
        return HttpResponseRedirect(reverse('website-ruta_list_compartments'))