// Loads the medium editor editable field
// var editor = new MediumEditor('.editable', {
//         buttonLabels: 'fontawesome'
// });



$(document).ready(function () {
   
   grabTextFile()
   grabHTMLplaces()
   grabHTMLorgs()
   grabHTMLpeople()
   grabHTMLother()


});



// grabs a file and displays it on the main div.  IT WORKS!

function grabTextFile() {

	$("#text1").load(path_to_show, highlightText);

}

// by clicking a tab I should load a different html file on the div. THIS KINDA WORKS


function grabHTMLplaces() {

$.ajax({
  type: "POST",
  url: "/get_places",
  data: { ent : "places" },
})
  .done(function( html ) {
    $( "#container_places" ).html( html );
  });

}


function grabHTMLorgs() {

$.ajax({
  type: "POST",
  url: "/get_places",
  data: { ent : "organizations" },
})
  .done(function( html ) {
    $( "#container_orgs" ).html( html );
  });

}

function grabHTMLpeople() {

$.ajax({
  type: "POST",
  url: "/get_places",
  data: { ent : "people" },
})
  .done(function( html ) {
    $( "#container_people" ).html( html );
  });

}

function grabHTMLother() {

$.ajax({
  type: "POST",
  url: "/get_places",
  data: { ent : "nouns" },
})
  .done(function( html ) {
    $( "#container_general" ).html( html );
  });

}

// highlight a list of terms on the main text. THIS WORKS

function highlightText() {

	$("#text1").highlight("the", true);
}

function removehighlightText() {

	$("#text1").removeHighlight();

}



// autosubmit the language selector form. THIS DOESNT WORK YET




