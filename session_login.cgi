#############################################################################################################################
# BWTheme 0.9.0 (https://github.com/winfuture/Bootstrap3-Webmin-Theme) - (http://theme.winfuture.it)						#
# Copyright (c) 2015 Riccardo Nobile <riccardo.nobile@winfuture.it> and Simone Cragnolini <simone.cragnolini@winfuture.it>	#
# Licensed under GPLv3 License (https://github.com/winfuture/Bootstrap3-Webmin-Theme/blob/testing/LICENSE)					#
#############################################################################################################################

BEGIN {push(@INC, ".." );};
use WebminCore;
$name = (&get_product_name() eq 'usermin') ? 'Usermin' : 'Webmin';
$pragma_no_cache = 1;
&ReadParse();
&init_config();

%text = &load_language($current_theme);
%gaccess = &get_module_acl(undef, "");
&get_miniserv_config(\%miniserv);

# Get some config parameters
$charset = &get_charset();
$realname = $gconfig{'realname'};
$showhost = $gconfig{'showhost'};
$loginbanner = $gconfig{'loginbanner'};
$webprefix = $gconfig{'webprefix'};
$noremember = $gconfig{'noremember'};
$tag = noremember ? 'autocomplete="off"' : '';

# Define the page title
$title = &get_html_framed_title();
if ($showhost) {
	$title = &get_display_hostname() . " : " . $title;
}

# Define host name
if ($realname) {
	$host = &get_display_hostname();
} else {
	$host = $ENV{'HTTP_HOST'};
	$host =~ s/:\d+//g;
	$host = &html_escape($host);
}

# Show pre login banner if exist
if ($loginbanner && $ENV{'HTTP_COOKIE'} !~ /banner=1/ && !$in{'logout'} && !$in{'failed'} && !$in{'timed_out'} ) {
	print "Set-Cookie: banner=1; path=/\r\n";
	&PrintHeader($charset);
	&LoginHeader($title, $webprefix);
	print '<div class="box-container box-banner">' . "\n";
	&BoxHeader($name, $host);
	print '<div class="box-body clearfix">' . "\n";
	print '<div>' . "\n";
	$url = $in{'page'};
	open(BANNER, $loginbanner);
	while (<BANNER>) {
		s/LOGINURL/$url/g;
		print;
	}
	close(BANNER);
	print '</div>' . "\n";
	print '<div class="input-group pull-right">' . "\n";
	print '<a href="' . $webprefix . '" type="submit" class="btn btn-bwtheme btn-danger"><i class="fa fa-unlock"></i> ' . &text('banner_login') . '</a>' . "\n";
	print '</div>' . "\n";
	print '</div>' . "\n";
	print '</div>' . "\n";
	print '</div>' . "\n";
	&LoginFooter();
	return;
}

