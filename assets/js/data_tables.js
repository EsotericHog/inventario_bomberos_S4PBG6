//$(document).ready( function () {
//    $('#itemsTable').DataTable( {
//        "tabIndex": 1,
//        "ordering": true
//    });
//} );

let table = new DataTable('#itemsTable', {
    order: [[0, 'desc']]
});
let table2 = new DataTable('#itemsManyTable');
let table3 = new DataTable('#compartmentsTable');
let table4 = new DataTable('#fireTrucksTable');
let table5 = new DataTable('#usersTable');