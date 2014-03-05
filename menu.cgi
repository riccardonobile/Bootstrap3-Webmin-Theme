#!/usr/bin/perl
BEGIN { push(@INC, ".."); };
use WebminCore;
&ReadParse();
&init_config();
%text = &load_language($current_theme);
%gaccess = &get_module_acl(undef, "");
$charset = &get_charset();
&PrintHeader($charset);

print 'Menu Here';