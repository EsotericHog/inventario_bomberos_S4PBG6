from ..models import FireTruck, Compartment, Inventory, InventoryMetadata, FireStation, Category, Status
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from ..forms import InventoryForm2
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count



#Vista - Lista de insumos
@login_required
def listInventoryView(request):
    fire_trucks = FireTruck.objects.filter(fire_stations=request.session.get('fire_station_id'))

    total_compartments = Compartment.objects.filter(fire_trucks__in=fire_trucks)

    local_inventory = Inventory.objects.filter(compartments__in=total_compartments).exclude(status_id = 4)

    total_inventory = local_inventory.count()

    return render(request, 'Website/management_inventory/list_items.html', {'items':local_inventory, 'total':total_inventory})



#Vista - Lista de insumos por lote
@login_required
def listInventoryManyView(request):
    fire_trucks = FireTruck.objects.filter(fire_stations=request.session.get('fire_station_id'))

    total_compartments = Compartment.objects.filter(fire_trucks__in=fire_trucks)

    local_inventory = Inventory.objects.filter(compartments__in=total_compartments)

    # Agrupar por nombre y contar la cantidad de cada grupo
    grouped_inventory = local_inventory.values(
        'inventorymetadata__name',
        'categories__name',
        ).annotate(count=Count('id'))

    return render(request, 'Website/management_inventory/list_items_many.html', {'items':grouped_inventory})



#Vista - Lista de insumos dados de baja
@login_required
def listInventoryCancelView(request):
    fire_trucks = FireTruck.objects.filter(fire_stations=request.session.get('fire_station_id'))

    total_compartments = Compartment.objects.filter(fire_trucks__in=fire_trucks)

    local_inventory = Inventory.objects.filter(compartments__in=total_compartments, status_id = 4)

    total_inventory = local_inventory.count()

    return render(request, 'Website/management_inventory/list_items_cancel.html', {'items':local_inventory, 'total':total_inventory})



#Vista - Lista de insumos unitarios por lote (detalle de cada lote)
@login_required
def listInventoryDetailView(request, name):
    batch = InventoryMetadata.objects.filter(name=name, inventory__compartments__fire_trucks__fire_stations_id=request.session.get('fire_station_id'))


    total_inventory = batch.count()

    return render(request, 'Website/management_inventory/list_items_many_detail.html', {'batch':batch, 'total':total_inventory, 'name_batch':name})



