//RUT
//function formValidateRut(inputElement) {
//    let rut = inputElement.value;
//
//    let checkDigit = rut.slice(-1);
//    let cleanRut = rut.slice(0, -1).replace(/\D/g, '');
//    
//    let array = cleanRut.split('').reverse();
//    let acumulator = 0;
//    let multiplicator = 2;
//
//
//    for(let number of array) {
//        acumulator += parseInt(number) * multiplicator;
//        multiplicator++;
//        //Necesitamos resetear el multiplicador a 2 , ya que la fórmula indica que el incremento es hasta el 7
//        if(multiplicator == 8) {
//            multiplicator = 2;
//        }
//    }
//    
//    //Aquí obtenemos el resto al dividir la suma total por 11
//    let digit = 11 - (acumulator % 11);
//
//    //Si el dígito verificador es 11, se convierte a 0
//    if(digit == 11) {
//        digit = '0';
//    }
//
//    //Si el dígito verificador es 10, se convierte a k
//    else if(digit == 10) {
//        digit = 'K';
//    }
//
//    if (digit == checkDigit && cleanRut.length >=8) {
//        return true;
//    }
//    else {
//        return false;
//    }
//};
//NUEVO MÉTODO DE EVENTO PARA VALIDAR DIGITO VERIFICADOR DE RUT
function formValidateRut(inputElement) {
    let rut = inputElement.value;
    let cleanRut = rut.replace(/\D/g, '');

    digit = calculateDigitVerificator(cleanRut);
    digitoVerificador = document.getElementById("digitoVerificador");
    digitoVerificador.value = digit;

    if (cleanRut.length >=8 && (digit != null || digit != "")) {
        return true
    }
    else {
        return false
    }
};


//NOMBRE, APELLIDO
function formValidateAlpha(inputElement) {
    let dynamicValue = inputElement.value;
    let format = /^[a-zA-Z\s]+$/;


    if (dynamicValue.length >= 2 && format.test(dynamicValue) == true) {
       return true;
    }
    else {
        return false;
    }
}


//EMAIL
function formValidateEmail(inputElement) {
    let dynamicValue = inputElement.value;
    let format = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;

    if(format.test(dynamicValue)) {
        return true;
    }
    else {
        return false;
    }
}


//CONTRASEÑA
function formValidatePassword(inputElement) {
    let dynamicValue = inputElement.value;
    //Mínimo 8 caracteres
    let lengthValue = dynamicValue.length >= 12 ? true : false;
    // Debe contener al menos una letra, al menos un número, al menos un caracter especial y al menos una letra mayúscula
    let letterValue = /[a-zA-Z]/.test(dynamicValue);
    let numberValue = /[0-9]/.test(dynamicValue);
    let specialCharValue = /[!@#$%^&*(),.?":{}|<>]/.test(dynamicValue);
    let uppercaseValue = /[A-Z]/.test(dynamicValue);

    if(lengthValue && letterValue && numberValue && specialCharValue && uppercaseValue) {
        return true
    }
    else {
        return false
    }
}


//CONFIRMAR CONTRASEÑA
function formConfirmPassword(inputElement1, inputElement2) {
    let password1 = inputElement1.value;
    let password2 = inputElement2.value;

    if (password1 == password2) {
        return true
    }
    else {
        return false
    }
}


//TELEFONO
function formValidateNumber(inputElement) {
    let dynamicValue = inputElement.value;

    // Dato opcional
    if (dynamicValue.length === 0) {
        console.log("Es cero");
        return true
    }
    
    if (dynamicValue.length >= 8 && /^[0-9]+$/.test(dynamicValue)) {
        console.log("Longitud correcta");
        return true
    }
    if (dynamicValue.length !== 8 && dynamicValue.length !== 0) {
        console.log("teléfono incorrecto");
        return false
    }
}


//SELECTS
function formValidateSelect(selectElement) {
    let dynamicValue = selectElement.value;

    if (dynamicValue != 0) {
        return true
    }
    else {
        return false
    }
}

//VALIDACION DE FORMULARIO COMPLETO ANTES DE ENVIAR AL SERVIDOR
function formValidation() {
    //let rut = document.getElementById('input-rut');
    //let name = document.getElementById('input-name');
    //let lastname = document.getElementById('input-lastname');
    //let email = document.getElementById('input-email');
    //let password = document.getElementById('input-password');
    //let confirm_password = document.getElementById('input-confirm_password');
    //let number = document.getElementById('input-number');
    //let profile = document.getElementById('selectProfile');
    //let region = document.getElementById('selectRegion');
    //let comune = document.getElementById('selectComune');
    //let station = document.getElementById('selectStation');

    if (!formValidateRut(inputRut)) {
        console.log("Rut no válido")
    }
    if (!formValidateAlpha(inputName)) {
        console.log("Nombre no válido")
    }
    if (!formValidateAlpha(inputLastName)) {
        console.log("Apellido no válido")
    }
    if (!formValidateEmail(inputEmail)) {
        console.log("Email no válido")
    }
    if (!formValidatePassword(inputPassword)) {
        console.log("Contraseña no válido")
    }
    if (!formConfirmPassword(inputPassword, inputConfirmPassword)) {
        console.log("Las contraseñas no coinciden")
    }
    if (!formValidateNumber(inputNumber)) {
        console.log("Número no válido")
    }
    if (!formValidateSelect(selectProfile)) {
        console.log("Perfil no válido")
    }
    if (!formValidateSelect(selectRegion)) {
        console.log("Región no válido")
    }
    if (!formValidateSelect(selectComune)) {
        console.log("Comuna no válido")
    }
    if (!formValidateSelect(selectStation)) {
        console.log("Estación no válido")
    }
    
    if(formValidateRut(inputRut) && formValidateAlpha(inputName) && formValidateAlpha(inputLastName) && formValidateEmail(inputEmail) && formValidatePassword(inputPassword) && formConfirmPassword(inputPassword, inputConfirmPassword) && formValidateNumber(inputNumber) && formValidateSelect(selectProfile) && formValidateSelect(selectRegion) && formValidateSelect(selectComune) && formValidateSelect(selectStation)) {
        return true
    }
}

//Selección del formulario
const signupForm = document.getElementById("signup-form");
if(signupForm) {
    signupForm.addEventListener("submit", (event) => {
        if (!formValidation()) {
            event.preventDefault();
            console.log("Creación de usuario incorrecta");
        }
        else {
            //Unir el rut
            inputRut.value = inputRut.value + "-" + document.getElementById("digitoVerificador").value;
        }
    });
}
//Botón success del formulario
const signupButtonForm = document.getElementById("signup-form-button");