$(document).ready(function() {
	$( ".navigation > li" ).click(function() {
		var sub = $('a', this).attr('href');
		$(sub).slideToggle();
	});
});