#Vista - Agregar insumo
@login_required
def addInventoryView(request, type):

    form = InventoryForm2(request.POST or None)

    station = request.session.get('fire_station_id')
    item_names = InventoryMetadata.objects.filter(inventory__compartments__fire_trucks__fire_stations=station).values_list('name', flat=True).distinct()
    # Convertir los nombres a una lista de Python
    item_names_list = list(item_names)

    #Marcas
    item_brands = InventoryMetadata.objects.filter(inventory__compartments__fire_trucks__fire_stations=station).values_list('brand', flat=True).distinct()
    item_brands_list = list(item_brands)
    #Modelo
    item_models = InventoryMetadata.objects.filter(inventory__compartments__fire_trucks__fire_stations=station).values_list('model', flat=True).distinct()
    item_models_list = list(item_models)

    #Cantidad
    quantity = None
    #sku
    sku_number = None


    if request.method == 'POST':
        if form.is_valid():
            #¿Se envió cantidad?
            if 'Quantity' in request.POST:
                if request.POST['Quantity'].isdigit():
                    quantity = request.POST['Quantity']
                    quantity = int(quantity)
                else:
                    messages.add_message(request, messages.WARNING, f"Cantidad incorrecta.")
                    return HttpResponseRedirect(reverse('website-ruta_add_item')) if type == 1 else HttpResponseRedirect(reverse('website-ruta_add_item_many'))
            
            #¿El código existe?
            if 'skuField' in request.POST:
                if request.POST['skuField'] != '':
                    sku_number = request.POST['skuField']

            if (Inventory.objects.filter(sku=sku_number).exclude(sku=None).exists()):
                messages.add_message(request, messages.WARNING, f"El código ya existe.")
                return HttpResponseRedirect(reverse('website-ruta_add_item')) if type == 1 else HttpResponseRedirect(reverse('website-ruta_add_item_many'))
            
            #¿Se seleccionó la categoría?
            if (request.POST['Category'] == '0'):
                messages.add_message(request, messages.WARNING, f"Debe seleccionar la categoría.")
                return HttpResponseRedirect(reverse('website-ruta_add_item')) if type == 1 else HttpResponseRedirect(reverse('website-ruta_add_item_many'))
            
            #¿Se seleccionó la ubicación (gaveta o contenedor)
            #Compartimento
            compartment = request.POST['Compartment'] if 'Compartment' in request.POST else "0"

            if ((compartment == "0") and (request.POST['Container'] == "0")):
                messages.add_message(request, messages.WARNING, f"Debe seleccionar la ubicación.")
                return HttpResponseRedirect(reverse('website-ruta_add_item')) if type == 1 else HttpResponseRedirect(reverse('website-ruta_add_item_many'))
            if ('Container' in request.POST and request.POST['Container'] != '0'):
                query = Inventory.objects.filter(id=request.POST['Container']).get()
                compartment = query.compartments_id
                container = request.POST['Container']
            else:
                compartment = request.POST.get('Compartment')
                container = None
            
            #Horas para mantención
            maintenance_hour = None
            #Fecha de expiración
            expire_date = None
            expire_notification = None
            #Programa de mantenimiento
            maintenance_program = None
            #Precio
            price = None

            
            #¿Se seleccionó la mantención programada?
            if ('checkboxMaintenance1' in request.POST):
                if request.POST['MaintenancePrograms'] == '0':
                    messages.add_message(request, messages.WARNING, f"Debe seleccionar la mantención programada.")
                    return HttpResponseRedirect(reverse('website-ruta_add_item')) if type == 1 else HttpResponseRedirect(reverse('website-ruta_add_item_many'))
                else:
                    maintenance_program = request.POST['MaintenancePrograms']
            
            #¿Se seleccionó la mantención por horas de uso?
            elif ('checkboxMaintenance2' in request.POST):
                if request.POST['maintenanceHourField']  == "":
                    messages.add_message(request, messages.WARNING, f"Debe indicar las horas de uso para realizar la mantención.")
                    return HttpResponseRedirect(reverse('website-ruta_add_item')) if type == 1 else HttpResponseRedirect(reverse('website-ruta_add_item_many'))
                else:
                    maintenance_hour = request.POST['maintenanceHourField']
            

            #¿Se seleccionó la expiración?
            if ('checkboxExpiration' in request.POST):
                if request.POST['expireDateField'] == "":
                    messages.add_message(request, messages.WARNING, f"Debe indicar la fecha de expiración.")
                    return HttpResponseRedirect(reverse('website-ruta_add_item')) if type == 1 else HttpResponseRedirect(reverse('website-ruta_add_item_many'))
                else:
                    expire_date = request.POST.get('expireDateField')
                    expire_notification = request.POST.get('expireNotificationField') if request.POST.get('expireNotificationField') != 0 else None

            #¿Precio?
            if not request.POST['priceField'] == "":
                price = request.POST['priceField']

  
            #Intentar generar registro
            if (quantity == "" or quantity == None):
                try:
                    i=Inventory.objects.create(sku=sku_number, categories_id=request.POST['Category'], compartments_id = compartment, status_id = 1, expire_at = expire_date, expire_notification = expire_notification, maintenance_hour = maintenance_hour, container_id = container, maintenance_programs_id = maintenance_program)
                    InventoryMetadata.objects.create(name = request.POST['nameField'], description = request.POST['descriptionField'], price = price, brand = request.POST['brandField'], model = request.POST['modelField'], inventory_id = i.id)
                    messages.add_message(request, messages.SUCCESS, f"Insumo creado con éxito.")
                    return HttpResponseRedirect(reverse('website-ruta_list_items'))
                except Exception as e:
                    messages.add_message(request, messages.WARNING, f"Ocurrió un error inesperado. Por favor, vuelva a intentarlo. {e}, {request.POST}")
                    return HttpResponseRedirect(reverse('website-ruta_list_items'))
            
            #Intentar generar registro por lote
            else:
                try:
                    for row in range(quantity):
                        i=Inventory.objects.create(sku=sku_number, categories_id=request.POST['Category'], compartments_id = compartment, status_id = 1, expire_at = expire_date, expire_notification = expire_notification, maintenance_hour = maintenance_hour, container_id = container, maintenance_programs_id = maintenance_program)
                        InventoryMetadata.objects.create(name = request.POST['nameField'], description = request.POST['descriptionField'], price = price, brand = request.POST['brandField'], model = request.POST['modelField'], inventory_id = i.id)

                    messages.add_message(request, messages.SUCCESS, f"Se generaron {quantity} registros")
                    return HttpResponseRedirect(reverse('website-ruta_list_items_many'))
                
                except Exception as e:
                    messages.add_message(request, messages.WARNING, f"Ocurrió un error inesperado. Por favor, vuelva a intentarlo. {e}, {request.POST}")
                    return HttpResponseRedirect(reverse('website-ruta_list_items_many'))
                
        else:
            messages.add_message(request, messages.WARNING, f"No fue posible crear el insumo. Vuelva a intentarlo. {form.errors}")
            return HttpResponseRedirect(reverse('website-ruta_add_item'))


    if type == 1:
        return render(request, 'Website/management_inventory/add_item.html', {'item_names':item_names_list, 'form':form, 'brands':item_brands_list, 'models':item_models_list})
    if type == 2:
        return render(request, 'Website/management_inventory/add_item_many.html', {'item_names':item_names_list, 'form':form, 'brands':item_brands_list, 'models':item_models_list})



