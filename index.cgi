#!/usr/bin/perl
BEGIN { push(@INC, ".."); };
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
	$in{'page'} ? "" :
	       	      "body.cgi?open=system&open=status";
if ($minfo) {
	$cat = "?$minfo->{'category'}=1";
	}
if ($in{'page'}) {
	$goto .= "/".$in{'page'};
	}
%text = &load_language($current_theme);
%gaccess = &get_module_acl(undef, "");
$title = &get_html_framed_title();
&header($title);
print '<div id="wrapper" class="index">' . "\n";
print '<header>' . "\n";
print '<nav class="navbar navbar-default navbar-fixed-top" role="navigation">' . "\n";
print '<div class="navbar-header">' . "\n";
print '<button type="button" class="navbar-toggle" data-toggle="collapse" data-target="#collapse">' . "\n";
print '<span class="sr-only">Toggle navigation</span>' . "\n";
print '<span class="icon-bar"></span>' . "\n";
print '<span class="icon-bar"></span>' . "\n";
print '<span class="icon-bar"></span>' . "\n";
print '</button>' . "\n";
print '<a class="navbar-brand" target="page" href="body.cgi?open=system&open=status">Webmin ' . &get_webmin_version() . ' - ' . &get_display_hostname() . '</a>' . "\n";
print '</div>' . "\n";
print '<div class="collapse navbar-collapse" id="collapse">' . "\n";
print '<ul class="nav navbar-nav visible-xs">' . "\n";
if ($gconfig{'log'} && &foreign_available("webminlog")) {
	print '<li><a target="page" href="webminlog/" onClick="show_logs(); return false;"><i class="fa fa fa-exclamation-triangle"></i> View Module\'s Logs</a></li>' . "\n";
}
print '<li><a target="page" href="body.cgi?open=system&open=status"><i class="fa fa-home"></i> System Information</a></li>' . "\n";
%gaccess = &get_module_acl(undef, "");
if (&get_product_name() eq 'webmin' && !$ENV{'ANONYMOUS_USER'} && $gconfig{'nofeedbackcc'} != 2 && $gaccess{'feedback'} && $gconfig{'feedback_to'} || &get_product_name() eq 'usermin' && !$ENV{'ANONYMOUS_USER'} && $gconfig{'feedback'}) {
	print '<li><a target="page" href="feedback_form.cgi"><i class="fa fa-envelope"></i> Send Feedback</a></li>' . "\n";
}
if (&foreign_available("webmin")) {
	print '<li><a target="page" href="webmin/refresh_modules.cgi"><i class="fa fa-refresh"></i> Refresh Modules</a></li>' . "\n";
}
print '</ul>' . "\n";
&foreign_require("system-status");
$info = &system_status::get_collected_info();
print '<button style="margin-right: 20px;" class="btn btn-default navbar-btn navbar-left" data-html="true" data-content="';
print '<ul id=\'dashboard\' class=\'list-group\'>';
if ($info->{'cpu'}) {
	@c = @{$info->{'cpu'}};
	$used = $c[0]+$c[1]+$c[3];
	print '<li class=\'list-group-item\'><strong>' . $text{'body_cpuuse'} . '</strong><span class=\'pull-right\'>' . int($used) . '%</span></li>';
	print '<li class=\'list-group-item\'>';
	print '<div class=\'progress progress-striped active\'>';
	print '<div class=\'progress-bar\' role=\'progressbar\' aria-valuenow=\'' . $used . '\' aria-valuemin=\'0\' aria-valuemax=\'100\' style=\'width: ' . $used . '%\'>';
	print '</div>';
	print '</div>';
	print '</li>';
}
if ($info->{'mem'}) {
	@m = @{$info->{'mem'}};
	if (@m && $m[0]) {
		$used = ($m[0]-$m[1])/$m[0]*100;
		print '<li class=\'list-group-item\'><strong>' . $text{'body_real'} . '</strong><span class=\'pull-right\'>' . int($used) . '%</span></li>';
		print '<li class=\'list-group-item\'>';
		print '<div class=\'progress progress-striped active\'>';
		print '<div class=\'progress-bar\' role=\'progressbar\' aria-valuenow=\'' . $used . '\' aria-valuemin=\'0\' aria-valuemax=\'100\' style=\'width: ' . $used . '%\'>';
		print '</div>';
		print '</div>';
		print '</li>';
	}
	if (@m && $m[2]) {
		$used = ($m[2]-$m[3])/$m[2]*100;
		print '<li class=\'list-group-item\'><strong>' . $text{'body_virt'} . '</strong><span class=\'pull-right\'>' . int($used) . '%</span></li>';
		print '<li class=\'list-group-item\'>';
		print '<div class=\'progress progress-striped active\'>';
		print '<div class=\'progress-bar\' role=\'progressbar\' aria-valuenow=\'' . $used . '\' aria-valuemin=\'0\' aria-valuemax=\'100\' style=\'width: ' . $used . '%\'>';
		print '</div>';
		print '</div>';
		print '</li>';
	}
}
if ($info->{'disk_total'}) {
	($total, $free) = ($info->{'disk_total'}, $info->{'disk_free'});
	$used = ($total-$free)/$total*100;
	print '<li class=\'list-group-item\'><strong>' . $text{'body_disk'} . '</strong><span class=\'pull-right\'>' . int($used) . '%</span></li>';
	print '<li class=\'list-group-item\'>';
	print '<div class=\'progress progress-striped active\'>';
	print '<div class=\'progress-bar\' role=\'progressbar\' aria-valuenow=\'' . $used . '\' aria-valuemin=\'0\' aria-valuemax=\'100\' style=\'width: ' . $used . '%\'>';
	print '</div>';
	print '</div>';
	print '</li>';
}
print '</ul>';
print '" data-placement="bottom" data-toggle="popover" data-container="body" type="button" data-original-title="" title="Dashboard"><i class="fa fa-fw fa-dashboard"></i></button>' . "\n";
if ($info->{'cputemps'} || $info->{'drivetemps'}) {
	print '<button style="margin-right: 20px;" class="btn btn-default navbar-btn navbar-left" data-html="true" data-content="';
	print '<ul id=\'temp\' class=\'list-group\'>';
	if ($info->{'cputemps'}) {
		print '<li class=\'list-group-item title\'><strong class=\'text-danger\'>CPU temperatures</strong></li>';
		foreach my $t (@{$info->{'cputemps'}}) {
			print '<li class=\'list-group-item\'><strong>Core ' . $t->{'core'} . '</strong><span class=\'pull-right\'>' . int($t->{'temp'}) . '&#176;C</span></li>';
		}
	}
	if ($info->{'drivetemps'}) {
		print '<li class=\'list-group-item title\'><strong  class=\'text-danger\'>Drive temperatures</strong></li>';
		foreach my $t (@{$info->{'drivetemps'}}) {
			my $short = $t->{'device'};
			$short =~ s/^\/dev\///;
			print '<li class=\'list-group-item\'><strong>' . $short .  '</strong><span class=\'pull-right\'>' . int($t->{'temp'}) . '&#176;C</span></li>';
		}
	}
	print '</ul>';
	print '" data-placement="bottom" data-toggle="popover" data-container="body" type="button" data-original-title="" title="Temperatures"><i class="fa fa-fw fa-fire"></i></button>' . "\n";
}
print '<button class="btn btn-default navbar-btn navbar-left" data-html="true" data-content="';
print '<p>Ciao</p>';
print '" data-placement="bottom" data-toggle="popover" data-container="body" type="button" data-original-title="" title="Temperatures"><i class="fa fa-fw fa-info"></i></button>' . "\n";

