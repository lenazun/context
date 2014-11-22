


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



// saving the content
// From http://stackoverflow.com/questions/22084698/how-to-export-source-content-within-div-to-text-html-file


function downloadInnerHtml(filename, elId, mimeType) {
    var elHtml = document.getElementById(elId).innerHTML;
    var link = document.createElement('a');
    mimeType = mimeType || 'text/html';

    link.setAttribute('download', filename);
    link.setAttribute('href', 'data:' + mimeType  +  ';charset=utf-8,' + encodeURIComponent(elHtml));
    link.click(); 
}

var fileName =  'exported.html';


$('#download').click(function(){
    downloadInnerHtml(fileName, 'text1','text/html');
});

