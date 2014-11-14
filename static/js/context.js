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

	$("#text1").load(path_to_show);

}

// by clicking a tab I should load a different html file on the div. THIS  WORKS


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

// highlight a list of terms on the main text. THIS  WORKS

var hiData = $.getJSON( "/named_entities", function() {
  console.log( "success loading highlight json" );
});
 

function highlight() {
    $("#text1").highlight(hiData.responseJSON);
    $("#highlight").one("click", unhighlight);
}
function unhighlight() {
    $("#text1").unhighlight();
    $("#highlight").one("click", highlight);
}
$("#highlight").one("click", highlight);


// getting Geocodes from JSON file.  Returns an object {"New_York": {"lat": 40.7305991, "lon": -73.9865812, "name": "New York"}....}

// var mapData = $.getJSON( "/geocodes", function() {
//   console.log( "success loading geocodes json" );
// });





// // saving the content

// $('.editable').on('input', function() {
//         $('#page_content').val(editor.serialize().page_content_editor.value);
//     });
//     $('#page_content_editor').html($('#page_content').val()); // Put editor content into hidden field