if (-r "$root_directory/webmin_search.cgi" && $gaccess{'webminsearch'}) {
	print '<form action="webmin_search.cgi" target="page" class="navbar-form navbar-right" role="search">' . "\n";
	print '<div class="form-group">' . "\n";
	print '<input type="text" class="form-control" name="search" placeholder="Search">' . "\n";
	print '</div>' . "\n";
	print '</form>' . "\n";
}
	$user = $remote_user;
	if (&foreign_available("net")) {
		$user = '<a target="page" href="acl/">' . $user . '</a>';
	}
	print '<p class="navbar-text navbar-right">Welcome ' . $user . '</p>' . "\n";
&get_miniserv_config(\%miniserv);
if ($miniserv{'logout'} && !$ENV{'SSL_USER'} && !$ENV{'LOCAL_USER'} && $ENV{'HTTP_USER_AGENT'} !~ /webmin/i) {
	if ($main::session_id) {
		print '<a href="session_login.cgi?logout=1" class="btn btn-danger navbar-btn navbar-right"><i class="fa fa-sign-out"></i> ' . $text{'main_logout'} . '</a>' . "\n";
	} else {
		print '<a href="switch_user.cgi" class="btn btn-danger navbar-btn navbar-right">' . $text{'main_switch'} . '</a>' . "\n";
	}
}
print '</div>' . "\n";
print '</nav>' . "\n";
print '</header>' . "\n" . "\n";
print '<aside id="sidebar" class="hidden-xs">' . "\n" . "\n";
print '<div>' . "\n";
print '<ul class="navigation">' . "\n";
@cats = &get_visible_modules_categories();
@modules = map { @{$_->{'modules'}} } @cats;
if ($gconfig{"notabs_${base_remote_user}"} == 2 || $gconfig{"notabs_${base_remote_user}"} == 0 && $gconfig{'notabs'} || @modules <= 1) {
	foreach $minfo (@modules) {
		$target = $minfo->{'noframe'} ? "_top" : "right";
		print "<a target=$target href=$minfo->{'dir'}/>$minfo->{'desc'}</a><br>\n";
		}
	}
