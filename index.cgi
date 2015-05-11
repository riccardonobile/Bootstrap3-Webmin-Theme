#############################################################################################################################
# BWTheme 0.9.0 (https://github.com/winfuture/Bootstrap3-Webmin-Theme) - (http://theme.winfuture.it)						#
# Copyright (c) 2015 Riccardo Nobile <riccardo.nobile@winfuture.it> and Simone Cragnolini <simone.cragnolini@winfuture.it>	#
# Licensed under GPLv3 License (https://github.com/winfuture/Bootstrap3-Webmin-Theme/blob/testing/LICENSE)					#
#############################################################################################################################

BEGIN {push(@INC, "..");};
use WebminCore;
&ReadParse();
&init_config();

if ($in{'mod'}) {
	$minfo = { &get_module_info($in{'mod'}) };
}
else {
	$minfo = &get_goto_module();
}
$goto = $minfo ? "$minfo->{'dir'}/" :
$in{'page-container'} ? "" : "sysinfo.cgi";

if ($minfo) {
	$cat = "?$minfo->{'category'}=1";
}
if ($in{'page-container'}) {
	$goto .= "/".$in{'page-container'};
}

%text = &load_language($current_theme);
%gaccess = &get_module_acl( undef, "" );
$title = &get_html_framed_title();

do "bootstrap/bwtheme_lib.cgi";

&header($title);
print '<nav class="navbar navbar-default navbar-webmin navbar-fixed-top" role="navigation">' . "\n";
print '<div class="container-fluid">' . "\n";
print '<div class="navbar-header">' . "\n";
print '<button type="button" class="navbar-toggle navbar-toggle-webmin" data-toggle="collapse" data-target="#navbar-collapse">' . "\n";
print '<span class="sr-only">Toggle navigation</span>' . "\n";
print '<span class="icon-bar"></span>' . "\n";
print '<span class="icon-bar"></span>' . "\n";
print '<span class="icon-bar"></span>' . "\n";
print '</button>' . "\n";
print '<a class="navbar-brand" href=""><i class="fa fa-cloud"></i> Webmin ' . &get_webmin_version() . ' <span>' . &get_display_hostname() . '</span></a>' . "\n";
print '</div>' . "\n";
print '<div class="collapse navbar-collapse" id="navbar-collapse">' . "\n";
print '<ul class="nav navbar-nav">' . "\n";
print '<li class="visible-xs"><a data-toggle="collapse" data-target="#navbar-collapse" target="page-container" href="'. $gconfig{'webprefix'} . '/mobile_menu.cgi"><i class="fa fa-tags"></i> Main Menu</a></li>' . "\n";
%gaccess = &get_module_acl(undef, "");
if ($gconfig{'log'} && &foreign_available("webminlog")) {
	print '<li><a data-toggle="collapse" data-target="#navbar-collapse" target="page-container" href="'. $gconfig{'webprefix'} . '/webminlog/"><i class="fa fa-file-text"></i> Logs</a></li>' . "\n";
}
if (&foreign_available("webmin")) {
	print '<li><a data-toggle="collapse" data-target="#navbar-collapse" target="page-container" href="'. $gconfig{'webprefix'} . '/webmin/refresh_modules.cgi"><i class="fa fa-refresh"></i> Refresh</a></li>' . "\n";
}
print '</ul>' . "\n";
print '<div class="navbar-right">' . "\n";
$user = $remote_user;
if (&foreign_available("net")) {
	$user = '<a data-toggle="collapse" data-target="#navbar-collapse" target="page-container" href="' . $gconfig{'webprefix'} . '/acl/edit_user.cgi?user=' . $user .'">' . $user . '</a>';
}
print '<p class="navbar-text pull-left">Welcome, ' . $user . '</p>' . "\n";
&get_miniserv_config(\%miniserv);
if ($miniserv{'logout'} && !$ENV{'SSL_USER'} && !$ENV{'LOCAL_USER'} && $ENV{'HTTP_USER_AGENT'} !~ /webmin/i) {
	if ($main::session_id) {
		print '<a href="'. $gconfig{'webprefix'} . '/session_login.cgi?logout=1" class="btn btn-bwtheme btn-danger navbar-btn pull-right"><i class="fa fa-sign-out"></i> Logout</a>' . "\n";
	} else {
		print '<a href="switch_user.cgi" class="btn btn-bwtheme btn-danger navbar-btn pull-right"> Switch user</a>' . "\n";
	}
}
print '</div>' . "\n";
print '</div>' . "\n";
print '</div>' . "\n";
print '</nav>' . "\n";
print '<aside class="webmin-sidebar hidden-xs">' . "\n";
print '<nav class="navbar-aside" role="navigation">' . "\n";
&print_menu_opener();
@cats = &get_visible_modules_categories();
@modules = map { @{$_->{'modules'}} } @cats;
foreach $cat (@cats) {
	&print_menu_category($cat->{'code'}, $cat->{'desc'});
	&print_sub_category_opener($cat->{'code'});
	foreach $module (@{$cat->{'modules'}}) {
		&print_sub_category($module->{'dir'} . '/', $module->{'desc'}, 'page-container');
	}
	&print_sub_category_closer();
}
&print_menu_closer();
if (-r "$root_directory/webmin_search.cgi" && $gaccess{'webminsearch'}) {
	&print_menu_search();
}
print '</nav>' . "\n";
print '</aside>' . "\n";
print '<div class="iframe-container">' . "\n";
print '<iframe name="page-container" src="' . $goto . '">' . "\n";
print '</iframe>' . "\n";
print '</div>' . "\n";
