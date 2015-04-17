$(function() {
	var menu = {};
	var time;
	$('[data-open="hideMenu"]').click(function() {
		$('[data-open]').parent().removeClass('active');
		$('.aside-arrow > i').removeClass('rotated');
		if (menu.isClose)
			time = 400;
		else
			time = 0;
		var i=0
		var len = $('.submenu').length;
		$('.submenu').slideUp(function() {
			if(i==len-1) {
				$('.webmin-sidebar').toggleClass('aside-close');
				$('.iframe-container').toggleClass('iframe-close');
				setTimeout(function() {
					$('.aside-text, .aside-arrow, .search-aside, .power-aside, .theme-update-aside').toggle();
				}, time);
			}
			i++;
		});
		menu.isClose = !menu.isClose;
		return false;
	});
	$('[data-open]').not("[data-open='hideMenu']").click(function() {
		menu.sub = $(this).attr('data-open');
		$(this).parent().toggleClass('active');
		if(menu.isClose) {
			$('.webmin-sidebar').removeClass('aside-close');
			$('.iframe-container').removeClass('iframe-close');
			setTimeout(function() {
				$('.aside-text, .aside-arrow, .search-aside, .power-aside, .theme-update-aside').toggle();
				$('.aside-arrow > i', this).toggleClass('rotated');
				$(menu.sub).slideToggle();
			}, 400);
			menu.isClose = !menu.isClose;
		} else {
			$(menu.sub).slideToggle();
		}
		$('.aside-arrow > i', this).toggleClass('rotated');
		return false;
	});
	var userAgent = navigator.userAgent.toLowerCase();
	if (userAgent.match(/(iphone|ipod|ipad)/)) {
		$('.iframe-container').addClass('ios');
	};
	var menuElement = {};
	menuElement.removeClass = function(){return}													//create a virtual empty function to avoid issues on first call
	var iframe =  $("iframe[name=page-container]");													//get the iframe
	iframe.load(function(){																			//when the iframe loads
		var iframePath = iframe.contents().get(0).location.pathname;								//get the iframe location path
		if (iframePath.substring(0, 1) == '/') { 													//if the first charter is "/"
		  iframePath = iframePath.substring(1);														//remove it
		}
		menuElement.removeClass("selected");															//remove active class from previous <li>
		menuElement = $("a[href='"+iframePath+"']").parent();												//get new <li>
		menuElement.addClass("selected");																//add active class to new <li>
	});
});
