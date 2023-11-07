# Anteckningar genomgång CERT-SE CTF2023

Mina anteckningar gjorda medan jag löste CERT-SE CTF2023. Information om CTF:en finns på sidan [CERT-SE CTF2023](https://www.cert.se/2023/09/cert-se-ctf2023).

Ladda ner ZIP-filen [här](https://www.cert.se/CERT-SE_CTF2023.zip). Har även sparat en lokal kopia i detta GitHub-repo vilket jag hoppas är okej för CERT-SE.

Börja med att verifiera ZIP-filen. Kör **grep** på SHA256-summan för snabb och enkel verifiering.

```bash
$ sha256sum CERT-SE_CTF2023.zip | grep 6823958ff25220d4a8dbdba52ef53f6f0359c28ef7094ea860ec317c1235c19f
6823958ff25220d4a8dbdba52ef53f6f0359c28ef7094ea860ec317c1235c19f  CERT-SE_CTF2023.zip
```

Instruktionerna från [CERT-SE CTF2023](https://www.cert.se/2023/09/cert-se-ctf2023) är:

```text
<scenario>
CERT-SE har kommit över filer från en okänd fiktiv gruppering försvarare av ett nätverk. I dessa filer finns "flaggor" gömda.
Kan du hitta alla flaggorna?
</scenario>

I .zip-filen under finns en nätverksdump (PCAP) och ett dokument som innehåller totalt sju stycken flaggor, dessa har formatet ”CTF[xxxxxxxxxx]”.
```

Till skillnad mot tidigare år så finns det alltså både en PCAP-fil och en odt-fil. Börja med att packa upp zip-filen:

```bash
$ unzip CERT-SE_CTF2023.zip
Archive:  CERT-SE_CTF2023.zip
   creating: CERT-SE_CTF2023/
  inflating: CERT-SE_CTF2023/CERT-SE_CTF2023 - CompetenceLateRoadThink.odt
  inflating: CERT-SE_CTF2023/CERT-SE_CTF2023.pcap
```

## Flagga 1

Låt oss börja med filen *CERT-SE_CTF2023 - CompetenceLateRoadThink.odt*.

```bash
$ odt2txt CERT-SE_CTF2023\ -\ CompetenceLateRoadThink.odt

I may not have gone where I intended to go, but I think I have
ended up where I needed to be.

[-- Image: Image1 --]

Would it save you a lot of time if I just gave up and went mad
now?

What’s he that wishes so?
My cousin Westmoreland? No, my fair cousin:
If we are mark’d to die, we are enow
To do our country loss; and if to live,
The fewer men, the greater share of honour.
God’s will! I pray thee, wish not one man more.
By Jove, I am not covetous for gold,
Nor care I who doth feed upon my cost;
It yearns me not if men my garments wear;
Such outward things dwell not in my desires:
But if it be a sin to covet honour,
I am the most offending soul alive.
No, faith, my coz, wish not a man from England:
God’s peace! I would not lose so great an honour
As one man more, methinks, would share from me
For the best hope I have. O, do not wish one more!
Rather proclaim it, Westmoreland, through my host,
That he which hath no stomach to this fight,
Let him depart; his passport shall be made
And crowns for convoy put into his purse:
We would not die in that man’s company
That fears his fellowship to die with us.
This day is called the feast of Crispian:
He that outlives this day, and comes safe home,
Will stand a tip-toe when the day is named,
And rouse him at the name of Crispian.
He that shall live this day, and see old age,
Will yearly on the vigil feast his neighbours,
And say ‘To-morrow is Saint Crispian:’
Then will he strip his sleeve and show his scars.

[-- Image: Image2 --]

Let me put on my slightly larger glasses.

Bow ties are cool.

CTF[☔-ra+💿d=i+⛺t=d]

```

Första observatione är att vi har en CTF-sträng och att det även finns två bilder som vi bör titta närmare på. Vi har följande emojis:

- ☔ - rain?
- 💿 - CD?
- ⛺ - tent?

Om det stämmer så har vi *rain (-ra) cd (d=i) tent (t=d)* vilket då blir *incident* och vi har första flaggan **CTF[incident]**.

Texten kommer från *Henry V, Act V, Scene III [What's he that wishes so?]* och finns [online](https://poets.org/poem/henry-v-act-v-scene-iii-whats-he-wishes-so). 

Meningen "Let me put on my slightly larger glasses" är med i The IT Crowd,  https://www.youtube.com/watch?v=LNKocMiehZA.
Meningen "Bow ties are cool" är troligen en hänvisning till Doctor Who (https://www.youtube.com/watch?v=vPGTizdGwSc och https://knowyourmeme.com/memes/bow-ties-are-cool).

## Flagga 2

Låt oss titta vidare på själva filen genom att se på dess metadata med hjälp av **exiftool**.

```bash
$ exiftool CERT-SE_CTF2023\ -\ CompetenceLateRoadThink.odt | grep -e 'CTF\['
User-defined                    : CTF[WILLIAM]
```

Här fick vi flagga två: **CTF[WILLIAM]**.

## Flagga 3

Packa upp .odt-filen:

```bash
$ mkdir odt
$ cp CERT-SE_CTF2023\ -\ CompetenceLateRoadThink.odt odt
$ cd odt
$ unzip CERT-SE_CTF2023\ -\ CompetenceLateRoadThink.odt
Archive:  CERT-SE_CTF2023 - CompetenceLateRoadThink.odt
 extracting: mimetype
   creating: Configurations2/toolbar/
   creating: Configurations2/floater/
   creating: Configurations2/menubar/
   creating: Configurations2/popupmenu/
   creating: Configurations2/accelerator/
   creating: Configurations2/toolpanel/
   creating: Configurations2/progressbar/
   creating: Configurations2/statusbar/
   creating: Configurations2/images/Bitmaps/
  inflating: manifest.rdf
  inflating: meta.xml
  inflating: settings.xml
 extracting: Thumbnails/thumbnail.png
  inflating: styles.xml
  inflating: content.xml
 extracting: Pictures/100000000000040000000300B296674118E1FCC5.jpg
 extracting: Pictures/1000020100000258000000BCA31AE58ABEF1BC61.png
  inflating: layout-cache
  inflating: META-INF/manifest.xml

```

Vi börjar med bilderna:

```bash
$ cd Pictures
$ stegolsb stegdetect -i 1000020100000258000000BCA31AE58ABEF1BC61.png
$ xdg-open 1000020100000258000000BCA31AE58ABEF1BC61_2LSBs.png
```

Vi har nu flagga tre som är **CTF[SNEAKY]** som fanns i bilden *1000020100000258000000BCA31AE58ABEF1BC61.png* och var dold med stenografi.


## Flagga 4

Vi har en bild kvar att titta på nämnligen *100000000000040000000300B296674118E1FCC5.jpg*. Det är en JPEG och ska därför sluta med **ffd9**. Låt oss se hur det stämmer med filen:

```bash
$ xxd 100000000000040000000300B296674118E1FCC5.jpg | tail -20
0002d5a0: 0a79 ac30 9abf 067a 13c3 7bda 8285 369c  .y.0...z..{...6.
0002d5b0: 50ec 3f12 724d 8db4 ebe3 7beb fbd1 9ddf  P.?.rM....{.....
0002d5c0: 1469 320f 0a2e 8439 ff00 96fb 8ce0 9bfd  .i2....9........
0002d5d0: e4c2 3635 614d 91f4 58b7 dce6 f6d7 1642  ..65aM..X......B
0002d5e0: 9e7b e84e 2308 d9ee 09a4 da28 763f ffd9  .{.N#......(v?..
0002d5f0: 4545 4545 4545 4545 4565 4545 4545 6565  EEEEEEEEEeEEEEee
0002d600: 4545 4545 4545 4545 4565 4565 4565 4545  EEEEEEEEEeEeEeEE
0002d610: 4545 4545 4545 4545 4565 4545 4565 6545  EEEEEEEEEeEEEeeE
0002d620: 4545 4545 4545 4545 4565 4565 6545 6565  EEEEEEEEEeEeeEee
0002d630: 4545 4545 4545 4545 4565 4545 4545 6545  EEEEEEEEEeEEEEeE
0002d640: 4545 4545 4545 4545 4565 6545 6565 4545  EEEEEEEEEeeEeeEE
0002d650: 4545 4545 4545 4545 4565 6565 4565 4565  EEEEEEEEEeeeEeEe
0002d660: 4545 4545 4545 4545 4565 6545 4565 6545  EEEEEEEEEeeEEeeE
0002d670: 4545 4545 4545 4545 4565 6545 4565 6545  EEEEEEEEEeeEEeeE
0002d680: 2045 4545 4545 4545 4545 6545 4545 4565   EEEEEEEEEeEEEEe
0002d690: 6545 4545 4545 4545 4545 6565 4565 4545  eEEEEEEEEEeeEeEE
0002d6a0: 6545 4545 4545 4545 4545 6565 6545 6545  eEEEEEEEEEeeeEeE
0002d6b0: 4545 4545 4545 4545 4545 6565 6565 4545  EEEEEEEEEEeeeeEE
0002d6c0: 6545 4545 4545 4545 4545 6545 6565 6545  eEEEEEEEEEeEeeeE
0002d6d0: 65                                       e
```

Vi har extra data efter **ffd9**. Använd dd för att spara den delen av filen.

```bash
$ dd if=100000000000040000000300B296674118E1FCC5.jpg bs=1 skip=$((0x2d5f0)) 2> /dev/null
EEEEEEEEEeEEEEeeEEEEEEEEEeEeEeEEEEEEEEEEEeEEEeeEEEEEEEEEEeEeeEeeEEEEEEEEEeEEEEeEEEEEEEEEEeeEeeEEEEEEEEEEEeeeEeEeEEEEEEEEEeeEEeeEEEEEEEEEEeeEEeeE EEEEEEEEEeEEEEeeEEEEEEEEEeeEeEEeEEEEEEEEEeeeEeEEEEEEEEEEEeeeeEEeEEEEEEEEEeEeeeEe
```

Här kan vi ta hjälp av funktionen magic i CyberChef och vi får den fjärde flaggan **CTF[Bluff City]**.

https://gchq.github.io/CyberChef/#recipe=Magic(3,true,true,'CTF%5C%5C%5B')&input=RUVFRUVFRUVFZUVFRUVlZUVFRUVFRUVFRWVFZUVlRUVFRUVFRUVFRUVlRUVFZWVFRUVFRUVFRUVFZUVlZUVlZUVFRUVFRUVFRWVFRUVFZUVFRUVFRUVFRUVlZUVlZUVFRUVFRUVFRUVFZWVlRWVFZUVFRUVFRUVFRWVlRUVlZUVFRUVFRUVFRUVlZUVFZWVFIEVFRUVFRUVFRWVFRUVFZWVFRUVFRUVFRUVlZUVlRUVlRUVFRUVFRUVFZWVlRWVFRUVFRUVFRUVFRWVlZWVFRWVFRUVFRUVFRUVlRWVlZUVl

## Flagga 5

Fortsätt med *CERT-SE_CTF2023.pcap* och låt oss först se om det finns någon enkel flagga i klartext.

```bash
$ grep -o -E -a  "CTF\[.*\]" CERT-SE_CTF2023.pcap | sort | uniq
CTF[HUNTER2]
```

Vi hittar flaggan **CTF[HUNTER2]** som är ett filnamn som visas vid kataloglistning i FTP-trafik mellan *192.168.0.20:44337* och *10.0.2.50:47744*.

Det gav oss flagga fem: **CTF[HUNTER2]**.

## Flagga 6

Läs in filen i Malcolm. Ser snabbt att det liksom i tidigare CTF:er från CERT-SE finns IRC-trafik. Läs ut den trafiken med **tshark**:

```bash
$ tshark -r CERT-SE_CTF2023.pcap -n -Y "tcp.port == 6667" -Tfields -e irc.request -e irc.response | grep PRIVMSG | grep -v -E "^PRIVMSG" | sed -E "s/^\t+//" | uniq
:Alice!~user@192.168.0.10 PRIVMSG #ops :is this really safe, I mean it's not encrypted right?
:Bob!~user@192.168.0.20 PRIVMSG #ops :we should be safe, it's only internal traffic on the hypervisor
:Bob!~user@192.168.0.20 PRIVMSG #ops :and the secret management system is encrypted with TLS
:Alice!~user@192.168.0.10 PRIVMSG #ops :should we proceed then?
:Bob!~user@192.168.0.20 PRIVMSG #ops :yes, you have to unlock the vault with the secret stored on the secret-management server
:Alice!~user@192.168.0.10 PRIVMSG #ops :yes I know I know. Just give me a sec
:Bob!~user@192.168.0.20 PRIVMSG #ops :ok
:Alice!~user@192.168.0.10 PRIVMSG #ops :so, I have unlocked the vault, you can do your thing now
:Bob!~user@192.168.0.20 PRIVMSG #ops :thanks
:Bob!~user@192.168.0.20 PRIVMSG #ops :thanks,:irc.example.net PONG irc.example.net :LAG1692217828410
:Alice!~user@192.168.0.10 PRIVMSG #ops :Hey, by the way you were saying we are listed on some target list for cyber attacks?
:Bob!~user@192.168.0.20 PRIVMSG #ops :yes we should keep our eyes open for anomalies
:Alice!~user@192.168.0.10 PRIVMSG #ops :ok, I will ping Christina, she is really good with the FPC and the analysis backend
:Bob!~user@192.168.0.20 PRIVMSG #ops :yes, that's a really good idea
:Alice!~user@192.168.0.10 PRIVMSG #ops :ping @Christina,:irc.example.net PONG irc.example.net :LAG1692217941117
:Alice!~user@192.168.0.10 PRIVMSG #ops :ping @Christina
:Christina!~user@192.168.0.30 PRIVMSG #ops :Hi Alice, how are you?
:Alice!~user@192.168.0.10 PRIVMSG #ops :just fine, how are you?
:Christina!~user@192.168.0.30 PRIVMSG #ops :o fine, just a lot of work with the new IDS. So many false positives, not really useful right now
:Alice!~user@192.168.0.10 PRIVMSG #ops :I see. Here is something to cheer you up a bit
:Alice!~user@192.168.0.10 PRIVMSG Christina :DCC SEND message.wav 199 0 11888756 47
:Alice!~user@192.168.0.10 PRIVMSG Christina :SHA-256 checksum for message.wav (remote): 4e31cddd5b972ce211770aca79dc2576099ad07c303de805b89604a7bfbc8b4c
:Christina!~user@192.168.0.30 PRIVMSG Alice :DCC SEND message.wav 3232235550 51991 11888756 47
:Christina!~user@192.168.0.30 PRIVMSG #ops :hahaha, that was wonderful. Thank you!
:Alice!~user@192.168.0.10 PRIVMSG #ops :Bob mentioned we are on some list of potential cyber operation targets. Please let us know if you find anything suspicious.
:Christina!~user@192.168.0.30 PRIVMSG #ops :yeah sure will. Do you know what kind of list and who's behind the announcement?
:Alice!~user@192.168.0.10 PRIVMSG #ops :He told me the group announcing the list is known to exfiltrate information
:Christina!~user@192.168.0.30 PRIVMSG #ops :ok, I'll see what I can find
:Christina!~user@192.168.0.30 PRIVMSG #ops :damn, I found some suspicious traffic to a known bad address
:Alice!~user@192.168.0.10 PRIVMSG #ops :Oh no
:Christina!~user@192.168.0.30 PRIVMSG #ops :Looks like they got in to that mail server we told operations to patch weeks ago!!
:Christina!~user@192.168.0.30 PRIVMSG #ops :need to investigate what data they transferred but It looks like it originates from the secret-management server.......
:Alice!~user@192.168.0.10 PRIVMSG #ops :Oh no, Bob and I used the secret earlier today
```

Vi kan misstänka att det finns en koppling till omnämnandet av **secret-management server**. Börjar titta på Alice trafik och hon skickar vid ett tillfälle (Community ID: 1:iN+LmmoqspxAuI0A1XpAUpdFyhk=) en privat nyckel i klartext:

```bash
-----BEGIN PRIVATE KEY-----
MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDU7yGUoAUtql9a
9QRcqcL8WLyyEVHbqL/twiO65RRU7mQW47jlUTyAqMYdsDgllnItuqZ2MGIzNCwL
qfiN9qlCGQ3NPb0wv/SWxMjxlA12F3Pwz9zLAZfWYB587K7q1cIVI4Ztlk3GAW5C
RVjBrNZgt1dGxPH0iGGtoyXtbj3rAuUKim3FMw0U8fx8mRZuR6lqWIT+p2OET01n
w+KuCgXRgaYgm2CZQij9VW2YotAByECN+DI6Rxx6FEZJe9/qGO7gbjxPb3/PNlRb
HqnsF6LcbYweYcluOg2ovfcNMwIY15J6Wi7/0hbUC7zgbsDnzTbJlVDPHI/bWp3a
n42qZV/lAgMBAAECggEABNR7dpouS+PMX8KPi6+Lx/rA+v64FItjy8zxJQqQYcB6
Pj0CTcIAOpXkJTprp59IQz/I31pHxqFlagqmuUenUrkWmPl7IA7hSYXjXfwjAF2r
UwLQChMk7Sdcga5tEFAdeSpyC0HTIqLtK+0pRH67FSdg1YQ0TdJFzvEUtD7212y8
iopbYH8aoJC5ty/lZMp9uqoy959s4SLkubMYL+SA1Au4fIqC6o99LpmBo74YB+vY
6YrCcCT3ymcUsx4p9W17lI6Hh8DI8HToWqFpn6klikvh+tY+aaTFZT/FooqAgKB2
M2npnGqKP2Pi4Tm0jw/jnKtF9qFwxy1THPBJDBGYgQKBgQDtPlzWVx0qaey44GwV
OHodgZE75vIK8vWEqL1Eb9kybi9oqMWZYOPcbqjj/bRQt8C0qg0jnG+dtt73+80E
CJ49O0YRPl5Huy0LdHeMHHiNbLE9D+WrEdqb0e3/2xa71wAztrdHyNfl7Xsuqzxb
AtZFg4qSWTX0pEtLvm6d+OuTZQKBgQDlxMMU1hZheCT5O1Ggukr+7lgwdGN5vFdT
SPdIVAc6eV6iKgMiJb5G6qhOUrjsJmr+9T0LnpcAIGieylO0h7KhkNFNtBB0PMLI
xb56fSF7RypYNAB1sGvWO3eZsNwiW8sWSVmRRRnZURSQI+d0Edy5AmJnOb7QQ2Xk
EU1eBFcSgQKBgGoALTbPoYZr4YsRKvmoTFeWpq+fFpJxz+VAB6DmYKM5vBEFJ5TK
R8Ub5HZJyyEtmPqf6FL6+Jv9M06VwRqGRz2QmFPoC/P827l8hlWh+vMll2NzEOkI
hyaL+80PtO6kt8BjaSy3vk9Ldnh5pfP8JoTUqzuMhKEUL1hec8o9h/RJAoGBAIuv
4rXxLewV4cyPzqF7gIqaFo1mxO9GnIRqsMONKlPXY7wM9Ji2/4YXtTjgu8H93UCh
kXpV8RFHorMe6GKxuNzWsRifZv1zzyvGZHYNSuSqsEitXLYwCm9U+fI6/qn4ynAD
KevSadOfonO7EESVc24az/5XsfTldLWB+1o0I0eBAoGAbkIGr+VAwYOliDl9Ax3X
KxqzanzzsmiqZnQ8XoCaKAEIOQOLxy6hyBX/ddRAMH8e0yaG+bBstSBnq0gX4qwg
JO3pwnvBeTkERQxS/eR0STnObz/B/M8DUEZZUFpK1hYi/SDEWtQ01yr4UMUqh27Q
THToWPWEz246+RekeBUvTEY=
-----END PRIVATE KEY-----
```

Om vi läser IRC-chatten så ska hon logga in på secret server och det ska göras mellan *2023/08/17 10:22:55* och *2023/08/17 10:23:39*. Där finns en session till servern *secret-management* som enligt Arkime (i Malcolm) har ett **cert:self-signed**. Om vi använder nyckel ovan och **tshark** för att se trafiken ser vi följande:

``` bash
$ tshark -r 3@230817-WgU-76gWh5BK_q-IQuh2BXx7.pcap -o 'tls.keys_list:any,443,http,private.key' -Y http
   23   0.025435 192.168.0.10 → 10.0.1.20    HTTP 185 GET /secret.png HTTP/1.1
   28   0.087438    10.0.1.20 → 192.168.0.10 HTTP 302 HTTP/1.1 200 OK  (PNG)
```

Det går att spara ner filen *secret.png* med hjälp av följande kommando:

```bash
$ tshark -r 3@230817-WgU-76gWh5BK_q-IQuh2BXx7.pcap -o 'tls.keys_list:any,443,http,private.key' --export-objects http,. > /dev/null
```

Tittar vi på den bilden kan vi se att flagga sex är: **CTF[GALOIS]**

**Kommentar:** Troligen är Galois en referens till [Évariste Galois](https://en.wikipedia.org/wiki/%C3%89variste_Galois).

## Flagga 7

Börja titta på filen *message.wav* som förs över enligt konversationen i IRC. Det är följande rader som är relevanta:

```bash
:Alice!~user@192.168.0.10 PRIVMSG Christina :DCC SEND message.wav 199 0 11888756 47
:Alice!~user@192.168.0.10 PRIVMSG Christina :SHA-256 checksum for message.wav (remote): 4e31cddd5b972ce211770aca79dc2576099ad07c303de805b89604a7bfbc8b4c
:Christina!~user@192.168.0.30 PRIVMSG Alice :DCC SEND message.wav 3232235550 51991 11888756 47
```

Låt oss extrahera filen och verifiera den med följande kommandon:

```bash
$ tshark -r CERT-SE_CTF2023.pcap -Y "ip.src == 192.168.0.10 && ip.dst == 192.168.0.30 &&  data.len>0" -T fields -e data > data
$ cat data | xxd -r -p > message.wav
$ sha256sum message.wav | grep 4e31cddd5b972ce211770aca79dc2576099ad07c303de805b89604a7bfbc8b4c
4e31cddd5b972ce211770aca79dc2576099ad07c303de805b89604a7bfbc8b4c message.wav
```

Kontrollera metadata:

```bash
$ ffprobe -loglevel quiet -show_entries stream_tags:format_tags -find_stream_info -of json message.wav
{
    "streams": [
        {

        }
    ],
    "format": {
        "tags": {
            "artist": "CTF"
        }
    }
}
```

Eftersom artisten är "CTF" är det sannolikt att vi kan hitta något intressant här. 

Testa om det är stenografi. Testat följande verktyg:

- https://github.com/danielcardeenas/AudioStego
- https://github.com/techchipnet/HiddenWave
- https://github.com/Sanjipan/Steganography

Om vi tittar efter **DTMF-toner** får vi följande:

```bash
$ dtmf2num message.wav

DTMF2NUM 0.1.1
by Luigi Auriemma
e-mail: aluigi@autistici.org
web:    aluigi.org

- open message.wav
  wave size      11888644
  format tag     1
  channels:      2
  samples/sec:   48000
  avg/bytes/sec: 192000
  block align:   4
  bits:          16
  samples:       5944322
  bias adjust:   1821
  volume peaks:  -26581 26582
  normalize:     6185
  resampling to: 8000hz

- MF numbers:    none

- DTMF numbers:  A**A**7*A****A***A*A*A***A*A******A**A*A***A**A*A*AAA7A*****A***A*A*****A*A*AA*****AA*A****A*AA*A**A***AA*A*A*A***A**A*A****AA*****A*A*A**A****A*A**A*A***A*A*A****A*****A*A*A*A****A*A****A*A**A**A******A*A****A**A**
```

För att säkerställa att detta inte är en falsk träff låt oss testa med verktyg till, [https://github.com/ribt/dtmf-decoder](https://github.com/ribt/dtmf-decoder).

```bash
$ ./dtmf.py -r ../../CERT-SE_CTF2023/message.wav 2> /dev/null

```

Vilket kan tyda på att det inte finns DTMF-toner. Det var varningar om en chuck vilket skulle kunna vara relevant.

Testa även multimon-ng:

```bash
$ multimon-ng -q -c -a DTMF -t wav ../Downloads/CERT-SE_CTF2023/message.wav 
```

Så troligen är det felaktig information from dtmf2num.

Titta efter SSTV med hjälp av https://github.com/colaclanth/sstv.git

```bash
$ sstv -d ../Downloads/CERT-SE_CTF2023/message.wav -o result.png                                                                                          
[sstv] Searching for calibration header... 60.9s
[sstv] Couldn't find SSTV header in the given audio file

```

Utöver detta har jag tittat på filen med

- Python librosa

Testade i nästa steg **fldigi** efter PSK31 men där missade jag själv att hitta flaggan då jag inte tänkte på att man kan behöva ändra frekvensen. Fick via detta klipp på [YouTube](https://www.youtube.com/watch?v=oFdY9hnn6KM) tips om det och kunde därefter hitta den sista flaggan **CTF[HAMRADIO]**.

## Flaggorna

De sju flaggorna är:

- **CTF[incident]**
- **CTF[WILLIAM]**
- **CTF[SNEAKY]**
- **CTF[HUNTER2]**
- **CTF[GALOIS]**
- **CTF[Bluff City]**
- **CTF[HAMRADIO]**

