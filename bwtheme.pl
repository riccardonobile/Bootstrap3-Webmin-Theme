#############################################################################################################################
# BWTheme 0.9.5 (https://github.com/winfuture/Bootstrap3-Webmin-Theme) - (http://theme.winfuture.it)						#
# Copyright (c) 2015 Riccardo Nobile <riccardo.nobile@winfuture.it> and Simone Cragnolini <simone.cragnolini@winfuture.it>	#
# Licensed under GPLv3 License (https://github.com/winfuture/Bootstrap3-Webmin-Theme/blob/testing/LICENSE)					#
#############################################################################################################################

sub theme_header {
	print '<!DOCTYPE HTML>' , "\n";
	print '<html>' , "\n";
	print '<head>' , "\n";
	print '<title>' , $_[0] , '</title>' , "\n";
	print '<meta charset="utf-8">' , "\n";
	print '<meta name="viewport" content="width=device-width, initial-scale=1.0">' . "\n";
	print '<link href="'. $gconfig{'webprefix'} . '/unauthenticated/assets/css/bootstrap.min.css" rel="stylesheet" type="text/css">' , "\n";
	print '<link href="'. $gconfig{'webprefix'} . '/unauthenticated/assets/css/font-awesome.min.css" rel="stylesheet" type="text/css">' , "\n";
	print '<link href="'. $gconfig{'webprefix'} . '/unauthenticated/assets/css/bootstrap-checkbox.css" rel="stylesheet" type="text/css">' , "\n";
	print '<link href="'. $gconfig{'webprefix'} . '/unauthenticated/assets/css/bootstrap-select.min.css" rel="stylesheet" type="text/css">' , "\n";
	print '<link href="'. $gconfig{'webprefix'} . '/unauthenticated/assets/css/bwtheme.css" rel="stylesheet" type="text/css">' , "\n";
	print '<link href="'. $gconfig{'webprefix'} . '/unauthenticated/assets/css/circleprogress.css" rel="stylesheet" type="text/css">' , "\n";
	print '<link href="'. $gconfig{'webprefix'} . '/favicon.ico" rel="icon" sizes="16x16">' , "\n";
	print '<script src="'. $gconfig{'webprefix'} . '/unauthenticated/assets/js/jquery.min.js" type="text/javascript"></script>' , "\n";
	print '<script src="'. $gconfig{'webprefix'} . '/unauthenticated/assets/js/bootstrap.min.js" type="text/javascript"></script>' , "\n";
	print '<script src="'. $gconfig{'webprefix'} . '/unauthenticated/assets/js/bootstrap-select.min.js" type="text/javascript"></script>' , "\n";
	print '<script src="'. $gconfig{'webprefix'} . '/unauthenticated/assets/js/bwtheme.js" type="text/javascript"></script>' , "\n";
	print '</head>' , "\n";
	print '<body>' , "\n";

if (@_ > 1) {
	print '<div class="container">' . "\n";
	my %this_module_info = &get_module_info(&get_module_name());
	print '<div class="panel panel-default" style="margin-top: 20px">' . "\n";
	print '<div class="panel-heading">' . "\n";
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
	print '</div>' . "\n";
	print '<div class="panel-body">' . "\n";
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
		print "&nbsp;<a style='margin-bottom: 15px;' class='btn btn-primary' href=\"$url\"><i class='fa fa-arrow-left'></i> ",&text('main_return', $_[$i+1]),"</a>\n";
		}
	}
	#If you comment this </div>, decomment the </div> commented in theme_ui_pre_footer, index.cgi, body.cgi
	print "</div>\n";
	print '</body>' , "\n";
	print '</html>' , "\n";
}
sub theme_file_chooser_button
{
my $form = defined($_[2]) ? $_[2] : 0;
my $chroot = defined($_[3]) ? $_[3] : "/";
my $add = int($_[4]);
my ($w, $h) = (400, 300);
if ($gconfig{'db_sizefile'}) {
	($w, $h) = split(/x/, $gconfig{'db_sizefile'});
	}
return "<button class='btn btn-bwtheme btn-default' type=button onClick='ifield = form.$_[0]; chooser = window.open(\"$gconfig{'webprefix'}/chooser.cgi?add=$add&type=$_[1]&chroot=$chroot&file=\"+escape(ifield.value), \"chooser\", \"toolbar=no,menubar=no,scrollbars=no,resizable=yes,width=$w,height=$h\"); chooser.ifield = ifield; window.ifield = ifield'>...</button>\n";
}
sub theme_popup_window_button
{
my ($url, $w, $h, $scroll, $fields) = @_;
my $scrollyn = $scroll ? "yes" : "no";
my $rv = "<input class='btn btn-bwtheme btn-default' type=button onClick='";
foreach my $m (@$fields) {
	$rv .= "$m->[0] = form.$m->[1]; ";
	}
my $sep = $url =~ /\?/ ? "&" : "?";
$rv .= "chooser = window.open(\"$url\"";
foreach my $m (@$fields) {
	if ($m->[2]) {
		$rv .= "+\"$sep$m->[2]=\"+escape($m->[0].value)";
		$sep = "&";
		}
	}
$rv .= ", \"chooser\", \"toolbar=no,menubar=no,scrollbars=$scrollyn,resizable=yes,width=$w,height=$h\"); ";
foreach my $m (@$fields) {
	$rv .= "chooser.$m->[0] = $m->[0]; ";
	$rv .= "window.$m->[0] = $m->[0]; ";
	}
$rv .= "' value=\"...\">";
return $rv;
}
sub theme_ui_upload
{
my ($name, $size, $dis, $tags) = @_;
$size = &ui_max_text_width($size);
return "<input style='margin: 4px 0;' class='btn btn-bwtheme btn-default' type=file name=\"".&quote_escape($name)."\" ".
       "size=$size ".
       ($dis ? "disabled=true" : "").
       ($tags ? " ".$tags : "").">";
}

