// Loads the medium editor editable field
// var editor = new MediumEditor('.editable', {
//         buttonLabels: 'fontawesome'
// });



$(document).ready(function () {
    
   grabTextFile()

});


function grabTextFile() {

	$("#text1").load(path_to_show);

}

function highlightText() {

	$("#text1").highlight("the", true);
}

function highlightText() {

	$("#text1").removeHighlight();

}

$("#profile").click(function() {

	$('#profile a[href="#profile"]').tab('show')

});


function load_home(){

document.getElementById("#general").innerHTML='<object type="text/html" data="general.html" ></object>';

}