// Make .full full width using padding and negative margins
function makeFull() {
    var fullWidth = $( window ).width(),
        fullHeight = $( window ).height();

    $( "#content" ).width( fullWidth ).height( fullHeight );

}
makeFull();
$( window ).bind( "resize", function() { makeFull(); } );

