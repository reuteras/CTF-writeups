# Anteckningar genomgång av FRA Julknäck andra advent 2021

Den andra CTF:n finns [här](https://fra.se/nyheter/nyheter/nyhetsarkiv/news/fraknack2tydmorsesignalerna.5.3421f87617d5c90b1821.html). Denna gång är det [morse](https://sv.wikipedia.org/wiki/Morsealfabetet) som ska tolkas. Finns ingen information om det finns fler flaggor och jag har ännu inte haft tid att leta efter andra dolda meddelanden - [steganografi](https://sv.wikipedia.org/wiki/Steganografi)

Har sedan tidigare bestämt mig för att göra så mycket som möjligt av CTF:en från en [Docker](https://www.docker.com/)-container som kör [Kali](https://www.kali.org/) Linux. Börjar med att se till att ha ett alias klart:

    alias kali='docker run -it --rm --name kali kalilinux/kali'

Allra först laddade jag ner filen som är i MP3-format och laddade upp den [online-tjänst](https://morsecode.world/international/decoder/audio-decoder-adaptive.html) och kunde konstatera att det är en jul-hälsning som sänds. Jag är för dålig på morse för att vilja försöka läsa denna challenge genom att lyssna. Datorer är till för att användas :)
Målsättning blev istället att göra en one-liner även om den blev lite väl lång. Här nedan är ett kommando som kör Kali i en container och uppdaterar den och installerar nödvändiga verktyg. Sedan hämtar jag webbsidan ovan och tar ut url:en till MP3-filen. Hämtar den sedan och skickar den vidare till [multimon-ng](https://github.com/EliasOenal/multimon-ng/) som avkodar morse och skriver ut meddelandet. Enkelt och smidigt!

    docker run -it --rm kalilinux/kali bash -c \
        "apt update > /dev/null 2>&1 && \
        apt dist-upgrade -y > /dev/null 2>&1 && \
        apt install -y curl multimon-ng sox libsox-fmt-mp3 > /dev/null 2>&1 ; \
        curl -s https://www.fra.se/nyheter/nyheter/nyhetsarkiv/news/fraknack2tydmorsesignalerna.5.3421f87617d5c90b1821.html | \
        grep mp3 | grep -o -E 'src=\"[^\"]*' | sed -e 's#src=\"#https://www.fra.se/#' | \
        xargs curl -s -o - | multimon-ng -t mp3 -a MORSE_CW /dev/stdin 2>&1 | tail -1"
    GOD JUL ÖNSKAR FRA

Får passa på att önska god jul till [FRA](https://www.fra.se) samtidigt!
