//GESTION DEL RUT
//FUNCIÓN DE EVENTO PARA FORMATEAR RUT EN ENTRADA DE TEXTO INPUT
function formatRut(inputElement, type) {
    let dynamicValue = inputElement.value;

    //Formulario Iniciar sesión
    if (type === "login") {
        //Elimina cualquier caracter que no sea un número o la letra 'k' o 'K'
        dynamicValue = dynamicValue.replace(/[^0-9kK]/g, '').toUpperCase();
        
        // Limitar la cadena a un máximo de 9 caracteres
        if (dynamicValue.length > 9) {
            dynamicValue = dynamicValue.slice(0, 9);
        }

        //Aplicar formato de puntos y guión
        if (dynamicValue.length > 1) {
            let last = dynamicValue.slice(-1);
            dynamicValue = dynamicValue.slice(0, -1);
            dynamicValue = dynamicValue.replace(/\B(?=(\d{3})+\b)/g, '.') + "-" + last;
        }
    }

    // Formulario Crear cuenta
    if (type === "signup") {
        // Permitir sólo números
        dynamicValue = dynamicValue.replace(/[^0-9]/g, '');

        //Limitar la cadena a un máximo de 8 caracteres
        if (dynamicValue.length > 8) {
            dynamicValue = dynamicValue.slice(0, 8);
        }

        //Aplicar formato de puntos y guión
        if (dynamicValue.length > 1) {
            dynamicValue = dynamicValue.replace(/\B(?=(\d{3})+\b)/g, '.');
        }
    }

    // Asignar valor formateado
    inputElement.value = dynamicValue;
}

////MÉTODO DE EVENTO PARA VALIDAR DIGITO VERIFICADOR DE RUT
//function validateRut(inputElement, goodIcon, badIcon = document.createElement("i")) {
//    let rut = inputElement.value;
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
//
//    if (digit == checkDigit && cleanRut.length >=8) {
//        goodIcon.classList.replace("checkIconHidden", "checkIcon");
//        badIcon.classList.replace("badIcon", "badIconHidden")
//    }
//    else {
//        goodIcon.classList.replace("checkIcon", "checkIconHidden");
//        badIcon.classList.replace("badIconHidden", "badIcon");
//    }
//};




//NUEVO MÉTODO DE EVENTO PARA VALIDAR DIGITO VERIFICADOR DE RUT
function validateRut(inputElement, goodIcon, badIcon = document.createElement("i")) {
    let rut = inputElement.value;
    let cleanRut = rut.replace(/\D/g, '');

    digit = calculateDigitVerificator(cleanRut);
    digitoVerificador = document.getElementById("digitoVerificador");
    digitoVerificador.value = digit;
    
    if (inputElement.value === "") {
        digitoVerificador.value = "";

    }

    if (cleanRut.length >=8 && digit != null) {
        goodIcon.classList.replace("checkIconHidden", "checkIcon");
        badIcon.classList.replace("badIcon", "badIconHidden")
    }
    else {
        goodIcon.classList.replace("checkIcon", "checkIconHidden");
        badIcon.classList.replace("badIconHidden", "badIcon");
    }
};
//NUEVO RUT DIGITO VERIFICADOR
function calculateDigitVerificator(cleanRut) {
    let array = cleanRut.split('').reverse();
    let acumulator = 0;
    let multiplicator = 2;


    for(let number of array) {
        acumulator += parseInt(number) * multiplicator;
        multiplicator++;
        //Necesitamos resetear el multiplicador a 2 , ya que la fórmula indica que el incremento es hasta el 7
        if(multiplicator == 8) {
            multiplicator = 2;
        }
    }
    
    //Aquí obtenemos el resto al dividir la suma total por 11
    let digit = 11 - (acumulator % 11);

    //Si el dígito verificador es 11, se convierte a 0
    if(digit == 11) {
        digit = '0';
    }

    //Si el dígito verificador es 10, se convierte a k
    else if(digit == 10) {
        digit = 'K';
    }

    return digit
};




