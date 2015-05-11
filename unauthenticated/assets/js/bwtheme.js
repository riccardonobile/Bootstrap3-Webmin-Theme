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
	menuElement.removeClass = function(){return};													//create a virtual empty function to avoid issues on first call
	var menuParent = menuElement;
	var iframe =  $("iframe[name=page-container]");													//get the iframe
	iframe.load(function(){																			//when the iframe loads
		var iframePath = iframe.contents().get(0).location.pathname;								//get the iframe location pathì

		menuElement.removeClass("selected");														//remove active class from previous <li>
		menuParent.removeClass("selected");															//remove active class from previous parent <li>

		var regex = /([A-z-])+\//;																	//take the first string containg "A-z" + "+" before "/"
		iframePath = regex.exec(iframePath);

		if(iframePath === null) {																	//if string was not found
			return;																					//return
		}

		iframePath = iframePath[0];

		menuElement = $("a[href='"+iframePath+"']").parent();										//get new <li>
		menuParent = menuElement.parent().parent().prev();											//get new parent <li>, two times because is the 2nd parent.

		menuElement.addClass("selected");															//add active class to new <li>
		menuParent.addClass("selected");															//add active class to new parent <li>
	});
});
