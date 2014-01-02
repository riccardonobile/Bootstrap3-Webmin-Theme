#!/usr/bin/perl
BEGIN { push(@INC, ".."); };
use WebminCore;
&ReadParse();
&init_config();
&load_theme_library();
if (&get_product_name() eq "usermin") {
	$level = 3;
}
else {
	$level = 0;
}
%text = &load_language($current_theme);
&header($title);
if ($level == 0) {
	print '<div id="wrapper" class="page">' . "\n";
	print '<div class="container">' . "\n";
	print '<div id="system-status" class="panel panel-default">' . "\n";
	print '<div class="panel-heading">' . "\n";
	print '<h3 class="panel-title">' . &text('body_header0') . '</h3>' . "\n";
	print '</div>';
	print '<div class="panel-body">' . "\n";
	print '<table class="table table-hover">' . "\n";
	
	# Ask status module for collected info
	&foreign_require("system-status");
	$info = &system_status::get_collected_info();
	
	# Hostname
	$ip = $info && $info->{'ips'} ? $info->{'ips'}->[0]->[0] :
				&to_ipaddress(get_system_hostname());
	$ip = " ($ip)" if ($ip);
	$host = &get_system_hostname() . $ip;
	print '<tr>' . "\n";
	print '<td><strong>' . &text('body_host') . '</strong></td>' . "\n";
	if (&foreign_available("net")) {
		$host = '<a href="net/list_dns.cgi">' . $host . '</a>';
	}
	print '<td>' . $host . '</td>' . "\n";
	print '</tr>' . "\n";
	
	# Operating system
	print '<tr>' . "\n";
	print '<td><strong>' . &text('body_os') . '</strong></td>' . "\n";
	if ($gconfig{'os_version'} eq '*') {
		print '<td>' . $gconfig{'real_os_type'} . '</td>' . "\n";
	}
	else {
		print '<td>' . $gconfig{'real_os_type'} . ' ' . $gconfig{'real_os_version'} . '</td>' . "\n";
	}
	print '</tr>' . "\n";
	
	# Webmin version
	print '<tr>' . "\n";
	print '<td><strong>' . &text('body_webmin') . '</strong></td>' . "\n";
	print '<td>' . &get_webmin_version() . '</td>' . "\n";
	print '</tr>' . "\n";

	# System time
	$tm = localtime(time());
	print '<tr>' . "\n";
	print '<td><strong>' . &text('body_time') .'</strong></td>' . "\n";
	if (&foreign_available("time")) {
		$tm = '<a href=time/>' . $tm . '</a>';
	}
	print '<td>' . $tm. '</td>' . "\n";
	print '</tr>' . "\n";

	# Kernel and CPU
	if ($info->{'kernel'}) {
		print '<tr>' . "\n";
		print '<td><strong>' . &text('body_kernel') .'</strong></td>' . "\n";
		print '<td>' . &text('body_kernelon', $info->{'kernel'}->{'os'}, $info->{'kernel'}->{'version'}, $info->{'kernel'}->{'arch'}) . '</td>' . "\n";
		print '</tr>' . "\n";
	}

	# CPU type and cores
	if ($info->{'load'}) {
		@c = @{$info->{'load'}};
		if (@c > 3) {
			print '<tr>' . "\n";
			print '<td><strong>' . $text{'body_cpuinfo'} . '</strong></td>' . "\n";
			print '<td>' . &text('body_cputype', @c) . '</td>' . "\n";
			print '</tr>' . "\n";
		}
	}
	
	# Temperatures, if available
	if ($info->{'cputemps'}) {
		print '<tr>' . "\n";
		print '<td><strong>' . $text{'body_cputemps'} . '</strong></td>' . "\n";
		print '<td>' . "\n";
		foreach my $t (@{$info->{'cputemps'}}) {
			print 'Core ' . $t->{'core'} . ': ' . int($t->{'temp'}) . '&#176;C ';
		}
		print '</td>' . "\n";
		print '</tr>' . "\n";
	}
	if ($info->{'drivetemps'}) {
		print '<tr>' . "\n";
		print '<td><strong>' . $text{'body_drivetemps'} . '</strong></td>' . "\n";
		print '<td>' . "\n";
		foreach my $t (@{$info->{'drivetemps'}}) {
			my $short = $t->{'device'};
			$short =~ s/^\/dev\///;
			my $emsg;
			if ($t->{'errors'}) {
				$emsg .= ' (<span class="text-danger">' . &text('body_driveerr', $t->{'errors'}) . "</span>)";
			}
			elsif ($t->{'failed'}) {
				$emsg .= ' (<span class="text-danger">' . &text('body_drivefailed') . '</span>)';
			}
			print $short .  ': ' . int($t->{'temp'}) . '&#176;C ' . $emsg;
		}
		print '</td>' . "\n";
		print '</tr>' . "\n";
	}
	
	# System uptime
	&foreign_require("proc");
	my $uptime;
	my ($d, $h, $m) = &proc::get_system_uptime();
	if ($d) {
		$uptime = &text('body_updays', $d, $h, $m);
	}
	elsif ($m) {
		$uptime = &text('body_uphours', $h, $m);
	}
	elsif ($m) {
		$uptime = &text('body_upmins', $m);
	}
	if ($uptime) {
		print '<tr>' . "\n";
		print '<td><strong>' . $text{'body_uptime'} . '</strong></td>' . "\n";
		if (&foreign_available("init")) {
			$uptime = '<a href=init/>' . $uptime . '</a>';
		}
		print '<td>' . $uptime . '</td>' . "\n";
		print '</tr>' . "\n";
	}

	# Running processes
	if (&foreign_check("proc")) {
		@procs = &proc::list_processes();
		$pr = scalar(@procs);
		print '<tr>' . "\n";
		print '<td><strong>' . $text{'body_procs'} . '</strong></td>' . "\n";
		if (&foreign_available("proc")) {
			$pr = '<a href=proc/>' . $pr . '</a>';
		}
		print '<td>' . $pr . '</td>' . "\n";
		print '</tr>' . "\n";
	}

	# Load averages
	if ($info->{'load'}) {
		@c = @{$info->{'load'}};
		if (@c) {
			print "<tr> <td><b>$text{'body_cpu'}</b></td>\n";
			print "<td>",&text('body_load', @c),"</td> </tr>\n";
			}
		}

	# CPU usage
	if ($info->{'cpu'}) {
		@c = @{$info->{'cpu'}};
		while ($c[0]+$c[1]+$c[2]+$c[3] > 100) {
			$c[2] = $c[2]-1;
		}
		while ($c[0]+$c[1]+$c[2]+$c[3] < 100) {
			$c[2] = $c[2]+1;
		}
		print '<tr>' . "\n";
		print '<td><strong>' . $text{'body_cpuuse'} . '</strong></td>' . "\n";
		print '<td>' . &text('body_cpustats', @c) . '</td>' . "\n";
		print '</tr>' . "\n";
		print '<tr>' . "\n";
		print '<td></td>' . "\n";
		print '<td>' . "\n";
		print '<div class="progress">' . "\n";
		print '<div class="progress-bar progress-bar-warning" style="width: ' . $c[0] . '%">' . "\n";
		print '</div>' . "\n";
		print '<div class="progress-bar progress-bar-info" style="width: ' . $c[1] . '%">' . "\n";
		print '</div>' . "\n";
		print '<div class="progress-bar progress-bar-danger" style="width: ' . $c[3] . '%">' . "\n";
		print '</div>' . "\n";
		print '<div class="progress-bar progress-bar-success" style="width: ' . $c[2] . '%">' . "\n";
		print '</div>' . "\n";
		print '</div>' . "\n";
		print '</td>' . "\n";
		print '</tr>' . "\n";
	}

	# Memory usage
	if ($info->{'mem'}) {
		@m = @{$info->{'mem'}};
		if (@m && $m[0]) {
			print '<tr>' . "\n";
			print '<td><strong>' . $text{'body_real'} . '</strong></td>' . "\n";
			$mem = &text('body_used', &nice_size($m[0]*1024), &nice_size(($m[0]-$m[1])*1024));
			if (&foreign_available("proc")) {
				$mem = '<a href="proc/index_size.cgi">' . $mem . '</a>';
			}
			print '<td>' . $mem . '</td>' . "\n";
			print '</tr>' . "\n";
			print '<tr>' . "\n";
			print '<td></td>' . "\n";
			print '<td>' . "\n";
			print '<div class="progress">' . "\n";
			$used = ($m[0]-$m[1])/$m[0]*100;
			print '<div class="progress-bar progress-bar-info" role="progressbar" aria-valuenow="' . $used . '" aria-valuemin="0" aria-valuemax="100" style="width: ' . $used . '%">' . "\n";
			print '</div>' . "\n";
			print '</div>' . "\n";
			print '</td>' . "\n";
			print '</tr>' . "\n";
		}

		if (@m && $m[2]) {
			print '<tr>' . "\n";
			print '<td><strong>' . $text{'body_virt'} . '</strong></td>' . "\n";
			print '<td>' . &text('body_used', &nice_size($m[2]*1024), &nice_size(($m[2]-$m[3])*1024)), '</td>' . "\n";
			print '</tr>' . "\n";
			print '<tr>' . "\n";
			print '<td></td>' . "\n";
			print '<td>' . "\n";
			print '<div class="progress">' . "\n";
			$used = ($m[2]-$m[3])/$m[2]*100;
			print '<div class="progress-bar progress-bar-info" role="progressbar" aria-valuenow="' . $used . '" aria-valuemin="0" aria-valuemax="100" style="width: ' . $used . '%">' . "\n";
			print '</div>' . "\n";
			print '</div>' . "\n";
			print '</td>' . "\n";
			print '</tr>' . "\n";
		}
	}

	# Disk space on local drives
	if ($info->{'disk_total'}) {
		($total, $free) = ($info->{'disk_total'}, $info->{'disk_free'});
		print '<tr>' . "\n";
		print '<td><strong>' . $text{'body_disk'} . '</strong></td>' . "\n";
		$disk = &text('body_used', &nice_size($total), &nice_size($total-$free));
		if (&foreign_available("mount")) {
			$disk = '<a href=mount/>' . $disk . '</a>';
		}
		print '<td>' , $disk , '</td>' . "\n";
		print '</tr>' . "\n";
		print '<tr>' . "\n";
		print '<td></td>' . "\n";
		print '<td>' . "\n";
		print '<div class="progress">' . "\n";
		$used = ($total-$free)/$total*100;
		print '<div class="progress-bar progress-bar-info" role="progressbar" aria-valuenow="' . $used . '" aria-valuemin="0" aria-valuemax="100" style="width: ' . $used . '%">' . "\n";
		print '</div>' . "\n";
		print '</div>' . "\n";
		print '</td>' . "\n";
		print '</tr>' . "\n";
	}

	# Package updates
	if ($info->{'poss'}) {
		print '<tr>' . "\n";
		print '<td><strong>' . $text{'body_updates'} . '</strong></td>' . "\n";
		@poss = @{$info->{'poss'}};
		@secs = grep { $_->{'security'} } @poss;
		if (@poss && @secs) {
			$msg = &text('body_upsec', scalar(@poss), scalar(@secs));
		}
		elsif (@poss) {
			$msg = &text('body_upneed', scalar(@poss));
		}
		else {
			$msg = $text{'body_upok'};
		}
		if (&foreign_available("package-updates")) {
			$msg = '<a href="package-updates/index.cgi?mode=updates">' . $msg  . '</a>';
		}
		print '<td>' . $msg . '</td>' . "\n";
		print '</tr>' . "\n";
	}
	print '</table>' . "\n";
	print '</div>' . "\n";
	print '</div>' . "\n";
	print '<p id="about">Template developed and written by <a href="https://www.facebook.com/RiccardoNob" target="_blank">Riccardo Nobile</a> & <a href="https://www.facebook.com/simone.cragnolini" target="_blank">Simone Cragnolini</a></p>' . "\n";
	print '<p id="about"><a href="http://winfuture.it/" target="_blank">WinFuture</a></p>' . "\n";
	print '</div>' . "\n";
	print '</div>' . "\n";

	# Check for incorrect OS
	if (&foreign_check("webmin")) {
		&foreign_require("webmin", "webmin-lib.pl");
		&webmin::show_webmin_notifications();
	}
}
elsif ($level == 3) {
	print '<div id="wrapper" class="page">' . "\n";
	print '<div class="container">' . "\n";
	print '<div id="system-status" class="panel panel-default">' . "\n";
	print '<div class="panel-heading">' . "\n";
	print '<h3 class="panel-title">' . &text('body_header1') . '</h3>' . "\n";
	print '</div>';
	print '<div class="panel-body">' . "\n";
	print '<table class="table table-hover">' . "\n";

	# Host and login info
	print '<tr>' . "\n";
	print '<td><strong>' . &text('body_host') . '</strong></td>' . "\n";
	print '<td>' . &get_system_hostname() . '</td>' . "\n";
	print '</tr>' . "\n";
	
	# Operating system
	print '<tr>' . "\n";
	print '<td><strong>' . &text('body_os') . '</strong></td>' . "\n";
	if ($gconfig{'os_version'} eq '*') {
		print '<td>' . $gconfig{'real_os_type'} . '</td>' . "\n";
	}
	else {
		print '<td>' . $gconfig{'real_os_type'} . ' ' . $gconfig{'real_os_version'} . '</td>' . "\n";
	}
	print '</tr>' . "\n";

	# Usermin version
	print '<tr>' . "\n";
	print '<td><strong>' . &text('body_usermin') . '</strong></td>' . "\n";
	print '<td>' . &get_webmin_version() . '</td>' . "\n";
	print '</tr>' . "\n";

	# System time
	$tm = localtime(time());
	print '<tr>' . "\n";
	print '<td><strong>' . &text('body_time') .'</strong></td>' . "\n";
	print '<td>' . $tm. '</td>' . "\n";
	print '</tr>' . "\n";
	

	# Disk quotas
	if (&foreign_installed("quota")) {
		&foreign_require("quota", "quota-lib.pl");
		$n = &quota::user_filesystems($remote_user);
		$usage = 0;
		$quota = 0;
		for($i=0; $i<$n; $i++) {
			if ($quota::filesys{$i,'hblocks'}) {
				$quota += $quota::filesys{$i,'hblocks'};
				$usage += $quota::filesys{$i,'ublocks'};
			}
			elsif ($quota::filesys{$i,'sblocks'}) {
				$quota += $quota::filesys{$i,'sblocks'};
				$usage += $quota::filesys{$i,'ublocks'};
			}
		}
		if ($quota) {
			$bsize = $quota::config{'block_size'};
			print '<tr>' . "\n";
			print '<td><strong>' . $text{'body_uquota'} . '</strong></td>' . "\n";
			print '<td>' . &text('right_out', &nice_size($usage*$bsize), &nice_size($quota*$bsize)), '</td>' . "\n";
			print '</tr>' . "\n";
			print '<tr>' . "\n";
			print '<td></td>' . "\n";
			print '<td>' . "\n";
			print '<div class="progress">' . "\n";
			$used = $usage/$quota*100;
			print '<div class="progress-bar progress-bar-info" role="progressbar" aria-valuenow="' . $used . '" aria-valuemin="0" aria-valuemax="100" style="width: ' . $used . '%">' . "\n";
			print '</div>' . "\n";
			print '</div>' . "\n";
			print '</td>' . "\n";
			print '</tr>' . "\n";
		}
	}
	print '</table>' . "\n";
	print '</div>' . "\n";
	print '</div>' . "\n";
	print '<p id="about">Template developed and written by <a href="https://www.facebook.com/RiccardoNob" target="_blank">Riccardo Nobile</a> & <a href="https://www.facebook.com/simone.cragnolini" target="_blank">Simone Cragnolini</a></p>' . "\n";
	print '<p id="about"><a href="http://winfuture.it/" target="_blank">WinFuture</a></p>' . "\n";
	print '</div>' . "\n";
	print '</div>' . "\n";
}
&footer();