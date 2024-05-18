//Obtener categorías de insumos
const listMaintenancePrograms = async () => {
    const selectMaintenancePrograms = document.getElementById('selectMaintenancePrograms');
    if(!selectMaintenancePrograms) {
        return;
    }

    let selectOption = selectMaintenancePrograms.options[selectMaintenancePrograms.selectedIndex];

    var optionValue = selectOption ? selectOption.value : null;
    var optionText = selectOption ? selectOption.text : null;

    try {
        const response = await fetch(`${window.location.origin}/maintenance_programs/`);
        const data = await response.json();
        
        if(data.message == "Success") {
            let options = ``;
            if(optionValue && optionText) {
                options += `<option value='0'>Seleccionar Programa de mantención</option>`;
                options += `<option selected value='${optionValue}'>${optionText}</option>`;
            }
            else {
                options += `<option value='0'>Seleccionar Programa de mantención</option>`;
            }
            data.programs.forEach((program)=>{
                if (program.frequency >= 364) {
                    var frequency = program.frequency / 364;
                    var string = "años";
                }
                else if (program.frequency >= 30) {
                    var frequency = program.frequency / 30;
                    var string = "meses";
                }
                else if (program.frequency >= 7) {
                    var frequency = program.frequency / 7;
                    var string = "semanas";
                }
                else {
                    var frequency = program.frequency;
                    var string = "días";
                }
                options += optionValue != program.id ? `<option value='${program.id}'>${program.name} - El día ${program.day} / cada ${frequency} ${string} / notificación ${program.notification} días antes </option>` : null;
            })
            selectMaintenancePrograms.innerHTML=options;
        }
        else {
            selectMaintenancePrograms.innerHTML=`<option value='0'>Seleccionar programa de mantención</option>`;
        }
    }
    catch(error) {
        console.log(error);
    }
}



//Obtener categorías de insumos
const listCategories = async () => {
    const selectCategory = document.getElementById('selectCategory');
    if(!selectCategory) {
        return;
    }
    let selectOption = selectCategory.options[selectCategory.selectedIndex];

    var optionValue = selectOption ? selectOption.value : null;
    var optionText = selectOption ? selectOption.text : null;

    try {
        const response = await fetch(`${window.location.origin}/categories/`);
        const data = await response.json();
        
        if(data.message == "Success") {
                let options = ``;
                if(optionValue && optionText) {
                    options += `<option value='0'>Seleccionar categoría</option>`;
                    options += `<option selected value='${optionValue}'>${optionText}</option>`;
                }
                else {
                    options += `<option value='0'>Seleccionar categoría</option>`;
                }
            data.categories.forEach((category)=>{
                options += optionValue != category.id ? `<option title='${category.description}' value='${category.id}'>${category.name}</option>` : null;
            })
            selectCategory.innerHTML=options;
        }
        else {
            selectCategory.innerHTML=``;
        }
    }
    catch(error) {
        console.log(error);
    }
}



//Obtener gavetas
const listCompartments = async (id, update = false) => {
    const selectCompartment = document.getElementById('selectCompartment');
    if(!selectCompartment) {
        return;
    }
    let selectOption = selectCompartment.options[selectCompartment.selectedIndex];

    var optionValue = selectOption ? selectOption.value : null;
    var optionText = selectOption ? selectOption.text : null;
    var update = update;

    try {
        const response = await fetch(`${window.location.origin}/compartments/${id}`);
        const data = await response.json();
        
        if(data.message == "Success") {
            let options = ``;
            if((optionValue) && (optionText) && (update)) {
                options += `<option value='0'>Seleccionar gaveta</option>`;
                options += `<option selected value='${optionValue}'>${optionText}</option>`;
            }
            else {
                options += `<option value='0'>Seleccionar gaveta</option>`;
            }

            data.compartments.forEach((compartment)=>{
                options += optionValue != compartment.id ? `<option title='${compartment.description ? compartment.description : ""}' value='${compartment.id}'>${compartment.name}</option>` : null;
            })
            selectCompartment.innerHTML=options;
            update = false;
        }
        else {
            selectCompartment.innerHTML=``;
        }
    }
    catch(error) {
        console.log(error);
    }
}



//Obtener unidades bomberiles
const listFireTrucks = async () => {
    const selectFireTruck = document.getElementById('selectFireTruck');
    if(!selectFireTruck) {
        return;
    }

    let selectOption = selectFireTruck.options[selectFireTruck.selectedIndex];

    var optionValue = selectOption ? selectOption.value : null;
    var optionText = selectOption ? selectOption.text : null;
    var update = true;

    try {
        const response = await fetch(`${window.location.origin}/firetrucks/`);
        const data = await response.json();
        
        if(data.message == "Success") {
            let options = ``;
            if(optionValue && optionText && (update)) {
                options += `<option value='0'>Seleccionar unidad</option>`;
                options += `<option selected value='${optionValue}'>${optionText}</option>`;
                listCompartments(optionValue, update);
            }
            else {
                options += `<option value='0'>Seleccionar unidad</option>`;
            }
            data.firetrucks.forEach((firetruck)=>{
                options += firetruck.id != optionValue ? `<option title='${firetruck.description}' value='${firetruck.id}'>${firetruck.name}</option>` : null;
            })
            selectFireTruck.innerHTML=options;
            update = false;
        }
        else {
            selectFireTruck.innerHTML=``;
        }
    }
    catch(error) {
        console.log(error);
    }

    selectFireTruck.addEventListener("change", (event) => {
        const value = event.target.value;
        selectContainer.value = 0;
        listCompartments(value, false);
    })
}