# Show login form
$sec = uc($ENV{'HTTPS'}) eq 'ON' ? "; secure" : "";
$sidname = $miniserv{'sidname'} || "sid";
print "Set-Cookie: banner=0; path=/$sec\r\n" if ($loginbanner);
print "Set-Cookie: $sidname=x; path=/$sec\r\n" if ($in{'logout'});
print "Set-Cookie: testing=1; path=/$sec\r\n";
&PrintHeader($charset);
&LoginHeader($title, $webprefix);
if (defined($in{'failed'})) {
	if ($in{'twofactor_msg'}) {
			LoginMessage('alert-danger', 'fa-bolt', $text{'login_danger'} . '!', &text('session_twofailed', &html_escape($in{'twofactor_msg'})));
		} else {
			LoginMessage('alert-danger', 'fa-bolt', $text{'login_danger'} . '!', $text{'session_failed'});
		}
} elsif ($in{'logout'}) {
	LoginMessage('alert-success', 'fa-check', $text{'login_success'} . '!', $text{'session_logout'});
} elsif ($in{'timed_out'}) {
	LoginMessage('alert-warning', 'fa-exclamation-triangle', $text{'login_warning'} . '!', &text('session_timedout', int($in{'timed_out'} / 60)));
}
print '<div class="box-container box-login">' . "\n";
&BoxHeader($name, $host);
print '<div class="box-body clearfix">' . "\n";
print '<div>' . "\n";
print '<p>Please, sign in with your account to manage this server</p>' . "\n";
print '<form method="post" action="' . $webprefix . '/session_login.cgi" role="form">' . "\n";
print '<div class="form-group">' . "\n";
print '<div class="input-group">' . "\n";
print '<span class="input-group-addon"><i class="fa fa-fw fa-user"></i></span>' ."\n";
print '<input type="text" class="form-control" placeholder="' . $text{'login_username'} . '" name="user" ' . $tag . '>' . "\n";
print '</div>' . "\n";
print '</div>' . "\n";
print '<div class="form-group">' . "\n";
print '<div class="input-group">' . "\n";
print '<span class="input-group-addon"><i class="fa fa-fw fa-lock"></i></span>' . "\n";
print '<input type="password" class="form-control" placeholder="' . $text{'login_password'} . '" name="pass" ' . $tag . '>' . "\n";
print '</div>' . "\n";
print '</div>' . "\n";
if ($miniserv{'twofactor_provider'}) {
	print '<div class="form-group">' . "\n";
	print '<div class="input-group">' . "\n";
	print '<span class="input-group-addon"><i class="fa fa-fw fa-qrcode"></i></span>' . "\n";
	print '<input type="text" class="form-control" placeholder="' . $text{'login_token'} . '" name="twofactor" autocomplete=off>' . "\n";
	print '</div>' . "\n";
	print '</div>' . "\n";
}
if (!$noremember) {
	print '<div class="input-group pull-left">' . "\n";
	print '<div class="checkbox">' . "\n";
	print '<input type="checkbox" name="remember-me" id="remember-me" class="remember-me">' . "\n";
	print '<label class="remember-me" for="remember-me">' . $text{'login_remember'} . '</label>' . "\n";
	print '</div>' . "\n";
	print '</div>' . "\n";
}
print '<div class="input-group pull-right">' . "\n";
print '<button type="submit" class="btn btn-bwtheme btn-primary"><i class="fa fa-sign-in"></i> ' . $text{'login_signin'} . '</button>' . "\n";
print '</div>' . "\n";
print '</form>' . "\n";
print '</div>' . "\n";
print '</div>' . "\n";
print '</div>' . "\n";
print '</div>' . "\n";
&LoginFooter();

# Login functions
sub LoginHeader {
	my ($title, $webprefix) = @_;
	print '<!DOCTYPE HTML>' , "\n";
	print '<html>' , "\n";
	print '<head>' , "\n";
	print '<title>' , $title , '</title>' , "\n";
	print '<meta charset="utf-8">' , "\n";
	print '<meta name="viewport" content="width=device-width, initial-scale=1.0">' . "\n";
	print '<link href="' . $webprefix . '/unauthenticated/assets/css/bootstrap.min.css" rel="stylesheet" type="text/css">' , "\n";
	print '<link href="' . $webprefix. '/unauthenticated/assets/css/font-awesome.min.css" rel="stylesheet" type="text/css">' , "\n";
	print '<link href="' . $webprefix. '/unauthenticated/assets/css/bootstrap-checkbox.css" rel="stylesheet" type="text/css">' , "\n";
	print '<link href="' . $webprefix. '/unauthenticated/assets/css/login.css" rel="stylesheet" type="text/css">' , "\n";
	print '<script src="' . $webprefix. '/unauthenticated/assets/js/jquery.min.js" type="text/javascript"></script>' , "\n";
	print '<script src="' . $webprefix. '/unauthenticated/assets/js/bootstrap.min.js" type="text/javascript"></script>' , "\n";
	print '</head>' , "\n";
	print '<body>' . "\n";
	print '<div class="container">' . "\n";
	print '<div class="row">' . "\n";
	print '<div class="col-xs-12 col-sm-fix">' . "\n";
}

sub LoginFooter {
	print '</div>' . "\n";
	print '</div>' . "\n";
	print '</div>' . "\n";
	print '</body>' , "\n";
	print '</html>' , "\n";
}

sub LoginMessage {
	my ($class, $icon, $title, $message) = @_;
	print '<div class="message-container">' . "\n";
	print '<div class="alert ' . $class . '">' . "\n";
	print '<strong><i class ="fa ' . $icon . '"></i> ' . $title . '</strong><br />' . "\n";
	print $message . "\n";
	print '</div>' . "\n";
	print '</div>' . "\n";
}

sub BoxHeader {
	my ($name, $host) = @_;
	print '<div class="box-header">' . "\n";
	print '<h1><i class="fa fa-cloud"></i> ' . $name . ' ' .  &get_webmin_version() . '</h1>' . "\n";
	print '<h2>' . $host . '</h2>' . "\n";
	print '</div>' . "\n";
}