# Thi is the web-lib-funcs.pl part dedicated to all web lib functions.
# WARNING!!! Work in progress - Not all is implemented!!!

################################# Theme icons generation functions #################################

# ff
sub theme_icons_table {
	print '<div class="row icons-row">' . "\n";
	for(my $i=0; $i<@{$_[0]}; $i++) {
		print '<div style="text-align: center;" class="col-xs-6 col-sm-4 col-md-3">' . "\n";
		&generate_icon($_[2]->[$i], $_[1]->[$i], $_[0]->[$i], ref($_[4]) ? $_[4]->[$i] : $_[4], $_[5], $_[6], $_[7]->[$i], $_[8]->[$i]);
		print '</div>' . "\n";
	}
	print '</div>' . "\n";
}

sub theme_generate_icon {
	my ($icon, $title, $link, $href, $width, $height, $before, $after) = @_;
	# Decomment only when new icons are ready
	$icon =~ s/.gif/.png/;
	$width = !defined($width) ? '48' : $width;
	$height = !defined($height) ? '48' : $height;

	if ($tconfig{'noicons'}) {
		if ($link) {
			print '<div>';
			print $before;
			print '<a href="' . $link . '" ' . $href . '>' . $title . '</a>';
			print $after;
			print '</div>';
		} else {
			print '<div>';
			print $before;
			print $title;
			print $after;
			print '</div>';
		}
	} elsif ($link) {
		print '<div style="height: 120px;" class="icon-container">';
		print '<a href="' . $link . '" ' . $href . '><img style="padding: 7px; border-radius: 4px; border: 1px solid #DDD; background: linear-gradient(to bottom, #FCFCFC 0%, #F5F5F5 100%) repeat scroll 0% 0% transparent; width: 64px; height: 64px; box-shadow: 0px 1px 1px rgba(0, 0, 0, 0.05);" src="' . $icon . '" width="' . $width . '" height="' . $height . '">';
		print $before;
		print '<a href="' . $link . '" ' . $href . '><p>' . $title . '</p></a>';
		print $after;
		print '</div>';
	} else {
		print '<div class="icon-container">';
		print '<img style="padding: 7px; border-radius: 4px; border: 1px solid #DDD; background: linear-gradient(to bottom, #FCFCFC 0%, #F5F5F5 100%) repeat scroll 0% 0% transparent; width: 64px; height: 64px; box-shadow: 0px 1px 1px rgba(0, 0, 0, 0.05);" src="' . $icon . '" width="' . $width . '" height="' . $height . '">';
		print $before;
		print '<p>' . $title . '</p>';
		print $after;
		print '</div>';
	}
}

