#!/usr/bin/perl
# session_login.cgi
# Display the login form used in session login mode

BEGIN { push(@INC, ".."); };
use WebminCore;
$name = (&get_product_name() eq 'usermin') ? 'Usermin' : 'Webmin';
$pragma_no_cache = 1;
&ReadParse();
&init_config();

%text = &load_language($current_theme);
%gaccess = &get_module_acl(undef, "");
&get_miniserv_config(\%miniserv);
$title = &get_html_framed_title();
$sec = uc($ENV{'HTTPS'}) eq 'ON' ? "; secure" : "";
$sidname = $miniserv{'sidname'} || "sid";
print "Set-Cookie: banner=0; path=/$sec\r\n" if ($gconfig{'loginbanner'});
print "Set-Cookie: $sidname=x; path=/$sec\r\n" if ($in{'logout'});
print "Set-Cookie: testing=1; path=/$sec\r\n";
$charset = &get_charset();
&PrintHeader($charset);
if ($gconfig{'realname'}) {
	$host = &get_display_hostname();
}
else {
	$host = $ENV{'HTTP_HOST'};
	$host =~ s/:\d+//g;
	$host = &html_escape($host);
}
$tag = $gconfig{'noremember'} ? 'autocomplete="off"' : '';
# Look up (there's something wrong with cookies or maybe i think)
print '<!DOCTYPE HTML>' , "\n";
print '<html>' , "\n";
print '<head>' , "\n";
print '<title>' , $title , '</title>' , "\n";
print '<meta charset="utf-8">' , "\n";
print '<meta name="viewport" content="width=device-width, initial-scale=1.0">' . "\n";
print '<link href="' . $gconfig{'webprefix'} . 'unauthenticated/css/bootstrap.css" rel="stylesheet" type="text/css">' , "\n";
print '<link href="' . $gconfig{'webprefix'} . 'unauthenticated/css/fontawesome.css" rel="stylesheet" type="text/css">' , "\n";
print '<link href="' . $gconfig{'webprefix'} . 'unauthenticated/css/login.css" rel="stylesheet" type="text/css">' , "\n";
#print '<script src="' . $gconfig{'webprefix'} . '/unauthenticated/js/jquery.js" type="text/javascript"></script>' , "\n";
#print '<script src="' . $gconfig{'webprefix'} . '/unauthenticated/js/bootstrap.js" type="text/javascript"></script>' , "\n";
print '</head>' , "\n";
print '<body>' . "\n";
print '<div class="container">' . "\n";
print '<div class="row">' . "\n";
if (defined($in{'failed'})) {
	print '<div class="col-xs-12 col-sm-fix">' . "\n";
	print '<div class="message-container">' . "\n";
	if ($in{'twofactor_msg'}) {
		print '<div class="alert alert-danger">' . "\n";
		print '<strong><i class ="fa fa-bolt"></i> Danger!</strong><br />' . &text('session_twofailed', &html_escape($in{'twofactor_msg'})) . "\n";
		print '</div>' . "\n";
	} else {
		print '<div class="alert alert-danger">' . "\n";
		print '<strong><i class ="fa fa-bolt"></i> Danger!</strong><br />' . "\n";
		print $text{'session_failed'} . "\n";
		print '</div>' . "\n";
	}
	print '</div>' . "\n";
	print '</div>' . "\n";
}
elsif ($in{'logout'}) {
	print '<div class="col-xs-12 col-sm-fix">' . "\n";
	print '<div class="message-container">' . "\n";
	print '<div class="alert alert-success">' . "\n";
	print '<strong><i class ="fa fa-check"></i> Success!</strong><br />' . "\n";
	print $text{'session_logout'} . "\n";
	print '</div>' . "\n";
	print '</div>' . "\n";
	print '</div>' . "\n";
}
elsif ($in{'timed_out'}) {
	print '<div class="col-xs-12 col-sm-fix">' . "\n";
	print '<div class="message-container">' . "\n";
	print '<div class="alert alert-warning">' . "\n";
	print '<strong><i class ="fa fa fa-exclamation-triangle"></i> Warning!</strong><br />' . "\n";
	print &text('session_timed_out', int($in{'timed_out'}/60)) . "\n";
	print '</div>' . "\n";
	print '</div>' . "\n";
	print '</div>' . "\n";
}
print '<div class="col-xs-12 col-sm-fix">' . "\n";
print '<div class="login-container">' . "\n";
print '<div class="login-header">' . "\n";
print '<h1><i class="fa fa-cloud"></i> ' . $name . ' ' .  &get_webmin_version() . '</h1>' . "\n";
print '<h2>' . $host . '</h2>' . "\n";
print '</div>' . "\n";
print '<div class="login-body clearfix">' . "\n";
# !! Export the text below in language file (placeholders and p)
print '<p>Please, sign in with your account to manage this server</p>' . "\n";
print '<form method="post" action="' . $gconfig{'webprefix'} . '/session_login.cgi" role="form">' . "\n";
print '<div class="form-group">' . "\n";
print '<div class="input-group">' . "\n";
print '<span class="input-group-addon"><i class="fa fa-fw fa-user"></i></span>' ."\n";
print '<input type="text" class="form-control" placeholder="Username" name="user" ' . $tag . '>' . "\n";
print '</div>' . "\n";
print '</div>' . "\n";
print '<div class="form-group">' . "\n";
print '<div class="input-group">' . "\n";
print '<span class="input-group-addon"><i class="fa fa-fw fa-lock"></i></span>' . "\n";
print '<input type="password" class="form-control" placeholder="Password" name="pass" ' . $tag . '>' . "\n";
print '</div>' . "\n";
print '</div>' . "\n";
if ($miniserv{'twofactor_provider'}) {
	print '<div class="form-group">' . "\n";
	print '<div class="input-group">' . "\n";
	print '<span class="input-group-addon"><i class="fa fa-fw fa-qrcode"></i></span>' . "\n";
	print '<input type="text" class="form-control" placeholder="Token" name="twofactor" autocomplete=off>' . "\n";
	print '</div>' . "\n";
	print '</div>' . "\n";
}
if (!$gconfig{'noremember'}) {
	print '<div class="input-group pull-left">' . "\n";
	print '<input value="1" name="save" id="remember-me" class="remember-me" type="checkbox">' . "\n";
	print '<label class="checkbox remember-me" for="remember-me">' . "\n";
	print '<i class="fa"></i> Remember me' . "\n";
	print '</label>' . "\n";
	print '</div>' . "\n";
}
print '<div class="input-group pull-right">' . "\n";
print '<button type="submit" class="btn btn-primary"><i class="fa fa-sign-in"></i> Sign in</button>' . "\n";
print '</div>' . "\n";
print '</form>' . "\n";
print '</div>' . "\n";
print '</div>' . "\n";
print '</div>' . "\n";
print '</div>' . "\n";
# print '</div>' . "\n"; printed by &footer();
&footer();