//Obtener categorías de insumos
const listContainers = async () => {
    const selectContainer = document.getElementById('selectContainer');
    if(!selectContainer) {
        return;
    }

    let selectOption = selectContainer.options[selectContainer.selectedIndex];

    var optionValue = selectOption ? selectOption.value : null;
    var optionText = selectOption ? selectOption.text : null;
    var update = true;

    try {
        const response = await fetch(`${window.location.origin}/containers/`);
        const data = await response.json();
        
        if(data.message == "Success") {
            let options = ``;
            if(optionValue && optionText && (update)) {
                options += `<option value='0'>Seleccionar contenedor</option>`;
                options += `<option selected value='${optionValue}'>${optionText}</option>`;
            }
            else {
                options += `<option value='0'>Seleccionar contenedor</option>`;
            }
            data.containers.forEach((container)=>{
                options += optionValue != container.inventory_id ? `<option title='${container.description}' value='${container.inventory_id}'>${container.name}</option>` : null;
            })
            selectContainer.innerHTML=options;
            update = false;
        }
        else {
            selectContainer.innerHTML=``;
        }
    }
    catch(error) {
        console.log(error);
    }

    selectContainer.addEventListener("change", (event) => {
        selectFireTruck.value = 0;
        listCompartments(0);
    })
}



//Obtener roles de usuario
const listProfiles = async () => {
    const selectProfile = document.getElementById('selectProfile');
    if(!selectProfile) {
        return;
    }

    try {
        const response = await fetch("../profiles/");
        const data = await response.json();
        
        if(data.message == "Success") {
            let options = ``;
                options += `<option value='0'>Rol de usuario</option>`;
            data.profiles.forEach((profile)=>{
                options += `<option value='${profile.id}'>${profile.name}</option>`;
            })
            selectProfile.innerHTML=options;
        }
        else {
            selectProfile.innerHTML=``;
        }
    }
    catch(error) {
        console.log(error);
    }

    selectProfile.addEventListener("change", (event) => {
        const value = event.target.value;
        if(value == 0) {
            checkSelectProfile.classList.replace("checkIcon", "checkIconHidden")
        }
        else {
            checkSelectProfile.classList.replace("checkIconHidden", "checkIcon")
        }
    })
}


//Obtener lista de ciudades
const listStations = async (id) => {
    if(id == 0) {
        selectStation.innerHTML=``;
    }
    else {
        try {
            const response = await fetch(`../stations/${id}`);
            const data = await response.json();
            
            if(data.message == "Success") {
                let options = ``;
                    options += `<option value=0>Seleccionar estación</option>`;
                data.stations.forEach((station)=>{
                    options += `<option value=${station.id}>${station.name}</option>`;
                })
                selectStation.innerHTML=options;
            }
            else {
                selectStation.innerHTML=``;
            }
        }
        catch(error) {
            console.log(error);
        }
    }

    selectStation.addEventListener("change", (event) => {
        const value = event.target.value;
        if(value == 0) {
            checkSelectStation.classList.replace("checkIcon", "checkIconHidden")
        }
        else {
            checkSelectStation.classList.replace("checkIconHidden", "checkIcon")
        }
    })
}

//Obtener lista de ciudades
const listComunes = async (id) => {
    if(id == 0) {
        selectComune.innerHTML=``;
    }
    else {
        try {
            const response = await fetch(`../comunes/${id}`);
            const data = await response.json();
            
            if(data.message == "Success") {
                let options = ``;
                    options += `<option value=0>Seleccionar comuna</option>`;
                data.comunes.forEach((comune)=>{
                    options += `<option value=${comune.id}>${comune.name}</option>`;
                })
                selectComune.innerHTML=options;
            }
            else {
                selectComune.innerHTML=``;
            }
        }
        catch(error) {
            console.log(error);
        }
    }

    selectComune.addEventListener("change", (event) => {
        const value = event.target.value;
        if(value == 0) {
            checkSelectComune.classList.replace("checkIcon", "checkIconHidden")
        }
        else {
            checkSelectComune.classList.replace("checkIconHidden", "checkIcon")
        }
        listStations(value);
    })
}

//Obtener lista de regiones
const listRegions = async() => {
    const selectRegion = document.getElementById('selectRegion');
    const checkSelectRegion = document.getElementById('checkSelectRegion');
    if(!selectRegion) {
        return;
    }
    else {
        selectRegion.addEventListener("change", (event) => {
            const value = event.target.value;
            if(value == 0) {
                checkSelectRegion.classList.replace("checkIcon", "checkIconHidden")
            }
            else {
                checkSelectRegion.classList.replace("checkIconHidden", "checkIcon")
            }
            listComunes(value);
        });
    }
    
    try {
        const response = await fetch("../regions/");
        const data = await response.json();
        
        if(data.message == "Success") {
            let options = ``;
                options += `<option value=0>Seleccionar región</option>`;
            data.regions.forEach((region)=>{
                options += `<option value="${region.id}">${region.name}</option>`;
            })
            selectRegion.innerHTML=options;
        }
        else {
            selectRegion.innerHTML=``;
        }
    }
    catch(error) {
        console.log(error);
    }
};


//Carga inicial - Sólo carga el listado de regiones
const startLoad = async () => {

    await listRegions();
    await listProfiles();
    await listContainers();
    await listCategories();
    await listFireTrucks();
    await listMaintenancePrograms();

};

//Evento load cuando se cargue el DOM
window.addEventListener("load", async () => {
    await startLoad();
});