//GESTIÓN NOMBRE Y APELLIDO
//Formato cadena alfabética - sólo letras y espacios
function formatAlpha(inputElement) {
    let dynamicValue = inputElement.value;

    //Eliminar caracteres numéricos 
    dynamicValue = dynamicValue.replace(/[^a-zA-Z\s]+/g, '').toUpperCase();

    // Limitar la cadena a un máximo de 50 caracteres
    if (dynamicValue.length > 50) {
        dynamicValue = dynamicValue.slice(0, 50);
    }

    //Actualizar valor de elemento
    inputElement.value = dynamicValue;
}
function validateAlpha(inputElement, goodIcon, badIcon = document.createElement("i")) {
    let dynamicValue = inputElement.value;

    if (dynamicValue.length >= 2) {
        goodIcon.classList.replace("checkIconHidden", "checkIcon");
        badIcon.classList.replace("badIcon", "badIconHidden");
    }
    else {
        goodIcon.classList.replace("checkIcon", "checkIconHidden");
        badIcon.classList.replace("badIconHidden", "badIcon");
    }
}



//GESTIÓN CORREO
//Formato correo
function formatEmail(inputElement) {
    let dynamicValue = inputElement.value;
    dynamicValue = dynamicValue.toLowerCase();

    //Actualizar valor de elemento
    inputElement.value = dynamicValue;
}
//VALIDACION CORREO ELECTRÓNICO
function validateEmail(inputElement, goodIcon, badIcon = document.createElement("i")) {
    let dynamicValue = inputElement.value;
    let emailFormat = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;

    if(emailFormat.test(dynamicValue)) {
        goodIcon.classList.replace("checkIconHidden", "checkIcon");
        badIcon.classList.replace("badIcon", "badIconHidden");
    }
    else {
        goodIcon.classList.replace("checkIcon", "checkIconHidden");
        badIcon.classList.replace("badIconHidden", "badIcon");
    }
}



