$(function(){
	function loading() {
		/*$('iframe[name="page"]').css('display', 'none');*/
		$('.loader-container').css('display', 'block');
	};
	loading();
	$('a[target="page"]').click(function(){loading()});
	$('iframe[name="page"]').load(function () {
		$('.loader-container').css('display', 'none');
		/*$('iframe[name="page"]').css('display', 'block');*/
		$('iframe[name="page"]').contents().find('a').not('[href~="#"], [onclick]').click(function(){loading()});
		$('iframe[name="page"]').contents().find('button').click(function(){loading()});
	});
});