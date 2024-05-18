/* Botón para volver a la página anterior */
function previousPage() {
    window.history.back();
}

const backButton = document.getElementById('back_btn');
if(backButton) {
    backButton.addEventListener("click", previousPage);
}



///* Función para verificar que se envió una imagen por formulario */
//function upload_image(formElement) {
//    let form = formElement;
//    if(form.file.value==0 || form.file.value=='') {
//        form.picture.value='empty';
//    }
//    form.submit();
//}
//
///*Seleccionar formulario para agregar vehículos*/
//const addVehicleForm = document.getElementById("addVehicleForm");
//if(addVehicleForm) {
//    addVehicleForm.addEventListener('submit', () => {
//        upload_image(addVehicleForm);
//    })
//}