# Thi is the bwtheme.pl part dedicated to all theme functions.
# WARNING!!! Work in progress - Not all is implemented!!!
# All the # theme_ui_x are are not yet implemented theme functions.

################################# Theme table generation functions #################################

sub theme_ui_link {
	my ($href, $text, $class, $tags) = @_;
	my $rv;

	$rv .= '<a class="bwtheme-link';
	$rv .= ($class ? ' ' . $class : '');
	$rv .= '" href="' . $href . '"';
	$rv .= ($tags ? ' ' . $tags : '');
	$rv .= '>' . $text . '</a>' . "\n";

	return $rv;
}

sub theme_ui_table_start {
	my ($heading, $tabletags, $cols, $tds, $rightheading) = @_;
	if (defined($main::ui_table_cols)) {
		push(@main::ui_table_cols_stack, $main::ui_table_cols);
		push(@main::ui_table_pos_stack, $main::ui_table_pos);
		push(@main::ui_table_default_tds_stack, $main::ui_table_default_tds);
	}
	my $colspan = 1;
	my $rv;

	$rv .= "<table width=100% class='ui_table' border $tabletags>\n";
	if (defined($heading) || defined($rightheading)) {
		$rv .= "<tr".($tb ? " ".$tb : "")." class='ui_table_head'>";
		if (defined($heading)) {
			$rv .= "<td><b>$heading</b></td>"
			}
		if (defined($rightheading)) {
			$rv .= "<td align=right>$rightheading</td>";
			$colspan++;
			}
		$rv .= "</tr>\n";
		}
	$rv .= "<tr".($cb ? " ".$cb : "")." class='ui_table_body'> <td colspan=$colspan>".
	       "<table width=100%>\n";
	$main::ui_table_cols = $cols || 4;
	$main::ui_table_pos = 0;
	$main::ui_table_default_tds = $tds;
	return $rv;
}

sub theme_ui_table_end {
	my $rv;
	if ($main::ui_table_cols == 4 && $main::ui_table_pos) {
		# Add an empty block to balance the table
		$rv .= &ui_table_row(" ", " ");
	}
	if (@main::ui_table_cols_stack) {
		$main::ui_table_cols = pop(@main::ui_table_cols_stack);
		$main::ui_table_pos = pop(@main::ui_table_pos_stack);
		$main::ui_table_default_tds = pop(@main::ui_table_default_tds_stack);
	}
	else {
		$main::ui_table_cols = undef;
		$main::ui_table_pos = undef;
		$main::ui_table_default_tds = undef;
	}
	$rv .= "</table></td></tr></table>\n";
	return $rv;
}

# theme_ui_table_row

# theme_ui_table_hr

# theme_ui_table_span

sub theme_ui_columns_start {
	my ($heads, $width, $noborder, $tdtags, $title) = @_;
	my ($rv, $i);

	$rv .= '<table width=100% class="table table-striped table-rounded">' . "\n";
	$rv .= '<thead>' . "\n";
	$rv .= '<tr>' . "\n";
	for($i=0; $i<@$heads; $i++) {
		$rv .= '<th>';
		$rv .= ($heads->[$i] eq '' ? '<br>' : $heads->[$i]);
		$rv .= '</th>' . "\n";
	}
	$rv .= '</tr>' . "\n";
	$rv .= '</thead>' . "\n";

	return $rv;
}

sub theme_ui_columns_row {
	my ($cols, $tdtags) = @_;
	my ($rv, $i);

	#$rv .= '<tbody>' . "\n";
	$rv .= '<tr>' . "\n";
	for($i=0; $i<@$cols; $i++) {
		$rv .= '<td>' . "\n";
		$rv .= ($cols->[$i] !~ /\S/ ? '<br>' : $cols->[$i]);
		$rv .= '</td>' . "\n";
	}
	$rv .= '</tr>' . "\n";
	#$rv .= '</tbody>' . "\n";

	return $rv;
}

