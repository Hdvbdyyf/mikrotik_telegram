:local token "8091893911:AAF_gOtg_4IDIUPoKt7nIvTlYiJhgBl8JgA";
:local chatid "5821829368";
:local msg "تقرير حالة الأجهزة في الشبكة: شبكة WAN MAX\n\n";

:local online 0;
:local offline 0;

/ip dhcp-server lease
:foreach i in=[find] do={
  :local status [get $i status];
  :local host [get $i host-name];
  :local ip [get $i address];
  :local mac [get $i mac-address];
  :local lastSeen [get $i last-seen];

  :if ($host = "") do={ :set host "غير معروف"; }

  :if ($status = "bound") do={
    :set online ($online + 1);
    :set msg ($msg . "✅ $host ($ip | $mac)\n");
  } else={
    :set offline ($offline + 1);
    :set msg ($msg . "❌ $host ($ip | $mac) - آخر ظهور: $lastSeen\n");
  }
}

/ip hotspot active
:foreach h in=[find] do={
  :local user [get $h user];
  :local ip [get $h address];
  :local mac [get $h mac-address];
  :set msg ($msg . "✅ [Hotspot] $user ($ip | $mac)\n");
}

/ip arp
:foreach a in=[find] do={
  :local ip [get $a address];
  :local mac [get $a mac-address];
  :set msg ($msg . "✅ [ARP] $ip | $mac\n");
}

:set msg ($msg . "\nعدد الأجهزة المتصلة: $online\nعدد الأجهزة المغلقة: $offline");

:local telegram_url ("https://api.telegram.org/bot" /$token . "/sendMessage?chat_id=" . $chatid . "&text=" . $msg);
:log info ("Telegram Message URL: " . $telegram_url);

tool fetch url=$telegram_url keep-result=no;