from django.core.exceptions import ValidationError

#VALIDACIONES
#Contraseña - mínimo 8 caracteres, 1 número y 1 letra
def validate_password(value):
    if len(value) < 8:
        raise ValidationError('La contraseña debe tener al menos 8 caracteres.')
    if not any(char.isalpha() for char in value):
        raise ValidationError('La contraseña debe contener al menos una letra.')
    if not any(char.isdigit() for char in value):
        raise ValidationError('La contraseña debe contener al menos un número.')

#Nombre y apellido
def custom_validate_name(value):
    if not all(char.isalpha() or char.isspace() for char in value):
        raise ValidationError('El nombre debe contener solo caracteres alfabéticos y espacios.')
    
#Teléfono
def validate_phone(value):
    if not value.isdigit():
        raise ValidationError('El teléfono solo debe contener números enteros.')

#Día del mes
def validate_month_day(value):
    try:
        frequency = int(value)
        if not (1 <= frequency <= 30):
            raise ValidationError('Día incorrecto')
    except ValueError:
        raise ValidationError('Valor incorrecto. Debe ser un número entero.')
    
#Extensiones de archivo (imágenes)
def validate_image_extension(value):
    if(value):
        valid_extensions = ['.jpg', '.jpeg', '.png']
        extension = value.name.split('.')[-1].lower()
        if not extension in valid_extensions:
            raise ValidationError('Sólo se permiten archivos jpg, jpeg y png')
    else:
        pass