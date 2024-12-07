from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from datetime import date, datetime, timedelta
import time
from django.conf import Settings
from ..forms import *
from ..models import Profile, UserMetadata
from ..mail import send_complete_signup_mail

#VISTAS DE ACCESO
#Vista - Iniciar sesión
def loginView(request):
    if not (request.user.is_authenticated):
        form = LoginForm(request.POST or None)
        if (request.method == 'POST'):
            if form.is_valid():
                rut_cleaned = form.cleaned_data['rutField']
                password_cleaned = form.cleaned_data['passwordField']
                user = authenticate(request, username=rut_cleaned, password=password_cleaned)

                if user is not None:
                    #Logear al usuario
                    login(request, user)
                    messages.success(request, "Sesión iniciada con éxito")
                    try:
                        #Obtención de registro en user_metadata y almacenamiento en la sesión
                        metadata = UserMetadata.objects.filter(user_id=request.user.id).get()
                        request.session['user_metadata_id']=metadata.id
                        #Obtención de ID y nombre de la estación
                        request.session['fire_station_id']=metadata.fire_stations_id
                        request.session['fire_station_name']=metadata.fire_stations.name

                    except UserMetadata.DoesNotExist:
                        messages.warning(request, "No se encontró la información completa del usuario")


                    return HttpResponseRedirect(reverse('website-ruta_home'))

                else:
                    messages.add_message(request, messages.WARNING, f"Los datos ingresados no son válidos. Vuelva a intentarlo")
                    return HttpResponseRedirect(reverse('website-ruta_redirect_login'))

        return render(request, 'Website/access/login.html', {'form':form})
    else:
        return HttpResponseRedirect(reverse('website-ruta_home'))
        

#Vista - Crear cuenta
def signupView(request):
    if request.user.is_authenticated:
        print("El usuario ya está autenticado.")
        return HttpResponseRedirect(reverse('website-ruta_home'))

    form = SignupForm(request.POST or None)
    
    if request.method == 'POST':
        if form.is_valid():
            #¿El rut existe?
            if (User.objects.filter(username=request.POST['rutField']).exists()):
                messages.add_message(request, messages.WARNING, f"El rut ya está en uso.")
                return HttpResponseRedirect(reverse('website-ruta_signup'))
            
            #¿Las contraseñas coinciden?
            elif(request.POST['passwordField'] != request.POST['confirmPasswordField']):
                messages.add_message(request, messages.WARNING, f"Las contraseñas no coinciden")
                return HttpResponseRedirect(reverse('website-ruta_signup'))
            
            #¿Los campos selects tiene valores válidos?
            elif(request.POST['profile'] == 0 or request.POST['station'] == 0):
                messages.add_message(request, messages.WARNING, f"Faltan campos que son obligatorios. Por favor, envíe el formulario completo")
                return HttpResponseRedirect(reverse('website-ruta_signup'))

            else:
                #Crear registro en la tabla auth_user
                u=User.objects.create_user(username=request.POST['rutField'], password=request.POST['passwordField'], email=request.POST['emailField'], first_name=request.POST['nameField'], last_name=request.POST['lastNameField'], is_active=0)
                #Crear registro en la tabla de metadata
                UserMetadata.objects.create(number=request.POST['numberField'], fire_stations_id=request.POST['station'], profiles_id=request.POST['profile'], user_id=u.id)
                messages.add_message(request, messages.SUCCESS, f"Cuenta creada a la espera de aprobación.")

                #Enviar correo
                send_complete_signup_mail(to=request.POST['emailField'], name=request.POST['nameField'])

                return HttpResponseRedirect(reverse('website-ruta_signup_success'))
        
        else:
            messages.add_message(request, messages.WARNING, f"No fue posible crear la cuenta. Vuelva a intentarlo.")
            #return HttpResponse(f"{form} - {form.errors} - Perfil = {request.POST['profileField']} - Estación = {request.POST['stationField']}")
            return HttpResponseRedirect(reverse('website-ruta_signup'))
        
    return render(request, 'Website/access/signup.html', {'form':form})


#Vista - Crear cuenta (POST)
def signupSuccessView(request):
    return render(request, 'Website/access/signup_success.html', {})


#Vista - Cerrar sesión
def logoutView(request):
    logout(request)
    messages.add_message(request, messages.SUCCESS, f'Se cerró la sesión exitosamente')
    return HttpResponseRedirect(reverse('website-ruta_redirect_login'))