sub theme_ui_columns_header {
	my ($cols, $tdtags) = @_;
	my ($rv, $i);

	$rv .= '<thead>' . "\n";
	$rv .= '<tr>' . "\n";
	for($i=0; $i<@$cols; $i++) {
		$rv .= '<th>';
		$rv .= ($cols->[$i] eq '' ? '#' : $cols->[$i]);
		$rv .= '</th>' . "\n";
	}
	$rv .= '</tr>' . "\n";
	$rv .= '</thead>' . "\n";

	return $rv;
}

# theme_ui_checked_columns_row

# theme_ui_radio_columns_row

sub theme_ui_columns_end {
	my $rv;

	$rv .= '</table>' . "\n";

	return $rv;
}

# theme_ui_columns_table

# theme_ui_form_columns_table

################################# Theme form generation functions #################################

sub theme_ui_form_start {
	my ($script, $method, $target, $tags) = @_;
	my $rv;

	$rv .= '<form role="form" ';
	$rv .= 'action="' . &html_escape($script) . '" ';
	$rv .= ($method eq 'post' ? 'method="post" ' : $method eq 'form-data' ? 'method="post" enctype="multipart/form-data" ' : 'method="get" ');
	$rv .= ($target ? 'target="' . $target . '" ' : '');
	$rv .= ($tags ? $tags : '');
	$rv .= '>' . "\n";

	return $rv;
}

# theme_ui_form_end

sub theme_ui_textbox {
	my ($name, $value, $size, $dis, $max, $tags) = @_;
	my $rv;

	$rv .= '<input style="display: inline; width: auto;" class="form-control" type="text" ';
	$rv .= 'name="' . &quote_escape($name) . '" ';
	$rv .= 'value="' . &quote_escape($value) . '" ';
	$rv .= 'size="' . $size . '" ';
	$rv .= ($dis ? 'disabled="true" ' : '');
	$fv .= ($max ? 'maxlength="' . $max . '" ' : '');
	$rv .= ($tags ? $tags : '');
	$rv .= '>' . "\n";

	return $rv;
}

# theme_ui_filebox

# theme_ui_upload

sub theme_ui_password {
	my ($name, $value, $size, $dis, $max, $tags) = @_;
	my $rv;

	$rv .= '<input style="display: inline; width: auto;" class="form-control" type="password" ';
	$rv .= 'name="' . &quote_escape($name) . '" ';
	$rv .= 'value="' . &quote_escape($value) . '" ';
	$rv .= 'size="' . $size . '" ';
	$rv .= ($dis ? 'disabled="true" ' : '');
	$fv .= ($max ? 'maxlength="' . $max . '" ' : '');
	$rv .= ($tags ? $tags : '');
	$rv .= '>' . "\n";

	return $rv;
}

sub ui_hidden {
	my ($name, $value) = @_;
	my $rv;

	$rv .= '<input style="display: none;" type="hidden" ';
	$rv .= 'name="' . &quote_escape($name) . '" ';
	#$rv .= 'id="' . &quote_escape($name) . '" ';
	$rv .= 'value="' . &quote_escape($value) . '" ';
	$rv .= '>' . "\n";

	return $rv;
}

sub theme_ui_select {
	my ($name, $value, $opts, $size, $multiple, $missing, $dis, $tags) = @_;
	my $rv;

	$rv .= '<select class="selectpicker" data-width="auto" name="' . &quote_escape($name) . '" id="' . &quote_escape($name) . '"';
	$rv .= ($multiple ? ' multiple' : '');
	$rv .= ($size ? ' size="' . $size . '"' : '');
	$rv .= ($dis ? ' disabled="true"' : '');
	$rv .= ($tags ? ' ' . $tags : '') . '>' . "\n";

	my ($o, %opt, $s);
	my %sel = ref($value) ? (map { $_, 1 } @$value) : ( $value, 1);

	foreach $o (@$opts) {
		$o = [ $o ] if (!ref($o));
		$rv .= "<option value=\"".&quote_escape($o->[0])."\"".
		       ($sel{$o->[0]} ? " selected" : "").($o->[2] ne '' ? " ".$o->[2] : "").">".
		       ($o->[1] || $o->[0])."</option>\n";
		$opt{$o->[0]}++;
	}
	foreach $s (keys %sel) {
		if (!$opt{$s} && $missing) {
			$rv .= "<option value=\"".&quote_escape($s)."\" selected>".($s eq "" ? "&nbsp;" : $s)."</option>\n";
		}
	}

	$rv .= '</select>' . "\n";
	return $rv;
}

