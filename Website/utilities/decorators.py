from functools import wraps
from django.contrib.auth import authenticate
from ..models import Profile, UserMetadata
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse


#Validar que el usuario sea Administrador
def administrador():
    def admin_required(function):
        @wraps(function)
        def _decorator(request, *args, **kwargs):
            #Obtención del rol Administrador
            admin_profile = Profile.objects.filter(name="ADMINISTRADOR").get()
            #Obtención del registro en user_metadata
            user_metadata = UserMetadata.objects.filter(user_id = request.session.get('user_metadata_id')).get()

            if (user_metadata.profiles_id == admin_profile.id):
                return function(request, *args, **kwargs)
            else:
                messages.warning(request, "No cuentas con los permisos para acceder a esta funcionalidad.")
                return HttpResponseRedirect(reverse('website-ruta_home'))
            
        return _decorator
    return admin_required