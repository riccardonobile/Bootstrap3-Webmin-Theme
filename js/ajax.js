var page = "dashboard.cgi";
var where = "#dashboard";
var time = 60000;
$(function(){
	var loop = function(){
		$.ajax({
			type: "GET",
			url: page,
			success: function(data) {
				$(where).html(data);
			}
		});
		setTimeout(function () {loop()}, time);
	}
	loop ();
});