#Vista - Modificar insumo
@login_required
def updateInventoryView(request, item_id, template, batch_name = None):
    item = InventoryMetadata.objects.filter(inventory_id=item_id).get()
    item_main = Inventory.objects.filter(id=item_id).get()
    # Accede al nombre del contenedor si existe
    container_name = None
    if item.inventory.container:
        container_name = item.inventory.container.inventorymetadata.name

    station = request.session.get('fire_station_id')
    
    item_names = InventoryMetadata.objects.filter(inventory__compartments__fire_trucks__fire_stations=station).values_list('name', flat=True).distinct()
    item_names_list = list(item_names)

    item_brands = InventoryMetadata.objects.filter(inventory__compartments__fire_trucks__fire_stations=station).values_list('brand', flat=True).distinct()
    item_brands_list = list(item_brands)

    item_models = InventoryMetadata.objects.filter(inventory__compartments__fire_trucks__fire_stations=station).values_list('model', flat=True).distinct()
    item_models_list = list(item_models)

    status = Status.objects.all()

    initial_data = {
        'skuField': item.inventory.sku,
        'nameField': item.name,
        'descriptionField': item.description,
        'priceField': item.price,
        'brandField': item.brand,
        'modelField': item.model,
        'expireDateField': item.inventory.expire_at,
        'expireNotificationField': item.inventory.expire_notification,
        'maintenanceHourField': item.inventory.maintenance_hour,
    }
    #Obtenemos el formulario
    form = InventoryForm2(request.POST or None, initial=initial_data)

    if request.method == 'POST':
        if form.is_valid():
            #¿El código existe?
            if request.POST['skuField'] == '':
                sku_number = None
            else:
                sku_number = request.POST['skuField']
            if (Inventory.objects.filter(sku=sku_number).exclude(sku=None).exists()):
                messages.add_message(request, messages.WARNING, f"El código ya existe.")
                return HttpResponseRedirect(reverse('website-ruta_update_item', args=[item_id, template, batch_name]))
            
            #¿Se seleccionó la categoría?
            if (request.POST['Category'] == '0'):
                messages.add_message(request, messages.WARNING, f"Debe seleccionar la categoría.")
                return HttpResponseRedirect(reverse('website-ruta_update_item', args=[item_id, template, batch_name]))
            
            #¿Se seleccionó la ubicación (gaveta o contenedor)
            if 'Compartment' not in request.POST and 'Container' not in request.POST:
                messages.add_message(request, messages.WARNING, f"Debe seleccionar la ubicación.")
                return HttpResponseRedirect(reverse('website-ruta_update_item', args=[item_id, template, batch_name]))
            if ('Container' in request.POST and request.POST['Container'] != '0'):
                query = Inventory.objects.filter(id=request.POST['Container']).get()
                compartment = query.compartments_id
                container = request.POST['Container']
            else:
                compartment = request.POST['Compartment']
                container = None
            
            #Horas para mantención
            maintenance_hour = None
            #Fecha de expiración
            expire_date = None
            expire_notification = None
            #Programa de mantenimiento
            maintenance_program = None
            #Precio
            price = None

            
            #¿Se seleccionó la mantención programada?
            if ('checkboxMaintenance1' in request.POST):
                if request.POST['MaintenancePrograms'] == '0':
                    messages.add_message(request, messages.WARNING, f"Debe seleccionar la mantención programada.")
                    return HttpResponseRedirect(reverse('website-ruta_update_item', args=[item_id, template, batch_name]))
                else:
                    maintenance_program = request.POST['MaintenancePrograms']
            
            #¿Se seleccionó la mantención por horas de uso?
            elif ('checkboxMaintenance2' in request.POST):
                if request.POST['maintenanceHourField']  == "":
                    messages.add_message(request, messages.WARNING, f"Debe indicar las horas de uso para realizar la mantención.")
                    return HttpResponseRedirect(reverse('website-ruta_update_item', args=[item_id, template, batch_name]))
                else:
                    maintenance_hour = request.POST['maintenanceHourField']
            

            #¿Se seleccionó la expiración?
            if ('checkboxExpiration' in request.POST):
                if request.POST['expireDateField'] == "":
                    messages.add_message(request, messages.WARNING, f"Debe indicar la fecha de expiración.")
                    return HttpResponseRedirect(reverse('website-ruta_update_item', args=[item_id, template, batch_name]))
                else:
                    expire_date = request.POST.get('expireDateField')
                    expire_notification = request.POST.get('expireNotificationField') if request.POST.get('expireNotificationField') != 0 else None

            #¿Precio?
            if not request.POST['priceField'] == "":
                price = request.POST['priceField']

  
            #Intentar generar registro
            try:
                item_main.sku = sku_number
                item_main.categories_id = request.POST['Category']
                item_main.compartments_id = compartment
                item_main.expire_at = expire_date
                item_main.expire_notification = expire_notification
                item_main.maintenance_hour = maintenance_hour
                item_main.container_id = container
                item_main.maintenance_programs_id = maintenance_program

                item.name = request.POST['nameField']
                item.description = request.POST['descriptionField']
                item.price = price
                item.brand = request.POST['brandField']
                item.model = request.POST['modelField']
                item.inventory_id = item_id

                item_main.save()
                item.save()

                
                messages.add_message(request, messages.SUCCESS, f"Insumo modificado con éxito.")
                return HttpResponseRedirect(reverse('website-ruta_list_items')) if template == 1 else HttpResponseRedirect(reverse('website-ruta_list_items_many_detail', args=[batch_name]))
            except Exception as e:
                messages.add_message(request, messages.WARNING, f"Ocurrió un error inesperado. Por favor, vuelva a intentarlo. {e}, {request.POST}")
                return HttpResponseRedirect(reverse('website-ruta_list_items')) if template == 1 else HttpResponseRedirect(reverse('website-ruta_list_items_many_detail', args=[batch_name]))
                
        else:
            messages.add_message(request, messages.WARNING, f"No fue posible crear el insumo. Vuelva a intentarlo. {form.errors}")
            return HttpResponseRedirect(reverse('website-ruta_update_item', args=[item_id, template, batch_name]))


    return render(request, 'Website/management_inventory/update_item.html', {'form':form, 'item':item})



#Vista - Dar de baja insumo
@login_required
def cancelInventoryView(request, item_id, template, batch_name = None):
    item = InventoryMetadata.objects.filter(inventory_id=item_id).get()

    return render(request, 'Website/management_inventory/cancel_item.html', {'item':item, 'template':template, 'batch_name':batch_name})



#Función - Dar de baja insumo
@login_required
def cancelInventory(request, item_id, template, batch_name = None):
    cancel_place = Compartment.objects.filter(name="DESCONTINUADO").get()
    item = Inventory.objects.filter(id=item_id).get()
    item.status_id = 4
    item.compartments_id = cancel_place.id
    item.compartments.fire_trucks.id = cancel_place.fire_trucks_id
    item.save()

    messages.add_message(request, messages.SUCCESS, f"Insumo descontinuado con éxito")
    return HttpResponseRedirect(reverse('website-ruta_list_items')) if template == 1 else HttpResponseRedirect(reverse('website-ruta_list_items_many_detail' , args=[batch_name]))



#Vista - Prestar insumo
def lendingIventoryView(request):
    pass