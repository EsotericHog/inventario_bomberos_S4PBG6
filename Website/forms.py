from django import forms
from .models import UserMetadata, Inventory, TypeFireTruck
from .validators import *
from django.utils.html import format_html

#FORMULARIOS
#Formulario destinado a extender el que trae Django Admin por defecto para crear usuarios. De esta forma incluyo los campos correspondientes a la metadata de usuarios
class UserMetadataForm(forms.ModelForm):
    class Meta:
        model = UserMetadata
        fields = '__all__'


#Para extender el de inventario
class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = '__all__'


#Iniciar sesión
class LoginForm(forms.Form):
    rutField = forms.CharField(required=True, widget=forms.TextInput(attrs={'id':'input-rut', 'placeholder':'RUT', 'autocomplete':'off'}))
    passwordField = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'id':'input-password', 'placeholder':'Contraseña'}))


#Crear usuario
class SignupForm(forms.Form):
    rutField = forms.CharField(required=True, widget=forms.TextInput(attrs={'id':'input-rut', 'placeholder':'RUT'}))
    nameField = forms.CharField(required=True, widget=forms.TextInput(attrs={'id':'input-name', 'placeholder':'Nombre'}))
    lastNameField = forms.CharField(required=True, widget=forms.TextInput(attrs={'id':'input-lastname', 'placeholder':'Apellido'}))
    emailField = forms.EmailField(required=True, widget=forms.TextInput(attrs={'id':'input-email', 'placeholder':'Correo electrónico'}))
    passwordField = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'id':'input-password', 'placeholder':'Contraseña'}))
    confirmPasswordField = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'id':'input-confirm_password', 'placeholder':'Confirmar contraseña'}))
    numberField = forms.CharField(required=False, widget=forms.TextInput(attrs={'id':'input-number', 'placeholder':'Teléfono (Opcional)'}))


#Actualizar usuario
class UpdateUserForm(forms.Form):
    rutField = forms.CharField(required=True, widget=forms.TextInput(attrs={'id':'input-rut', 'placeholder':'RUT'}))
    nameField = forms.CharField(required=True, widget=forms.TextInput(attrs={'id':'input-name', 'placeholder':'Nombre'}))
    lastNameField = forms.CharField(required=True, widget=forms.TextInput(attrs={'id':'input-lastname', 'placeholder':'Apellido'}))
    emailField = forms.EmailField(required=True, widget=forms.TextInput(attrs={'id':'input-email', 'placeholder':'Correo electrónico'}))
    numberField = forms.CharField(required=False, widget=forms.TextInput(attrs={'id':'input-number', 'placeholder':'Teléfono (Opcional)'}))


#Crear vehículo
class FireTruckForm(forms.Form):
    nameField = forms.CharField(required=True, widget=forms.TextInput(attrs={'id':'inputTitle', 'placeholder':'Nombre'}))
    descriptionField = forms.CharField(required=False, widget=forms.Textarea(attrs={'id':'fireTruckDescription', 'placeholder':'Descripción (opcional)'}))
    plateField = forms.CharField(required=True, widget=forms.TextInput(attrs={'id':'fireTruckPlate', 'placeholder':'Patente'}))
    modelField = forms.CharField(required=False, widget=forms.TextInput(attrs={'id':'inputModel', 'placeholder':'Modelo (opcional)'}))
    yearField = forms.CharField(required=False, widget=forms.TextInput(attrs={'id':'inputYear', 'placeholder':'Año (opcional)'}))
    imageField = forms.CharField(required=False, widget=forms.TextInput(attrs={'type':'file', 'id':'inputImage', 'class':'form-control'}))


#Gavetas
class CompartmentForm(forms.Form):
    nameField = forms.CharField(required=True, widget=forms.TextInput(attrs={'id':'inputTitle', 'placeholder':'Nombre'}))
    descriptionField = forms.CharField(required=False, widget=forms.Textarea(attrs={'id':'fireTruckDescription', 'placeholder':'Descripción (opcional)'}))
    quantityField = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'id':'inputNumber', 'placeholder':'Cantidad esperada (opcional)'}))


#Insumos
class InventoryForm2(forms.Form):
    skuField = forms.CharField(required=False, widget=forms.NumberInput(attrs={'id':'inputSku', 'placeholder':'Código (Recomendado)'}))
    nameField = forms.CharField(required=True, widget=forms.TextInput(attrs={'id':'inputTitle', 'type':'text', 'list':'item_names', 'placeholder':'Nombre'}))
    descriptionField = forms.CharField(required=False, widget=forms.Textarea(attrs={'id':'fireTruckDescription', 'placeholder':'Descripción (opcional)'}))
    priceField = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'id':'inputPrice', 'placeholder':'Precio (opcional)'}))
    brandField = forms.CharField(required=False, widget=forms.TextInput(attrs={'id':'inputBrand', 'placeholder':'Marca (opcional)', 'list':'item_brands'}))
    modelField = forms.CharField(required=False, widget=forms.TextInput(attrs={'id':'inputModel', 'placeholder':'Modelo (opcional)', 'list':'item_models'}))
    expireDateField = forms.CharField(required=False, widget=forms.TextInput(attrs={'id':'inputExpireDate', 'type':'date', 'hidden':'true'}))
    expireNotificationField = forms.CharField(required=False, widget=forms.TextInput(attrs={'id':'inputExpireNotification', 'type':'number', 'min':'0', 'max':'360', 'hidden':'true'}))
    #maintenanceHourField = forms.CharField(required=False, widget=forms.TextInput(attrs={'id':'inputMaintenanceHour', 'type':'number', 'placeholder':'Cada cuántas horas de uso se debe hacer mantenimiento', 'hidden':'true'}))