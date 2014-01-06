sub theme_header {
	print '<!DOCTYPE HTML>' , "\n";
	print '<html>' , "\n";
	print '<head>' , "\n";
	print '<title>' , $_[0] , '</title>' , "\n";
	print '<meta charset="utf-8">' , "\n";
	print '<meta name="viewport" content="width=device-width, initial-scale=1.0">' . "\n";
	print '<link href="/css/bootstrap.css" rel="stylesheet" type="text/css">' , "\n";
	print '<link href="/css/fontawesome.css" rel="stylesheet" type="text/css">' , "\n";
	print '<link href="/css/default.css" rel="stylesheet" type="text/css">' , "\n";
	print '<script src="/js/jquery.js" type="text/javascript"></script>' , "\n";
	print '<script src="/js/bootstrap.js" type="text/javascript"></script>' , "\n";
	print '</head>' , "\n";
	print '<body>' , "\n";
	
if (@_ > 1) {
	print '<div class="container">' . "\n";
	my %this_module_info = &get_module_info(&get_module_name());
	print "<table class='header' width=100%><tr>\n";
	if ($gconfig{'sysinfo'} == 2 && $remote_user) {
		print "<td id='headln1' colspan=3 align=center>\n";
		print &get_html_status_line(1);
		print "</td></tr> <tr>\n";
		}
	print "<td id='headln2l' width=15% valign=top align=left>";
	if ($ENV{'HTTP_WEBMIN_SERVERS'} && !$tconfig{'framed'}) {
		print "<a href='$ENV{'HTTP_WEBMIN_SERVERS'}'>",
		      "$text{'header_servers'}</a><br>\n";
		}
	if (!$_[5] && !$tconfig{'noindex'}) {
		my @avail = &get_available_module_infos(1);
		my $nolo = $ENV{'ANONYMOUS_USER'} ||
			      $ENV{'SSL_USER'} || $ENV{'LOCAL_USER'} ||
			      $ENV{'HTTP_USER_AGENT'} =~ /webmin/i;
		if ($gconfig{'gotoone'} && $main::session_id && @avail == 1 &&
		    !$nolo) {
			print "<a href='$gconfig{'webprefix'}/session_login.cgi?logout=1'>",
			      "$text{'main_logout'}</a><br>";
			}
		elsif ($gconfig{'gotoone'} && @avail == 1 && !$nolo) {
			print "<a href=$gconfig{'webprefix'}/switch_user.cgi>",
			      "$text{'main_switch'}</a><br>";
			}
		elsif (!$gconfig{'gotoone'} || @avail > 1) {
			print "<a href='$gconfig{'webprefix'}/?cat=",
			      $this_module_info{'category'},
			      "'>$text{'header_webmin'}</a><br>\n";
			}
		}
	if (!$_[4] && !$tconfig{'nomoduleindex'}) {
		my $idx = $this_module_info{'index_link'};
		my $mi = $module_index_link || "/".&get_module_name()."/$idx";
		my $mt = $module_index_name || $text{'header_module'};
		print "<a href=\"$gconfig{'webprefix'}$mi\">$mt</a><br>\n";
		}
	if (ref($_[2]) eq "ARRAY" && !$ENV{'ANONYMOUS_USER'} &&
	    !$tconfig{'nohelp'}) {
		print &hlink($text{'header_help'}, $_[2]->[0], $_[2]->[1]),
		      "<br>\n";
		}
	elsif (defined($_[2]) && !$ENV{'ANONYMOUS_USER'} &&
	       !$tconfig{'nohelp'}) {
		print &hlink($text{'header_help'}, $_[2]),"<br>\n";
		}
	if ($_[3]) {
		my %access = &get_module_acl();
		if (!$access{'noconfig'} && !$config{'noprefs'}) {
			my $cprog = $user_module_config_directory ?
					"uconfig.cgi" : "config.cgi";
			print "<a href=\"$gconfig{'webprefix'}/$cprog?",
			      &get_module_name()."\">",
			      $text{'header_config'},"</a><br>\n";
			}
		}
	print "</td>\n";
	if ($_[1]) {
		# Title is a single image
		print "<td id='headln2c' align=center width=70%>",
		      "<img alt=\"$_[0]\" src=\"$_[1]\"></td>\n";
		}
	else {
		# Title is just text
		my $ts = defined($tconfig{'titlesize'}) ?
				$tconfig{'titlesize'} : "+2";
		print "<td id='headln2c' align=center width=70%>",
		      ($ts ? "<font size=$ts>" : ""),$_[0],
		      ($ts ? "</font>" : "");
		print "<br>$_[9]\n" if ($_[9]);
		print "</td>\n";
		}
	print "<td id='headln2r' width=15% valign=top align=right>";
	print $_[6];
	print "</td></tr></table>\n";
	print $tconfig{'postheader'};
	}
$miniserv::page_capture = 1;
}
sub theme_footer {
for(my $i=0; $i+1<@_; $i+=2) {
	my $url = $_[$i];
	if ($url ne '/' || !$tconfig{'noindex'}) {
		if ($url eq '/') {
			$url = "/?cat=$this_module_info{'category'}";
			}
		elsif ($url eq '' && &get_module_name()) {
			$url = "/".&get_module_name()."/".
			       $this_module_info{'index_link'};
			}
		elsif ($url =~ /^\?/ && &get_module_name()) {
			$url = "/".&get_module_name()."/$url";
			}
		$url = "$gconfig{'webprefix'}$url" if ($url =~ /^\//);
		print "&nbsp;<a href=\"$url\"><i class='fa fa-arrow-left'></i> ",&text('main_return', $_[$i+1]),"</a>\n";
		}
	}
	#If you comment this decomment the </div> in theme_ui_pre_footer, index.cgi, body.cgi
	print "</div>\n";
	print '</body>' , "\n";
	print '</html>' , "\n";
}
sub theme_ui_tabs_start {
	my ($tabs, $name, $sel, $border) = @_;
	my $rv;
	# Output the tabs
	my $imgdir = "$gconfig{'webprefix'}/images";
	$rv .= &ui_hidden($name, $sel)."\n";
	$rv .= '<ul class="nav nav-tabs">' . "\n";
	foreach my $t (@$tabs) {
		my $tabid = "tab_".$t->[0];
		if ($t->[0] eq $sel) {
			# Selected tab
			$rv .= '<li class="active"><a data-toggle="tab" href="#' . $t->[0] . '">' . $t->[1] . '</a></li>' . "\n";
		}
		else {
			# Other tab (which has a link)
			$rv .= '<li><a data-toggle="tab" href="#' . $t->[0] . '">' . $t->[1] . '</a></li>' . "\n";
		}
	}
	$rv .= '</ul>' . "\n";
	$rv .= '<div class="tab-content">' . "\n";
	$main::ui_tabs_selected = $sel;
	return $rv;
}
sub theme_ui_tabs_end {
my $rv;
$rv .= '</div>' . "\n";
return $rv;
}
sub theme_ui_tabs_start_tab {
	my ($name, $tab) = @_;
	my $defclass = $tab eq $main::ui_tabs_selected ?
				' active' : '';
	my $rv = "<div id='$tab' class='tab-pane$defclass'>\n";
	return $rv;
}

sub theme_ui_tabs_end_tab {
	return "</div>\n";
}
sub theme_ui_post_header {
	my ($text) = @_;
	my $rv;
	$rv .= "<hr>\n";
	return $rv;
}
sub theme_ui_pre_footer {
	my $rv;
	$rv .= "<hr>\n";
	#$rv .= '</div>' . "\n";
	return $rv;
}

sub theme_generate_icon {
my $icon = $_[0];
$icon =~ s/.gif/.png/;
my $w = !defined($_[4]) ? "width=48" : $_[4] ? "width=$_[4]" : "";
my $h = !defined($_[5]) ? "height=48" : $_[5] ? "height=$_[5]" : "";
if ($tconfig{'noicons'}) {
	if ($_[2]) {
		print "$_[6]<a href=\"$_[2]\" $_[3]>$_[1]</a>$_[7]\n";
		}
	else {
		print "$_[6]$_[1]$_[7]\n";
		}
	}
elsif ($_[2]) {
	print "<table><tr><td width=48 height=48>\n",
	      "<a href=\"$_[2]\" $_[3]><img src=\"$icon\" alt=\"\" border=0 ",
	      "$w $h></a></td></tr></table>\n";
	print "$_[6]<a href=\"$_[2]\" $_[3]>$_[1]</a>$_[7]\n";
	}
else {
	print "<table><tr><td width=48 height=48>\n",
	      "<img src=\"$icon\" alt=\"\" border=0 $w $h>",
	      "</td></tr></table>\n$_[6]$_[1]$_[7]\n";
	}
}

sub theme_ui_submit {
	my ($label, $name, $dis, $tags) = @_;
	my $rv;
	my $fa;
	my $btntype = 'btn-default';
	if ($name eq 'delete') {
		$btntype = 'btn-danger';
		#$fa = '<i class="fa fa-times"></i>';
	} elsif ($name eq 'stop') {
		$btntype = 'btn-danger';
		#$fa = '<i class="fa fa-exclamation"></i>';
	} elsif ($name eq 'start') {
		$btntype = 'btn-success';
		#$fa = '<i class="fa fa-check"></i>';
	} elsif ($name eq 'restart') {
		$btntype = 'btn-warning';
		#$fa = '<i class="fa fa-refresh"></i>';
	}
	$rv .= '<button type="submit" class="btn ' . $btntype . '" ';
	$rv .= ($name ne '' ? 'name="' . &quote_escape($name) . '" ' : '');
	$rv .= ($dis ? ' disabled="disabled"' : '');
	$rv .= ($tags ? ' ' . $tags : ''). '>';
	$rv .= $fa . ' ' . &quote_escape($label);
	$rv .= '</button>';
	$rv .= "\n";
	return $rv;
}
sub theme_ui_reset {
	my ($label, $dis) = @_;
	my $rv;
	$rv .= '<button class="btn btn-default" type="reset" ';
	$rv .= ($dis ? 'disabled="disabled">' : '>');
	$rv .= &quote_escape($label);
	$rv .= '</button>';
	$rv .= "\n";
	return $rv;
}
sub theme_ui_button {
	my ($label, $name, $dis, $tags) = @_;
	my $rv;
	$rv .= '<button class="btn btn-default" type="button" ';
	$rv .= ($name ne '' ? 'name="' . &quote_escape($name) . '" ' : '');
	$rv .= ($dis ? 'disabled="disabled"' : '');
	$rv .= ($tags ? ' ' . $tags : ''). '>'
	$rv .= &quote_escape($label);
	$rv .= '</button>';
	$rv .= "\n";
	return $rv;
}
sub theme_ui_alert_box {
	my ($msg, $class) = @_;
	my ($rv, $type, $tmsg, $fa);
	
	if ($class eq "success") { $type = 'alert-success', $tmsg = 'Well done!', $fa = 'fa-check'; }
	elsif ($class eq "info") { $type = 'alert-info', $tmsg = 'Heads up!', $fa = 'fa-info'; }
	elsif ($class eq "warn") { $type = 'alert-warning', $tmsg = 'Warning!', $fa = 'fa-exclamation-triangle'; }
	elsif ($class eq "danger") { $type = 'alert-danger', $tmsg = 'Oh snap!', $fa = 'fa-bolt'; }
	
	$rv .= '<div class="alert ' . $type . '">' . "\n";
	$rv .= '<i class="fa fa-fw ' . $fa . '"></i> <strong>' . $tmsg . '</strong>';
	$rv .= '<br>' . "\n";
	$rv .= $msg . "\n";
	$rv .= '</div>';
	$rv .= "\n";
	
	return $rv;
}
