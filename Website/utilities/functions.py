import os
from datetime import datetime

#MODULO DE UTILIDADES: FUNCIONES VARIAS PARA UTILIZAR EN LA APP

#Validar extensión de archivo para imágenes válidas
def getExtension(file):
    extension = os.path.splitext(str(file))[1]
    if (extension == ".png" or extension == ".PNG"):
        return True
    elif (extension == ".jpg" or extension == ".JPG"):
        return True
    elif (extension == ".jpeg" or extension == ".JPEG"):
        return True
    else:
        return False