# theme_ui_multi_select

# theme_ui_multiselect_javascript

sub theme_ui_radio {
	my ($name, $value, $opts, $dis) = @_;
	my $rv;
	my $o;
	foreach $o (@$opts) {
		my $id = &quote_escape($name."_".$o->[0]);
		my $label = $o->[1] || $o->[0];
		my $after;

		if ($label =~ /^([\000-\377]*?)((<a\s+href|<input|<select|<textarea|<span|<br|<p)[\000-\377]*)$/i) {
			$label = $1;
			$after = $2;
		}

		$rv .= '<div style="margin: 0" class="radio">';
		$rv .= '<input type="radio" name="' . &quote_escape($name) . '" value="' . &quote_escape($o->[0]) . '" id="' . $id . '"';
		$rv .= ($o->[0] eq $value ? ' checked' : '') . ($dis ? ' disabled=true' : '') . ($o->[2] ? ' ' . $o->[2] : '');
		$rv .= '>';
		$rv .= '<label for="' . $id . '">' . $label . "</label>" . $after;
		$rv .= '</div>' . "\n";
	}

	return $rv;
}

sub theme_ui_yesno_radio {
	my ($name, $value, $yes, $no, $dis) = @_;
	my $rv;

	$yes = 1 if (!defined($yes));
	$no = 0 if (!defined($no));
	$value = int($value);

	$rv = &ui_radio($name, $value, [ [ $yes, $text{'yes'} ], [ $no, $text{'no'} ] ], $dis);

	return $rv;
}

sub theme_ui_checkbox {
	my ($name, $value, $label, $sel, $tags, $dis) = @_;
	my $after, $rv;
	my $id = &quote_escape("${name}_${value}");

	if ($label =~ /^([^<]*)(<[\000-\377]*)$/) {
		$label = $1;
		$after = $2;
	}

	$rv = '<div style="margin: 0" class="checkbox">';
	$rv .= '<input type="checkbox" name="' . &quote_escape($name) . '" value="' . &quote_escape($value) . '" id="' . $id . '"';
	$rv .= ($sel ? ' checked' : '') . ($dis ? ' disabled=true' : '');
	$rv .= '>';
	$rv .= '<label for="' . $id . '">' . $label . "</label>" . $after;
	$rv .= '</div>' . "\n";

	return $rv;
}

sub theme_ui_oneradio {
	my ($name, $value, $label, $sel, $tags, $dis) = @_;
	my $id = &quote_escape("${name}_${value}");
	my $after, $rv;

	if ($label =~ /^([^<]*)(<[\000-\377]*)$/) {
		$label = $1;
		$after = $2;
	}

	$rv = '<div style="margin: 0" class="radio">';
	$rv .= '<input type="radio" name="' . &quote_escape($name) . '" value="' . &quote_escape($value) . '" id="' . $id . '"';
	$rv .= ($sel ? ' checked' : '') . ($dis ? ' disabled=true' : '');
	$rv .= '>';
	$rv .= '<label for="' . $id . '">' . $label . "</label>" . $after;
	$rv .= '</div>' . "\n";

	return $rv;
}

sub theme_ui_textarea {
	my ($name, $value, $rows, $cols, $wrap, $dis, $tags) = @_;
	my $rv;
	$cols = &ui_max_text_width($cols, 1);

	$rv .= '<textarea style="display: inline; width: auto;" class="form-control" ';
	$rv .= 'name="' . &quote_escape($name) . '" ';
	$rv .= 'rows="' . $rows . '" ';
	$rv .= 'cols="' . $cols . '" ';
	$rv .= ($wrap ? 'wrap="' . $wrap . '" ' : '');
	$rv .= ($dis ? 'disabled="true" ' : '');
	$rv .= ($tags ? $tags : '');
	$rv  .= '>' . &html_escape($value) . '</textarea>' . "\n";

	return $rv;
}

