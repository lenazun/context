// Loads the medium editor editable field
// var editor = new MediumEditor('.editable', {
//         buttonLabels: 'fontawesome'
// });



$(document).ready(function () {
   
   grabTextFile()
   grabHTMLfile()


});



// grabs a file and displays it on the main div.  IT WORKS!

function grabTextFile() {

	$("#text1").load(path_to_show, highlightText);

}

// by clicking a tab I should load a different html file on the div. THIS KINDA WORKS


function grabHTMLfile() {

$.ajax({
  type: "POST",
  url: "/get_places",
})
  .done(function( html ) {
    $( "#container_places" ).html( html );
  });



// $.ajax({
//   url: "../templates/places.html",
//   cache: false
// })
//   .done(function( html ) {
//     $( "#container_places" ).html( html );
//   });

}



// highlight a list of terms on the main text. THIS WORKS

function highlightText() {

	$("#text1").highlight("the", true);
}

function removehighlightText() {

	$("#text1").removeHighlight();

}



// autosubmit the language selector form. THIS DOESNT WORK YET



