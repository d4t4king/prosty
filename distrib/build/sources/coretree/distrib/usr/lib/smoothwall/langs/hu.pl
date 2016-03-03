# SmoothWall CGIs
#
# This code is distributed under the terms of the GPL
#
# (c) The SmoothWall Team
#
# (c) Hungarian Translation Team:
# Hamar Kriszti�n
# Kov�cs Csaba

%basetr = (

%basetr,

# common
'save' => 'Ment', # button
'refresh' => 'Frissit', # button
'restore' => 'Visszaallit', # button
'error messages' => 'Hiba�zenetek:',
'back' => 'VISSZA',
'help' => 'S�g�',
'primary dns' => 'Els�dleges DNS:',
'secondary dns' => 'M�sodlagos DNS:',
'invalid primary dns' => '�rv�nytelen els�dleges DNS.',
'invalid secondary dns' => '�rv�nytelen m�sodlagos DNS.',
'dhcp server' => 'DHCP szerver',
'username' => 'Felhasznal�i N�v:',
'password' => 'Jelsz�:',
'enabled' => 'Enged�lyezve:',
'this field may be blank' => 'Ez a mez� �resen maradhat.',
'these fields may be blank' => 'Ezek a mez�k �resen maradhatnak.',

# header.pl
'sshome' => 'home',
'ssstatus' => '�llapot',
'sstraffic graphs' => 'forgalmi grafikonok',
'ssppp settings' => 'ppp be�ll�t�sok',
'ssmodem' => 'modem',
'ssusb adsl firmware upload' => 'usb adsl firmware felt�lt�s',
'ssssh' => 'ssh',
'sspasswords' => 'jelszavak',
'ssweb proxy' => 'web proxy',
'ssdhcp' => 'dhcp',
'ssport forwarding' => 'port �tir�ny�t�s',
'ssexternal service access' => 'external service access',
'ssdmz pinholes' => 'dmz lyukak',
'ssdynamic dns' => 'dinamikus dns',
'ssids' => 'intrusion detection system',
'sscontrol' => 'vez�rl�s',
'ssconnections' => 'kapcsolatok',
'ssother' => 'egy�b',
'ssfirewall' => 't�zfal',
'ssshutdown' => 'le�ll�t�s',
'ssshell' => 'shell',
'ssupdates' => 'friss�t�sek',
'sshelp' => 's�g�',
'sscredits' => 'credits',
'ssip info' => 'IP Inform�ci�',
'powered by' => 'powered by',
'alt home' => 'Home', # alt
'alt information' => 'Inform�ci�', # alt
'alt dialup' => 'Dialup', # alt
'alt remote access' => 'T�voli hozz�f�r�s', # alt
'alt services' => 'Services', # alt
'alt ids' => 'Intrusion Detection System', # alt
'alt vpn' => 'Virtu�lis Mag�n H�lozat (VPN)', # alt
'alt logs' => 'Napl�k', #alt
'alt shutdown' => 'Le�ll�t�s', # alt
'alt shell' => 'Shell', # alt
'alt updates' => 'Friss�t�sek', # alt

# changepw.cgi
'admin user password has been changed' => 'Az admin felhaszn�l� jelszava megv�ltozott.',
'dial user password has been changed' => 'a dial felhaszn�l� jelszava megv�ltozott.',
'password cant be blank' => 'A jelsz� mez� nem lehet �res.',
'passwords do not match' => 'A jelszavak nem egyeznek.',
'change passwords' => 'Jelszavak megv�ltoztat�sa',
'administrator user password' => 'Az admin felhaszn�l� jelszava:',
'dial user password' => 'A dial felhaszn�l� jelszava:',
'again' => 'Ism�t:',
'passwords must be at least 6 characters in length' => 'A jelsz�nak musz�ly 6 karaktern�l hosszabbnak lennie',
'password contains illegal characters' => 'A jelsz� nem megengedett karaktereket tartalmaz',


# credits.cgi
'credits' => 'Credits',
'version' => 'Verzi�: ',
'sponsors' => 'Szponzorok',
'links' => 'Linkek',
'smoothwall homepage' => 'Smoothwall Weboldal',
"translation teams" => 'Ford�t� csoportok',

# dhcp.cgi
'invalid start address' => '�rv�nytelen kezd�c�m.',
'invalid end address' => '�rv�nytelen v�g c�m.',
'cannot specify secondary dns without specifying primary' => 'Nem adhat� meg m�sodlagos DNS addig, am�g elsodleges nincs megadva.',
'invalid default lease time' => '�rv�nytelen Ip b�rleti id�.',
'invalid max lease time' => '�rv�nytelen IP b�rleti id�.',
'dhcp server enabled' => 'DHCP szerver bekapcsolva.  �jraind�t�s.',
'dhcp server disabled' => 'DHCP szerver kikapcsolva.  Le�ll�tva.',
'dhcp configuration' => 'DHCP be�ll�t�s',
'start address' => 'Kezdo c�m:',
'end address' => 'V�g c�m:',
'default lease time' => 'Alap b�rleti id� (perc):',
'max lease time' => 'Max b�rleti id� time (perc):',
'domain name suffix' => 'Domain n�v ut�tag:',

# proxy.cgi
'web proxy configuration' => 'Web proxy be�ll�t�s',
'web proxyc' => 'Web proxy:',
'cache size' => 'Cache m�ret (MB):',
'invalid cache size' => '�rv�nytelen cache m�ret.',
'remote proxy' => 'T�voli proxy:',
'invalid maximum object size' => '�rv�nytelen maxim�lis objektum m�ret.',
'invalid minimum object size' => '�rv�nytelen minim�lis objektum m�ret.',
'invalid maximum outgoing size' => '�rv�nytelen minim�lis kimeno m�ret.',
'invalid maximum incoming size' => '�rv�nytelen maxim�lis bej�vo m�ret.',
'transparent' => 'Transzparens:',
'max size' => 'Max objektum m�ret (KB):',
'min size' => 'Min objektum m�ret (KB):',
'max outgoing size' => 'Max kimen� m�ret (KB):',
'max incoming size' => 'Max bej�v� m�ret (KB):',

# common to logs cgis
'january' => 'Janu�r',
'february' => 'Febru�r',
'march' => 'M�rcius',
'april' => '�prilis',
'may' => 'M�jus',
'june' => 'J�nius',
'july' => 'J�lius',
'august' => 'Augusztus',
'september' => 'Szeptember',
'october' => 'Okt�ber',
'november' => 'November',
'december' => 'December',
'month' => 'H�nap:',
'day' => 'Nap:',
'update' => 'Frissit', # button
'export' => 'Export', # button
'older' => 'R�gebbi',
'newer' => '�jabb',
'settingsc' => 'Be�ll�t�sok:',

# logs.cgi/firewalllog.dat
'firewall log' => 'T�zfal napl�',
'firewall log2' => 'T�zfal napl�:',
'date' => 'D�tum:',
'time' => 'Id�',
'action' => 'Esem�ny',
'chain' => 'L�nc',
'iface' => 'Interface',
'protocol' => 'Protokoll',
'source' => 'Forr�s',
'src port' => 'Forr�s Port',
'destination' => 'C�l',
'dst port' => 'C�l Port',
'unknown' => 'ISMERETLEN',
'lookup' => 'Lookup',

# logs.cgi/log.dat
'log viewer' => 'Napl� olvas�',
'section' => 'Szekci�:',
'kernel' => 'Kernel',
'loginlogout' => 'Login/Logout',
'update transcript' => 'Update transcript',
'log' => 'Napl�:',

# logs.cgi/proxylog.dat
'proxy log viewer' => 'Proxy napl� olvas�',
'bad ignore filter' => 'Rossz mell�z� sz�ro:',
'caps all' => 'MIND',
'ignore filterc' => 'Mell�z� sz�ro:',
'enable ignore filterc' => 'Mell�z� sz�r�k enged�lyezve:',
'source ip' => 'Forr�s IP',
'website' => 'Weboldal',

# logs.cgi/ids.dat
'ids log viewer', 'IDS napl� olvas�',
'datec' => 'D�tum:',
'namec' => 'N�v:',
'priorityc' => 'Priorit�s:',
'typec' => 'T�pus:',
'ipinfoc' => 'IP info:',
'referencesc' => 'Referenci�k:',
'none found' => 'Nincs tal�lat',

# index.cgi
'main page' => 'F� oldal',
'dial' => 'Kapcsolatot kezd', # button
'hangup' => 'Kapcsolatot bont', # button
'current profile' => 'Aktu�lis Profil:',
'connected' => 'Csatlakozva',
'dialing' => 'T�rcs�z�s...',
'modem idle' => 'Modem v�rakozik',
'isdn idle' => 'ISDN v�rakozik',
'profile has errors' => 'A profil hib�s',
'modem settings have errors' => 'A modem be�ll�t�s hib�s',
'user pages' => 'Felhaszn�l�i oldalak',
'mstatus information' => '�llapot&nbsp;inform�ci�k',
'mnetwork traffic graphs' => 'Network&nbsp;traffic&nbsp;graphs',
'administrator pages' => 'Rendszergazdai oldalak',
'mppp setup' => 'PPP&nbsp;be�ll�t�s',
'mmodem configuration' => 'Modem&nbsp;be�ll�t�s',
'mchange passwords' => 'Jelszavak&nbsp;v�ltoztat�sa',
'mremote access' => 'T�voli&nbsp;hozz�f�r�s',
'mdhcp configuration' => 'DHCP&nbsp;be�ll�t�s',
'mproxy configuration' => 'Proxy&nbsp;be�ll�t�s',
'mport forwarding configuration' => 'Port&nbsp;�tir�ny�t�s&nbsp;be�ll�t�s',
'mshutdown control' => 'Le�ll�t�s&nbsp;vez�rl�s',
'mlog viewer' => 'Napl�&nbsp;olvas�',
'mfirewall log viewer' => 'T�zfal&nbsp;napl�&nbsp;olvas�',
'msecure shell' => 'Biztons�gos&nbsp;shell',
'modem dod waiting' => 'Modem 	Dial on Demand v�rakoz�s',
'isdn dod waiting' => 'ISDN Dial on Demand v�rakoz�s',
'pppoe idle' => 'PPPOE �res',
'usbadsl idle' => 'USB ADSL �res',
'pppoe dod waiting' => 'PPPOE Dial on Demand v�rakoz�s',
'there are updates' => 'Friss�t�sek el�rhetoek a rendszerhez. Menj a "Friss�t�sek" men�pont al� t�bb inform�ci��rt.',
'updates is old1' => 'A frissit�s f�jlaid ',
'updates is old2' => 'naposak. Azt javasoljuk friss�tsd fel oket a "Friss�t�s" men�pont al�l.',

# pppsetup.cgi
'profile name not given' => 'Nincs megadva profil n�v.',
'telephone not set' => 'Telefon nincs be�ll�tva.',
'bad characters in the telephone number field' => 'Rossz karakterek a telefonsz�m mezoben.',
'username not set' => 'Nincs felhaszn�l�i n�v.',
'spaces not allowed in the username field' => 'Sz�k�z�k nem megengedettek a felhaszn�l�i n�v mezoben.',
'password not set' => 'Nincs jelsz� be�ll�tva.',
'spaces not allowed in the password field' => 'Sz�k�z�k nem megengedettek a jelsz� mezoben.',
'idle timeout not set' => 'Idle timeout not set.',
'only digits allowed in the idle timeout' => 'Csak sz�mok megengedettek az "�resj�r�s" mezoben.',
'bad characters in script field' => 'Rossz karakterek a script mezoben',
'max retries not set' => 'Maxim�lis pr�b�lkoz�s sz�m nincs be�ll�tva.',
'only digits allowed in max retries field' => 'Csak sz�mok megengedettek a maxim�lis pr�b�lkoz�s mezoben.',
'profile saved' => 'Profil elmentve: ',
'select' => 'Kivalaszt', # button
'profile made current' => 'Profile aktivv� t�ve: ',
'the selected profile is empty' => 'A kiv�lasztott profil �res.',
'delete' => 'T�r�l', # button
'profile deleted' => 'Profil t�r�lve: ',
'empty' => '�RES',
'unnamed' => 'N�vtelen',
'ppp setup' => 'PPP be�ll�t�s',
'profiles' => 'Profilok:',
'profile name' => 'Profil neve:',
'telephony' => 'Telefon:',
'interface' => 'Interface:',
'modem on com1' => 'Modem a COM1-en',
'modem on com2' => 'Modem a COM2-on',
'modem on com3' => 'Modem a COM3-on',
'modem on com4' => 'Modem a COM4-en',
'isdn tty' => 'ISDN a TTY-n',
'isdn1' => 'Egy csatorn�s ISDN (single)',
'isdn2' => 'Dual ISDN',
'computer to modem rate' => ':',
'number' => 'Sz�m:',
'modem speaker on' => 'Modem hangsz�r� be:',
'dialing mode' => 'T�rcs�z�si m�d:',
'tone' => 'Tone',
'pulse' => 'Pulse',
'maximum retries' => 'Maxim�lis pr�b�lkoz�sok:',
'idle timeout' => '�resj�r�si id� (perc; 0 kikapcsol):',
'persistent connection' => 'Folyamatos kapcsolat:',
'authentication' => 'Bel�ptet�s:',
'method' => 'M�d:',
'pap or chap' => 'PAP vagy CHAP',
'standard login script' => 'Standard login script',
'demon login script' => 'Demon login script',
'other login script' => 'Other login script',
'script name' => 'Script neve:',
'type' => 'T�pus:',
'manual' => 'Manu�lis',
'automatic' => 'Automatikus',
'dod' => 'Dial on Demand:',
'dod for dns' => 'Dial on Demand for DNS:',
'connect on smoothwall restart' => 'Kapcsol�d�s a Smoothwall �jraind�t�sa ut�n:',
'pppoe settings' => 'Additional PPPoE settings:',
'usb adsl settings' => 'Additional USB ADSL settings:',
'service name' => 'Service name:',
'concentrator name' => 'Concentrator name:',
'vpi number' => 'VPI Number:',
'vci number' => 'VCI Number:',
'firmwarec' => 'Firmware:',
'firmware present' => 'Tal�lhat�',
'firmware not present' => '<B>Nem</B> tal�lhat�',
'upload usb adsl firmware' => 'Upload USB ADSL firmware',

# remote.cgi
'ssh is enabled' => 'SSH bekapcsolva.  �jraind�t�s.',
'ssh is disabled' => 'SSH kikapcsolva.  Le�ll�t�s.',
'remote access' => 'T�voli hozz�f�r�s',
'remote access2' => 'T�voli hozz�f�r�s:',

# shutdown.cgi
'shutting down smoothwall' => 'Smoothwall le�ll�t�sa',
'shutdown control' => 'Le�ll�t�s vez�rl�s',
'shutdown' => 'Shutdown', # button
'shutdown2' => 'Le�ll�t�s:',
'shutting down' => 'Le�ll�t�s folyamatban',
'smoothwall has now shutdown' => 'A Smoothwall le�llt.',
'rebooting smoothwall' => 'A Smoothwall �jraind�t�sa',
'reboot' => 'Reboot', # button
'rebooting' => '�jraind�t�s',
'smoothwall has now rebooted' => 'A Smoothwall �jraindult.',
# status.cgi
'web server' => 'Web szerver',
'cron server' => 'CRON szerver',
'dns proxy server' => 'DNS proxy szerver',
'logging server' => 'Napl�z� szerver',
'kernel logging server' => 'Kernel napl�z� szerver',
'secure shell server' => 'Secure shell szerver',
'vpn' => 'VPN',
'web proxy' => 'Web proxy',
'intrusion detection system' => 'Intrusion Detection System',
'status information' => '�llapot inform�ci�',
'services' => 'Services:',
'memory' => 'Mem�ria:',
'uptime and users' => 'Uptime �s felhaszn�l�k:',
'interfaces' => 'Csatol�k:',
'disk usage' => 'Lemez haszn�lts�g:',
'loaded modules' => 'Bet�lt�tt modulok:',
'kernel version' => 'Kernel verzi�:',
'stopped' => 'LE�LL�TVA',
'running' => 'FUT',
'swapped' => 'SWAPPED',

# portfw.cgi and dmzhole.cgi and xtaccess.cgi
'source port numbers' => 'A forr�s portnak sz�mnak kell lennie.',
'source is bad' => 'Nem val�s IP c�m vagy h�l�zati n�v.',
'destination ip bad' => '�rv�nytelen c�l IP',
'destination port numbers' => 'A c�l portnak sz�mnak kell lennie.',
'unable to open file' => 'Nem siker�lt megnyitni a file-t',
'source port in use' => 'Forr�s port haszn�latban:',
'forwarding rule added' => '�tir�ny�t� szab�ly hozz�adva; �t�r�ny�t� �jraind�t�sa',
'forwarding rule removed' => '�tir�ny�t� szab�ly elt�vol�tva; �t�r�ny�t� �jraind�t�sa',
'external access rule added' => 'K�ls� hozz�f�r�si szab�ly hozz�adva; hozz�f�r�si vez�rlo �jraind�t�sa',
'external access rule removed' =>' K�ls� hozz�f�r�si szab�ly elt�vol�tva; hozz�f�r�si vez�rl� �jraind�t�sa',
'dmz pinhole rule added' => 'DMZ pinhole rule added; restarting DMZ pinhole',
'dmz pinhole rule removed' => 'DMZ pinhole rule removed; restarting DMZ pinhole',
'port forwarding configuration' => 'Port �t�r�ny�t�s konfigur�l�sa',
'dmz pinhole configuration' => 'DMZ pinhole configuration',
'external access configuration' => 'K�lso hozz�f�r�s konfigur�l�sa',
'add a new rule' => '�j szab�ly hozz�ad�sa:',
'sourcec' => 'Forr�s IP, vagy h�lozat (�res az "MIND"):',
'source ipc' => 'Forr�s IP:',
'source portc' => 'Forr�s port:',
'destination ipc' => 'C�l IP:',
'destination portc' => 'C�l port:',
'current rules' => 'Aktu�lis szab�lyok:',
'source ip' => 'Forr�s IP',
'source port' => 'Forr�s port',
'destination ip' => 'C�l IP',
'destination port' => 'C�l port',
'add' => 'Hozzaad', # button
'remove' => 'Eltavolit', # button
'edit' => 'Szerkeszt', # button
'enabledtitle' => 'Enged�lyezve',
'nothing selected' => 'Semmi nincs kiv�lasztva',
'you can only select one item to edit' => 'Csak egy item-et tudsz kiv�lasztani szerkeszt�sre',
'mark' => 'megjel�l',
'all' => 'MIND',

# ddns.cgi
'dynamic dns' => 'Dinamikus DNS',
'add a host' => 'Host hozz�ad�sa:',
'servicec' => 'Service:',
'behind a proxy' => 'Proxy m�g�tt:',
'enable wildcards' => 'Enable wildcards:',
'hostnamec' => 'Hostn�v:',
'domainc' => 'Domain:',
'current hosts' => 'Aktu�lis hostok:',
'service' => 'Service',
'hostname' => 'Hostn�v',
'domain' => 'Domain',
'proxy' => 'Proxy',
'wildcards' => 'Wildcards',
'hostname not set' => 'Hostn�v nincs be�ll�tva.',
'domain not set' => 'Domain nincs be�ll�tva.',
'invalid hostname' => '�rv�nytelen hostn�v.',
'invalid domain name' => '�rv�nytelen domain n�v.',
'hostname and domain already in use' => 'A hostn�v �s a domain m�r haszn�latban van.',
'ddns hostname added' => 'Dinamikus DNS hostn�v hozz�adva',
'ddns hostname removed' => 'Dinamikus DNS hostn�v elt�vol�tva',
'force update' => 'Force update',

# ipinfo.cgi
'ip info' => 'IP Inform�ci�',
'lookup failed' => 'Visszakeres�s sikertelen',

# shell.cgi
'secure shellc' => 'Secure shell:',

# modem.cgi
'restore defaults' => 'Alapertelmezesek visszaallitasa', # button
'timeout must be a number' => 'A timeout-nak sz�mnak kell lennie.',
'modem configuration' => 'Modem konfigur�ci�',
'modem configurationc' => 'Modem konfigur�ci�:',
'init string' => 'Inicializ�l�s:',
'hangup string' => 'Hangup:',
'speaker on' => 'Speaker be:',
'speaker off' => 'Speaker ki:',
'tone dial' => 'Tone t�rcs�z�s:',
'pulse dial' => 'Pulse t�rcs�z�s:',
'connect timeout' => 'Kapcsol�d�si id�t�ll�p�s:',
'send cr' => 'ISP CR-t ig�nyel:',

# vpnmain.cgi
'restart' => '�jraind�t',
'stop' => 'Le�ll�t',
'vpn configuration main' => 'VPN konfigur�ci� - Fo',
'main' => 'Fo',
'connections' => 'Kapcsolatok',
'global settingsc' => 'Glob�lis be�ll�t�sok:',
'local vpn ip' => 'Helyi VPN IP:',
'if blank the currently configured ethernet red address will be used', 'If blank, the currently configured ethernet RED address will be used.',
'manual control and status' => 'K�zi vez�rl�s �s �llapot:',
'connection name' => 'N�v',
'connection status' => '�llapot',
'capsclosed' => 'LEZ�RT',
'capsdisabled' => 'KIKAPCSOLT',
'capsopen' => 'NYITOTT',

# vpn.cgi/vpnconfig.dat
'name must only contain characters' => 'A n�v csak karaktereket tartalmazhat.',
'left ip is invalid' => 'Left IP is invalid.',
'left next hop ip is invalid' => 'Left next hop is IP invalid.',
'left subnet is invalid' => 'Left subnet is invalid.',
'right ip is invalid' => 'Right IP is invalid.',
'right next hop ip is invalid' => 'Right next hop is IP invalid.',
'right subnet is invalid' => 'Right subnet is invalid.',
'vpn configuration connections' => 'VPN konfigur�ci� - Kapcsolatok',
'add a new connection' => '�j kapcsolat hozz�ad�sa:',
'namec' => 'N�v:',
'leftc' => 'Left:',
'left next hopc' => 'Left next hop:',
'left subnetc' => 'Left subnet:',
'rightc' => 'Right:',
'right next hopc' => 'Right next hop:',
'right subnetc' => 'Right subnet:',
'secretc' => 'Secret:',
'current connections' => 'Aktu�lis kapcsolatok:',
'markc' => 'jel�lt:',
'import and export' => 'Import �s Export:',
'import' => 'Import', # button

# graphs.cgi
'network traffic graphs' => 'H�l�zati forgalom grafikonok',
'network traffic graphsc' => 'H�l�zati forgalom grafikonok:',
'no graphs available' => 'Nincs el�rhet� grafikon.',
'no information available' => 'Nincs el�rhet� inform�ci�.',

# usbadsl.cgi
'usb adsl setup' => 'USB ADSL be�ll�t�s',
'usb adsl help' => 'Az USB ADSL modem haszn�lat�hoz fel kell t�lteni a firmware-ta Smoothwall-ba. T�ltsd le a tar file-t az Alcatel-t�l majjd t�ltsd fel <B>mgmt.o</B> az al�bbiak szerint.',
'upload' => 'Feltolt', # button
'upload successfull' => 'Feltoltes sikeres.',
'could not create file' => 'Nem lehet a file-t l�trehozni.',
'mgmt upload' => 'USB ADSL meghajt� felt�lt�s:',
'upload filec' => 'Felt�ltend� file:',

# updates.cgi
'updates' => 'Friss�t�sek',
'could not open available updates file' => 'Nem tudom megnyitni az el�rheto friss�t�s file-okat.',
'could not download the available updates list' => 'Nem tudom let�lteni az el�rheto friss�t�s list�j�t.',
'could not create directory' => 'Nem tudom l�trehozni a k�nyvt�rat.',
'could not open updatefile for writing' => 'Nem tudom megnyitni a friss�t�s file-okat �r�sra.',
'this is not an authorised update' => 'This is not an authorised update, or your patchlist is out of date.',
'this is not a valid archive' => 'Ez nem megfelelo arch�vum.',
'could not open update information file' => 'Nem tudom megnyitni a friss�t�sek inform�ci�s file-at.  A friss�t�s file s�r�lt.',
'this update is already installed' => 'Ez a friss�t�s m�r telep�tve van.',
'package failed to install' => 'Csomag telep�t�s sikertelen.',
'update installed but' => 'Update telep�tve, de de az install�lt csopmag adatb�zis nem friss�thet�',
'refresh update list' => 'Update lista frissitese .', # button
'installed updates' => 'Telep�tett friss�t�sek:',
'id' => 'ID',
'title' => 'C�m',
'description' => 'Le�r�s',
'released' => 'Kiadva',
'installed' => 'Telep�tve',
'could not open installed updates file' => 'Nem lehet megnyitni az install�lt update f�jlokat.',
'available updates' => 'El�rhet� friss�t�sek:',
'there are updates available' => 'Friss�t�sek vannak a rendszeredhez.Er�sen aj�nlott, hogy telep�tsd azokat, amilyen hamar csak lehet.',
'info' => 'Inf�',
'all updates installed' => 'Minden friss�t�s telep�tve',
'install new update' => '�j friss�t�s telep�t�se:',
'to install an update' => 'A friss�t�s telep�t�s�hez t�ltsd fel az al�bbi .tar.gz f�jlt:',
'upload update file' => 'Update felt�lt�s:',
'could not download latest patch list' => 'Nem tudom let�lteni a legfrissebb patch list�t.',
'could not connect to smoothwall org' => 'Nem tudok csatlakozni a smoothwall.org-hoz',
'successfully refreshed updates list' => 'Sikeresen frissitettem az update list�t.',
'the following update was successfully installedc' => 'A k�vetkez� frissit�sek sikeresen feltelepedtek:',

# ids.cgi
'snort is enabled' => 'Snort enged�lyezve',
'snort is disabled' => 'Snort tiltva',
'intrusion detection system2' => 'Intrusion Detection System:',

);
