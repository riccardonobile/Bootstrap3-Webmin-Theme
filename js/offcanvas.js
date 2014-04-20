$(document).ready(function() {
	var hidden = 0;
	function hide_show (status) {
		if (status == 'open') {
			$('#sidebar .open-hidden').hide();
			$('#sidebar').animate({width: "240px"}, 200, function() {		//funzione all'interno dell'altra per fare in modo che venga eseguita quando la prima ha finito
				$('#sidebar a span').toggle();							//quando apro faccio apparire dopo gli elementi
				$('#sidebar ul.navigation:not(:first-child)').css({'margin-top': '0'});
			});
			$('#sidebar form').css({"margin": "10px"});
			$('#sidebar input[name="search"]').toggle();
			$('#wrapper .menu').animate({marginLeft: "240px"}, 200);
		} else if (status == 'close') {
			$('#sidebar .sub').hide();									//chiudo le tab eventualmente aperte
			width = '40px';
			$('#sidebar a span').toggle();								//quando chiudo faccio sparire prima gli elementi
			$('#sidebar .open-hidden').show();
			$('#sidebar input[name="search"]').toggle();
			$('#sidebar form').css({'margin': '0'});
			$('#sidebar ul.navigation:not(:first-child)').css({'margin-top': '-1px'});
			$('#sidebar').animate({width: "40px"}, 200);
			$('#wrapper .menu').animate({marginLeft: "40px"}, 200);
		}
		hidden = !hidden;
	}
	$( ".navigation > li" ).click(function() {
		var sub = $('a', this).attr('href');
		if (sub == '#hide'){
			if (hidden == 0) {
				hide_show ('close');
			} else {
				hide_show ('open');
			}
		} else {
			if (hidden == 1) {
				hide_show ('open');
			}
			$(sub).slideToggle();
			if (sub == '#search') {
				$('#sidebar input[name="search"]').focus();
			}
		}
		return false;
	});
});