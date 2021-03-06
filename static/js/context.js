


$(document).ready(function () {
   
   grabTextFile()
   grabHTMLplaces()
   grabHTMLpeople()
   grabHTMLorgs()
   grabHTMLother()


});


// grabs a file and displays it on the main div.

function grabTextFile() {

  $.getJSON( "/text", function(textdata) {
    console.log( "success loading text data" );
    $("#text1").html(textdata);
  });


}

// by clicking a tab I should load a different html file on the div. 


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

// highlight a list of terms on the main text. 
// http://bartaz.github.io/sandbox.js/jquery.highlight.html

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


// Image Gallery (Magnific Popup) http://dimsemenov.com/plugins/magnific-popup/

function magnificPopup() {

  $('.popup-gallery').magnificPopup({
    delegate: 'a',
    type: 'image',
    tLoading: 'Loading image #%curr%...',
    mainClass: 'mfp-img-mobile',
    gallery: {
      enabled: true,
      navigateByImgClick: true,
      preload: [0,1] // Will preload 0 - before current, and 1 after the current image
    },
    image: {
      tError: '<a href="%url%">The image #%curr%</a> could not be loaded.',
      titleSrc: function(item) {
        return item.el.attr('title') + '<small>on Wikipedia</small>';
      }
    }
  });

};