sub theme_ui_user_textbox {
	my ($name, $value, $form, $dis, $tags) = @_;
	my $rv;

	$rv .= &ui_textbox($name, $value, 13, $dis, undef, $tags);
	$rv .= " ";
	$rv .= &user_chooser_button($name, 0, $form);

	return $rv;
}

sub theme_ui_group_textbox {
	my ($name, $value, $form, $dis, $tags) = @_;
	my $rv;

	$rv .= &ui_textbox($name, $value, 13, $dis, undef, $tags);
	$rv .= " ";
	$rv .= &user_chooser_button($name, 0, $form);

	return $rv;
}

sub theme_ui_opt_textbox {
	my ($name, $value, $size, $opt1, $opt2, $dis, $extra, $max, $tags) = @_;
	my $dis1 = &js_disable_inputs([ $name, @$extra ], [ ]);
	my $dis2 = &js_disable_inputs([ ], [ $name, @$extra ]);
	my $rv;
	$size = &ui_max_text_width($size);
	$rv .= &ui_radio($name."_def", $value eq '' ? 1 : 0,
			 [ [ 1, $opt1, "onClick='$dis1'" ],
			   [ 0, $opt2 || " ", "onClick='$dis2'" ] ], $dis)."\n";
	$rv .= "<input class='ui_opt_textbox form-control' type='text' ".
	       "name=\"".&quote_escape($name)."\" ".
	       "id=\"".&quote_escape($name)."\" ".
	       "size=$size value=\"".&quote_escape($value)."\"".
	       ($dis ? " disabled" : "").
	       ($max ? " maxlength=$max" : "").
	       ($tags ? " ".$tags : "").">";
	return $rv;
}

sub theme_ui_submit {
	my ($label, $name, $dis, $tags) = @_;
	my ($rv, $fa);
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

	$rv .= '<button type="submit" class="btn btn-bwtheme ' . $btntype . '" ';
	$rv .= ($name ne '' ? 'name="' . &quote_escape($name) . '" ' : '');
	$rv .= ($name ne '' ? 'id="' . &quote_escape($name) . '" ' : '');
	$rv .= ' value="' . &quote_escape($label) . '"'.
	$rv .= ($dis ? ' disabled="disabled"' : '');
	$rv .= ($tags ? ' ' . $tags : ''). '>';
	$rv .= $fa . ' ' . &quote_escape($label);
	$rv .= '</button>' . "\n";

	return $rv;
}

sub theme_ui_reset {
	my ($label, $dis) = @_;
	my $rv;

	$rv .= '<button class="btn btn-bwtheme btn-default" type="reset" ';
	$rv .= ($dis ? 'disabled="disabled">' : '>');
	$rv .= &quote_escape($label);
	$rv .= '</button>' . "\n";

	return $rv;
}

sub theme_ui_button {
	my ($label, $name, $dis, $tags) = @_;
	my $rv;

	$rv .= '<button type="button" class="btn btn-bwtheme btn-default" ';
	$rv .= ($name ne '' ? 'name="' . &quote_escape($name) . '" ' : '');
	$rv .= ($dis ? 'disabled="disabled"' : '');
	$rv .= ($tags ? ' ' . $tags : ''). '>';
	$rv .= &quote_escape($label);
	$rv .= '</button>' . "\n";

	return $rv;
}

# theme_ui_date_input

# theme_ui_buttons_start

# theme_ui_buttons_end

# theme_ui_buttons_row

# theme_ui_buttons_hr

################################# Theme header and footer functions #################################

sub theme_ui_post_header {
	my ($text) = @_;

	my $rv;
	#$rv .= '<hr>' . "\n";

	return $rv;
}

sub theme_ui_pre_footer {
	my $rv;

	#$rv .= '<hr>' . "\n";
	$rv .= '</div>' . "\n";
	$rv .= '</div>' . "\n";
	#$rv .= '</div>' . "\n";

	return $rv;
}

# theme_ui_print_header

# theme_ui_print_unbuffered_header

# theme_ui_print_footer

# theme_ui_config_link

# theme_ui_print_endpage

# theme_ui_subheading

# theme_ui_links_row

################################# Theme collapsible section / tab functions #################################

# theme_ui_hidden_javascript

# theme_ui_hidden_start

# theme_ui_hidden_end