else {
	foreach $c (@cats) {
		# Show category opener, plus modules under it
		&print_category_opener($c->{'code'}, $in{$c->{'code'}} ? 1 : 0, $c->{'unused'} ? "<font color=#888888>$c->{'desc'}</font>" : $c->{'desc'});
		$cls = $in{$c->{'code'}} ? "itemshown" : "itemhidden";
		print '<ul style="display: none;" id="' . $c->{'code'} . '">' . "\n";
		foreach my $minfo (@{$c->{'modules'}}) {
			&print_category_link("$minfo->{'dir'}/",
					     $minfo->{'desc'},
					     undef,
					     undef,
					     $minfo->{'noframe'} ? "_top" : "",
					);
			}
		print '</ul>' . "\n";
		}
	}
print '</ul>' . "\n";
print '</div>' . "\n";
print '</aside>' . "\n";
print '<div id="wrapper" class="menu">' . "\n";
print '<iframe name="page" src="' . $goto . '">' . "\n";
print '</iframe>' . "\n";
print '</div>' . "\n";
print '</div>' . "\n";
print '<script>' . "\n";
print '$("[data-toggle=popover]").popover()' . "\n";
print '</script>' . "\n";
print '<script src="js/ajax.js" type="text/javascript"></script>' , "\n";
print '<script src="js/application.js" type="text/javascript"></script>' , "\n";
&footer();

# print_category_opener(name, &allcats, label)
# Prints out an open/close twistie for some category
sub print_category_opener {
local ($c, $status, $label) = @_;
$label = $c eq "others" ? $text{'left_others'} : $label;
local $img = $status ? "gray-open.gif" : "gray-closed.gif";

# Show link to close or open catgory
print '<li>' . "\n";
print '<a href="#' . $c . '"> ' . $label . '</a>' . "\n";
print '</li>' . "\n";
}


sub print_category_link {
local ($link, $label, $image, $noimage, $target) = @_;
$target ||= "page";
print '<li>' . "\n";
print '<a target="' . $target . '" href="' . $link . '"> ' . $label . '</a>' . "\n";
print '</li>' . "\n";
}