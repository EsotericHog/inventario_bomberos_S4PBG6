import os
import shutil
from ..models import FireTruck
from django.conf import settings
from pathlib import Path
from datetime import datetime, date, timedelta

ROUTE = settings.ROUTE
ROUTE2 = settings.ROUTE2

#Mover imagen de vehículos bomberiles desde /media a /assets
def moveImageFireTruck(file, id):
    if existFileMedia(file):
        current_date = datetime.now()
        name = f"{datetime.timestamp(current_date)}{os.path.splitext(str(file))[1]}"
        shutil.move(f"{ROUTE}Django_S4PBG6/media/firetrucks/{file}", f"{ROUTE2}assets/uploads/firetrucks/{name}")
        FireTruck.objects.filter(id=id).update(image=name)

#Verificar si el archivo existe en /assets/
def existFile(folder, file):
    try:
        route = f"{ROUTE}Django_S4PBG6/assets/uploads/{folder}/{file}"
        fileObj = Path(route)
        return fileObj.is_file()
    except Exception as e:
        return False
    
#Verificar si el archivo existe en /media/
def existFileMedia(file):
    try:
        route = f"{ROUTE}Django_S4PBG6/media/firetrucks/{file}"
        fileObj = Path(route)
        return fileObj.is_file()
    except Exception as e:
        return False