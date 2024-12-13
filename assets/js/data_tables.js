function initializeTable(selector) {
    return new DataTable(selector, {
        language: {
            processing: "Procesando...",
            search: "Buscar:",
            lengthMenu: "Mostrar _MENU_ registros",
            info: "Mostrando registros del _START_ al _END_ de un total de _TOTAL_ registros",
            infoEmpty: "Mostrando registros del 0 al 0 de un total de 0 registros",
            infoFiltered: "(filtrado de un total de _MAX_ registros)",
            infoPostFix: "",
            loadingRecords: "Cargando...",
            zeroRecords: "No se encontraron resultados",
            emptyTable: "Ningún dato disponible en esta tabla",
            paginate: {
                first: "Primero",
                previous: "Anterior",
                next: "Siguiente",
                last: "Último"
            },
            aria: {
                sortAscending: ": Activar para ordenar la columna de manera ascendente",
                sortDescending: ": Activar para ordenar la columna de manera descendente"
            }
        }
    });
}



//let table = new DataTable('#itemsTable', {
//    order: [[0, 'desc']],
//    language: {
//        search: "Buscar:"
//    }
//});
let table = initializeTable('#itemsTable');
let table2 = initializeTable('#itemsManyTable');
let table3 = initializeTable('#compartmentsTable');
let table4 = initializeTable('#fireTrucksTable');
let table5 = initializeTable('#usersTable');

// let table2 = new DataTable('#itemsManyTable');
// let table3 = new DataTable('#compartmentsTable');
// let table4 = new DataTable('#fireTrucksTable');
// let table5 = new DataTable('#usersTable');