#!/usr/bin/perl
BEGIN { push(@INC, ".."); };
use WebminCore;
&ReadParse();
&init_config();
%text = &load_language($current_theme);
%gaccess = &get_module_acl(undef, "");
&foreign_require("system-status");
$info = &system_status::get_collected_info();
$charset = &get_charset();
&PrintHeader($charset);
if ($info->{'cpu'}) {
	@c = @{$info->{'cpu'}};
	$used = $c[0]+$c[1]+$c[3];
	print '<li class=\'list-group-item\'><strong>' . $text{'body_cpuuse'} . '</strong><p class=\'pull-right\'>' . int($used) . '%</p></li>';
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
		print '<li class=\'list-group-item\'><strong>' . $text{'body_real'} . '</strong><p class=\'pull-right\'>' . int($used) . '%</p></li>';
		print '<li class=\'list-group-item\'>';
		print '<div class=\'progress progress-striped active\'>';
		print '<div class=\'progress-bar\' role=\'progressbar\' aria-valuenow=\'' . $used . '\' aria-valuemin=\'0\' aria-valuemax=\'100\' style=\'width: ' . $used . '%\'>';
		print '</div>';
		print '</div>';
		print '</li>';
	}
	if (@m && $m[2]) {
		$used = ($m[2]-$m[3])/$m[2]*100;
		print '<li class=\'list-group-item\'><strong>' . $text{'body_virt'} . '</strong><p class=\'pull-right\'>' . int($used) . '%</p></li>';
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
	print '<li class=\'list-group-item\'><strong>' . $text{'body_disk'} . '</strong><p class=\'pull-right\'>' . int($used) . '%</p></li>';
	print '<li class=\'list-group-item\'>';
	print '<div class=\'progress progress-striped active\'>';
	print '<div class=\'progress-bar\' role=\'progressbar\' aria-valuenow=\'' . $used . '\' aria-valuemin=\'0\' aria-valuemax=\'100\' style=\'width: ' . $used . '%\'>';
	print '</div>';
	print '</div>';
	print '</li>';
}