//GESTION DE CONTRASEÑA
//Validar contraseña
function validatePassword(inputElement, goodIcon, badIcon = document.createElement("i")) {
    let dynamicValue = inputElement.value;

    //Mínimo 8 caracteres
    let lengthValue = dynamicValue.length >= 12 ? true : false;
    // Debe contener al menos una letra, al menos un número, al menos un caracter especial y al menos una letra mayúscula
    let letterValue = /[a-zA-Z]/.test(dynamicValue);
    let numberValue = /[0-9]/.test(dynamicValue);
    let specialCharValue = /[!@#$%^&*(),.?":{}|<>]/.test(dynamicValue);
    let uppercaseValue = /[A-Z]/.test(dynamicValue);

    if(lengthValue && letterValue && numberValue && specialCharValue && uppercaseValue) {
        goodIcon.classList.replace("checkIconHidden", "checkIcon");
        badIcon.classList.replace("badIcon", "badIconHidden");
    }
    else {
        goodIcon.classList.replace("checkIcon", "checkIconHidden");
        badIcon.classList.replace("badIconHidden", "badIcon");
    }
}
//Función para ocultar / mostrar contraseña dinámicamente
function showHide(inputElement, eyeicon) {
    if(inputElement.type == "password") {
        inputElement.type = "text";
        eyeicon.classList.replace("fa-eye-slash","fa-eye");
        eyeicon.setAttribute("style", "color:#0080ff");
    }
    else {
        inputElement.type = "password";
        eyeicon.classList.replace("fa-eye","fa-eye-slash");
        eyeicon.removeAttribute("style");
    }
}



//GESTION CONFIRMAR CONTRASEÑA
//Validación de coincidencia
function validateConfirmPassword(password1, password2, goodIcon, badIcon = document.createElement("i")) {
    let password = password1;
    let confirm_password = password2.value;

    if(password == confirm_password) {
        goodIcon.classList.replace("checkIconHidden", "checkIcon");
        badIcon.classList.replace("badIcon", "badIconHidden");
    }
    else {
        goodIcon.classList.replace("checkIcon", "checkIconHidden");
        badIcon.classList.replace("badIconHidden", "badIcon");
    }
}



//GESTION TELEFONO
//Formato número telefónico - Sólo dígitos (8)
function formatNumber(inputElement) {
    let dynamicValue = inputElement.value;

    //Eliminar caracteres no numéricos 
    dynamicValue = dynamicValue.replace(/[^0-9]/g, '');

    // Limitarun máximo de 8 caracteres
    if (dynamicValue.length > 8) {
        dynamicValue = dynamicValue.slice(0, 8);
    }

    //Actualizar valor de elemento
    inputElement.value = dynamicValue;
}
//Validación número telefónico
function validateNumber(inputElement, goodIcon, badIcon = document.createElement("i")) {
    let dynamicValue = inputElement.value;

    if (dynamicValue.length >= 8 && /^[0-9]+$/.test(dynamicValue)) {
        goodIcon.classList.replace("checkIconHidden", "checkIcon");
        badIcon.classList.replace("badIcon", "badIconHidden");
    }
    else if (dynamicValue.length !== 0 && dynamicValue.length < 8) {
        goodIcon.classList.replace("checkIcon", "checkIconHidden");
        badIcon.classList.replace("badIconHidden", "badIcon");

    }
    if (dynamicValue.length === 0) {
        goodIcon.classList.replace("checkIcon", "checkIconHidden");
        badIcon.classList.replace("badIcon", "badIconHidden");
    }

}



//GESTION PATENTE DE VEHÍCULO CHILENO
//Formato - Sólo letras y números en mayúscula
function formatPlate(inputElement) {
    let dynamicValue = inputElement.value;

    //Eliminar caracteres especiales y convertir a mayúsculas
    dynamicValue = dynamicValue.replace(/[^a-zA-Z0-9]/g, '').toUpperCase();

    // Limitar la cadena a un máximo de 6
    if (dynamicValue.length > 6) {
        dynamicValue = dynamicValue.slice(0, 6);
    }

    //Actualizar valor de elemento
    inputElement.value = dynamicValue;
}



//GESTIÓN AÑO
//Formato
function formatYear(inputElement) {
    let dynamicValue = inputElement.value;

    // Eliminar caracteres que no son números
    dynamicValue = dynamicValue.replace(/\D/g, '');

    // Limitar la cadena a un máximo de 4
    if (dynamicValue.length > 4) {
        dynamicValue = dynamicValue.slice(0, 4);
    }

    //Actualizar valor de elemento
    inputElement.value = dynamicValue;
}



//GESTION NOMBRE, MODELO DE INSUMOS Y VEHICULOS, ETC. (FORMATO MAYUSCULAS SIMPLE)
//Formato
function formatUpper(inputElement) {
    let dynamicValue = inputElement.value;
    
    dynamicValue = dynamicValue.toUpperCase();
    
    //Actualizar valor de elemento
    inputElement.value = dynamicValue;
}



//GESTION SKU
//Formato - máximo 13 dígitos (EAN-13)
function formatEan13(inputElement) {
    let dynamicValue = inputElement.value;

    // Eliminar caracteres que no son números
    dynamicValue = dynamicValue.replace(/\D/g, '');

    // Limitar la cadena a un máximo de 13
    if (dynamicValue.length > 13) {
        dynamicValue = dynamicValue.slice(0, 13);
    }


    //Actualizar valor de elemento
    inputElement.value = dynamicValue;

}



//GESTION CHECKBOX PARA INSUMOS
//Mostrar y ocultar campos
function displayElement(element) {
    element.removeAttribute("hidden");
}
function hideElement(element) {
    element.setAttribute("hidden", true);
}



//Evento load cuando se cargue el DOM para los checks de validaciones
window.addEventListener("load", async () => {
    if(checkRut) {
        validateRut(inputRut, checkRut);
        document.getElementById("digitoVerificador").value = "";
    }
    if(checkName) {
        validateAlpha(inputName, checkName);
    }
    if(checkLastName) {
        validateAlpha(inputLastName, checkLastName);
    }
    if(checkEmail) {
        validateEmail(inputEmail, checkEmail);
    }
    if(checkPassword) {
        validatePassword(inputPassword, checkPassword);
    }
    if(checkNumber) {
        validateNumber(inputNumber, checkNumber);
    }
});



//------------------------------------------------------------------
//------------------------------------------------------------------
//------------------------------------------------------------------


/*SELECCION DE ELEMENTO Y APLICACIÓN DE EVENTOS*/
//RUT
const inputRut = document.getElementById("input-rut");
const inputRutLogin = document.getElementById("input-rut-login");
const checkRut = document.getElementById("check-rut");
const xmarkRut = document.getElementById("xmark-rut");
//const inputDigitRut = document.getElementById("digito-verificador");
if(inputRut) {
    //Evento formato
    inputRut.addEventListener('input', ()=> {
        formatRut(inputRut, "signup");
    });
}
if(inputRutLogin) {
    //Evento formato
    inputRutLogin.addEventListener('input', ()=> {
        formatRut(inputRutLogin, "login");
    });
}
if(checkRut) {
    //Evento validación
    inputRut.addEventListener('blur', ()=> {
        validateRut(inputRut, checkRut, xmarkRut);
        //calculateValidateRut(inputRut, inputDigitRut);
    });
}



//NOMBRE
const inputName = document.getElementById("input-name");
const checkName = document.getElementById("check-name");
const xmarkName = document.getElementById("xmark-name");
if(inputName) {
    //Evento formato
    inputName.addEventListener('input', ()=> {
        formatAlpha(inputName);
    });
    //Evento validación
    inputName.addEventListener('blur', ()=> {
        validateAlpha(inputName, checkName, xmarkName);
    });
}



//APELLIDO
const inputLastName = document.getElementById("input-lastname");
const checkLastName = document.getElementById("check-lastname");
const xmarkLastName = document.getElementById("xmark-lastname");
if(inputLastName) {
    //Evento formato
    inputLastName.addEventListener('input', ()=> {
        formatAlpha(inputLastName);
    });
    //Evento validación
    inputLastName.addEventListener('blur', ()=> {
        validateAlpha(inputLastName, checkLastName, xmarkLastName);
    });
}



//CORREO ELECTRONICO
const inputEmail = document.getElementById("input-email");
const checkEmail = document.getElementById("check-email");
const xmarkEmail = document.getElementById("xmark-email");
if(inputEmail) {
    //Evento formato
    inputEmail.addEventListener('input', ()=> {
        formatEmail(inputEmail);
    });
    //Evento validación
    inputEmail.addEventListener('blur', ()=> {
        validateEmail(inputEmail, checkEmail, xmarkEmail);
    });
}



//CONTRASEÑA
const inputPassword = document.getElementById("input-password");
const eyeicon = document.getElementById("eye-slash-icon");
const checkPassword = document.getElementById("check-password");
const xmarkPassword = document.getElementById("xmark-password");
if(inputPassword) {
    //Evento validación
    inputPassword.addEventListener('blur', ()=> {
        validatePassword(inputPassword, checkPassword, xmarkPassword);
    });
    //Mostrar y/o ocultar contraseña
    eyeicon.addEventListener("click", ()=>{
        showHide(inputPassword, eyeicon);
    });
}



//CONFIRMAR CONTRASEÑA
const inputConfirmPassword = document.getElementById("input-confirm_password")
const checkConfirmPassword = document.getElementById("check-confirm_password");
const xmarkConfirmPassword = document.getElementById("xmark-confirm_password");
if(inputConfirmPassword) {
    //Evento validación
    inputConfirmPassword.addEventListener('blur', ()=> {
        validateConfirmPassword(inputPassword.value, inputConfirmPassword, checkConfirmPassword, xmarkConfirmPassword);
    });
}



//TELEFONO
const inputNumber = document.getElementById("input-number");
const checkNumber = document.getElementById("check-number");
const xmarkNumber = document.getElementById("xmark-number");
if(inputNumber) {
    //Evento formato
    inputNumber.addEventListener('input', ()=> {
        formatNumber(inputNumber);
    });
    //Evento validación
    inputNumber.addEventListener('blur', ()=> {
        validateNumber(inputNumber, checkNumber, xmarkNumber);
    });
}



//AÑO
const inputYear = document.getElementById("inputYear");
if(inputYear) {
    //Evento formato
    inputYear.addEventListener('input', ()=> {
        formatYear(inputYear);
    });
}



//PATENTE DE VEHICULO CHILENO
const inputPlate = document.getElementById("fireTruckPlate");
if(inputPlate) {
    //Evento formato
    inputPlate.addEventListener('input', () => {
        formatPlate(inputPlate);
    });
}



//NUMERO DE CHASIS
const inputVin = document.getElementById("fireTruckVin");
if(inputVin) {
    //Evento formato
    inputVin.addEventListener('input', () => {
        formatUpper(inputVin);
    });
}



//NOMBRE DE VEHICULO E INSUMO
const inputTitle = document.getElementById("inputTitle");
if(inputTitle) {
    //Evento formato
    inputTitle.addEventListener('input', () => {
        formatUpper(inputTitle);
    })
}



//MODELO DE VEHICULO E INSUMO
const inputModel = document.getElementById("inputModel");
if(inputModel) {
    //Evento formato
    inputModel.addEventListener('input', () => {
        formatUpper(inputModel);
    })
}



//MARCA
const inputBrand = document.getElementById("inputBrand");
if(inputBrand) {
    //Evento formato
    inputBrand.addEventListener('input', () => {
        formatUpper(inputBrand);
    })
}


//CODIGO DE BARRAS
const inputSku = document.getElementById("inputSku");
if (inputSku) {
    //Evento formato
    inputSku.addEventListener("input", () => {
        formatEan13(inputSku);
    })
}



//MANTENCIÓN
const checkboxMaintenance1 = document.getElementById("checkboxMaintenance1");
console.log("check de mantención programada identificado")
const selectMaintenancePrograms = document.getElementById("selectMaintenancePrograms");

const checkboxMaintenance2 = document.getElementById("checkboxMaintenance2");
const inputMaintenanceHour = document.getElementById("inputMaintenanceHour");
const labelMaintenanceHour = document.getElementById("labelMaintenanceHour");

checkboxMaintenance1.addEventListener("change", (event) => {
    console.log("cambio detectado en el check de mantencion programada")
    if (event.target.checked) {
        checkboxMaintenance2.checked = false;
        displayElement(selectMaintenancePrograms);
        inputMaintenanceHour.value = "";

        hideElement(inputMaintenanceHour);
        hideElement(labelMaintenanceHour);

    }
    else {
        hideElement(selectMaintenancePrograms);
        selectMaintenancePrograms.value = 0;
    }
})
checkboxMaintenance2.addEventListener("change", (event) => {
    if (event.target.checked) {
        checkboxMaintenance1.checked = false;
        selectMaintenancePrograms.value = 0;
        hideElement(selectMaintenancePrograms);

        displayElement(inputMaintenanceHour);
        displayElement(labelMaintenanceHour);
    }
    else {
        hideElement(inputMaintenanceHour);
        hideElement(labelMaintenanceHour);
        inputMaintenanceHour.value = "";
    }
})



//EXPIRACIÓN
const checkboxExpiration = document.getElementById("checkboxExpiration");
const labelExpireDate = document.getElementById("labelExpireDate");
const inputExpireDate = document.getElementById("inputExpireDate");
const labelExpireNotification = document.getElementById("labelExpireNotification");
const inputExpireNotification = document.getElementById("inputExpireNotification");
const indicatorExpireNotification = document.getElementById("indicatorExpireNotification");

checkboxExpiration.addEventListener("change", (event) => {
    if (event.target.checked) {
        displayElement(inputExpireDate);
        displayElement(labelExpireDate);
        displayElement(inputExpireNotification);
        displayElement(labelExpireNotification);
        displayElement(indicatorExpireNotification);
        inputExpireNotification.value = 7;
        indicatorExpireNotification.innerHTML= `${inputExpireNotification.value} días`;
    }
    else {
        hideElement(inputExpireDate);
        hideElement(labelExpireDate);
        hideElement(inputExpireNotification);
        hideElement(labelExpireNotification);
        hideElement(indicatorExpireNotification);
        inputExpireDate.value = "";
        inputExpireNotification.value = "";
    }
})

inputExpireNotification.addEventListener("input", () => {
    const value = inputExpireNotification.value;
            let labelText = value + ' día'; // Por defecto, asumimos un solo día
            if (value > 1) {
            labelText += 's'; // Plural para "días" si es más de uno
            }

            //Convertir a meses si es mayor a 30
            if (value >= 30) {
                const months = Math.floor(value / 30);
                labelText = months + ' mes';
                if (months > 1) {
                    labelText += 'es';
                }

                if (value % 30 !== 0) {
                    labelText += ` ${value % 30} día`;
                    if (value % 30 > 1) {
                      labelText += 's';
                    }
                }
            }
            
            indicatorExpireNotification.textContent = labelText;
})