# theme_ui_hidden_table_row_start

# theme_ui_hidden_table_row_end

# theme_ui_hidden_table_start

# theme_ui_hidden_table_end

sub theme_ui_tabs_start {
	my ($tabs, $name, $sel, $border) = @_;
	my $rv;

	$rv .= '<ul class="nav nav-tabs">' . "\n";
	foreach my $t (@$tabs) {
		my $tabid = "tab_".$t->[0];
		if ($t->[0] eq $sel) {
			$rv .= '<li class="active"><a data-toggle="tab" href="#' . $t->[0] . '">' . $t->[1] . '</a></li>' . "\n";
		} else {
			$rv .= '<li><a data-toggle="tab" href="#' . $t->[0] . '">' . $t->[1] . '</a></li>' . "\n";
		}
	}
	$rv .= '</ul>' . "\n";
	$rv .= '<div class="tab-content">' . "\n";
	$main::ui_tabs_selected = $sel;

	return $rv;
}

sub theme_ui_tabs_end {
	my ($border) = @_;
	my $rv;

	$rv .= '</div>' . "\n";

	return $rv;
}

sub theme_ui_tabs_start_tab {
	my ($name, $tab) = @_;
	my $rv;
	my $defclass = $tab eq $main::ui_tabs_selected ? 'active' : '';

	$rv .= '<div id="' . $tab . '" class="tab-pane ' . $defclass . '">' . "\n";

	return $rv;
}

# theme_ui_tabs_start_tabletab

sub theme_ui_tabs_end_tab {
	my $rv;

	$rv .= '</div>' . "\n";

	return $rv;
}

# theme_ui_tabs_end_tabletab

# theme_ui_radio_selector

################################# Theme collapsible section / tab functions #################################

# theme_ui_grid_table

sub theme_ui_grid_table {
	my ($elements, $cols, $width, $tds, $tabletags, $title) = @_;
	return "" if (!@$elements);
	my $rv = "<table width=100% class='ui_grid_table'".
		    ($width ? " width=$width%" : "").
		    ($tabletags ? " ".$tabletags : "").
		    ">\n";
	my $i;
	for($i=0; $i<@$elements; $i++) {
		$rv .= "<tr class='ui_grid_row'>" if ($i%$cols == 0);
		$rv .= "<td ".$tds->[$i%$cols]." valign=top class='ui_grid_cell'>".
		       $elements->[$i]."</td>\n";
		$rv .= "</tr>" if ($i%$cols == $cols-1);
		}
	if ($i%$cols) {
		while($i%$cols) {
			$rv .= "<td ".$tds->[$i%$cols]." class='ui_grid_cell'>".
			       "<br></td>\n";
			$i++;
			}
		$rv .= "</tr>\n";
		}
	$rv .= "</table>\n";
	if (defined($title)) {
		$rrv = $rv;
		$rv = '<div class="panel panel-default">' . "\n";
		$rv .= '<div class="panel-heading">' . "\n";
		$rv .= $title . "\n";
		$rv .= '</div>' . "\n";
		$rv .= '<div class="panel-body">' . "\n";
		$rv .= "<table width=100% class=ui_table border='0' ".
			($width ? " width=$width%" : "").">\n".
				"<tr><td>$rrv</td></tr>\n".
			"</table>";
		$rv .= '</div>' . "\n";
		$rv .= '</div>' . "\n";
		}
	return $rv;
}

# theme_ui_radio_table

# theme_ui_up_down_arrows

sub theme_ui_hr {
	my $rv;

	$rv .= '<hr>' . "\n";

	return $rv;
}

# theme_ui_nav_link

# theme_ui_confirmation_form !!!!! NB: Not available to override ?????

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
	$rv .= '</div>' . "\n";

	return $rv;
}

# theme_ui_page_flipper

sub theme_js_redirect {
	my ($url, $window) = @_;
	my $rv;

	$window ||= "window";
	if ($url =~ /^\//) {
		# If the URL is like /foo , add webprefix
		$url = $gconfig{'webprefix'}.$url;
	}

	$rv .= "<script type='text/javascript'>" . ${window} . '.location = ' . &quote_escape($url) . ';</script>' . "\n";

	return $rv;
}
