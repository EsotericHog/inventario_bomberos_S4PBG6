//Switch para activar modo claro y oscuro
const switchTheme = document.getElementById("switch-theme");
const bodyHtml = document.body;
const inputBoxes = document.getElementsByClassName("input-box");

if(switchTheme) {
    switchTheme.addEventListener('click', () => {
        switchTheme.classList.toggle("active");
        bodyHtml.classList.toggle("darkmode");
        if(inputBoxes) {
            //inputBoxes.classList.toggle("darkmode");
        }

        //Guardar configuración en localstorage
        if (bodyHtml.classList.contains("darkmode")) {
            localStorage.setItem('dark-mode', 'true');
        }
        else {
            localStorage.setItem('dark-mode', 'false');
        }
    });
}

document.addEventListener('DOMContentLoaded', () => {
    //Consultar configuración en localstorage
        if (localStorage.getItem('dark-mode') === "true") {
            switchTheme.classList.add("active");
            bodyHtml.classList.add("darkmode");
            //inputBoxes.classList.add("darkmode");
        }
        else {
            switchTheme.classList.remove("active");
            bodyHtml.classList.remove("darkmode");
            //inputBoxes.classList.remove("darkmode");
        }
    })