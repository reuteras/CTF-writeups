# Notes going through CERT-SE CTF2026

These are my notes solving the CERT-SE CTF2026. Information about the CTF can be found at [CERT-SE CTF2026](https://www.cert.se/2026/10/antar-du-var-utmaning.html).

Instructions are as follows:

```markdown
As in previous years CERT-SE has put together a CTF during the cyber security month [1, 2]. The challenge is open to anyone with an interest in IT security regardless of the level of expertise.

In the .zip file below [3] is a network dump (PCAPNG) that contains a total of six flags. All of these have the format ”ctf[string]” or “CTF[STRING]”. Everything you need in order to find the flags is included in the network dump and can be solved without connection to the internet. You will not find any clues in any online references. However, free external tools can be useful.

When you have found as many flags as you can, please email them to us along with a description of how you solved the various tasks. It does not matter if the flags submitted are upper or lower case. Email cert@cert.se, with “CTF2026” as the subject of the email.

Please note, we will only accept one response per person. Make sure to find as many flags as possible before submitting. The last day to submit your answer is 31 October 2026.

Länkar
[1] https://en.wikipedia.org/wiki/Capture_the_flag_(cybersecurity)
[2] https://cybersecuritymonth.eu/
[3] https://www.cert.se/ctf/CERT-SE_CTF2026.zip
```

## Download and verify

Download the zip and verify the downloaded file:

```bash
$ wcurl https://www.cert.se/ctf/CERT-SE_CTF2026.zip
$ sha256sum CERT-SE_CTF2026.zip | grep cf271adc6abd284eadfa79f00cbfcc1fcad2eaffc8af9e95e371465cf8c8ca78
cf271adc6abd284eadfa79f00cbfcc1fcad2eaffc8af9e95e371465cf8c8ca78  CERT-SE_CTF2026.zip
```

First unzip the zip file.

```bash
$ 7z x CERT-SE_CTF2026.zip
```

The zip file contained one pcap named *CERT-SE_CTF_2026.pcapng*.

## First flag with grep

We can get the first flag by simply using grep:

```bash
$ grep -oaiE 'ctf\[.*\]' CERT-SE_CTF_2026.pcapng
ctf[first_flag]
```

And we have found the first flag: **ctf[first_flag]**

The flag has been appended to the end of the pcap so opening the pcap with `tshark` gives:

```text
...
tshark: The file "CERT-SE_CTF_2026.pcapng" appears to be damaged or corrupt.
(pcapng: total block length 1936877926 is too large (> 134348832))
```

Let us clean the pcap file by removing the length of the flag, 16 bytes. First get the full length of the original pcap:

```bash
$ stat -f%z CERT-SE_CTF_2026.pcapng
45133992
```

Do the calculation with python:

```bash
$ python3 -c "print(hex(45133992-16))"
0x2b0b098
```

Clean the original pcap and save the new as *clean.pcapng*.

```bash
$ head -c $((0x2b0b098)) CERT-SE_CTF_2026.pcapng > clean.pcapng
```

Could of course have been done with `dd` as well.

## The clean pcap

Let's start looking at the pcap:

```bash
$ tshark -r clean.pcapng -q -z io,phs

===================================================================
Protocol Hierarchy Statistics
Filter:

frame                                    frames:19007 bytes:44491574
  eth                                    frames:19007 bytes:44491574
    ip                                   frames:18989 bytes:44490818
      udp                                frames:550 bytes:313466
        dns                              frames:188 bytes:25711
        quic                             frames:358 bytes:287063
          quic                           frames:46 bytes:37797
            quic                         frames:2 bytes:1564
        nbdgm                            frames:2 bytes:512
          smb                            frames:2 bytes:512
            mailslot                     frames:2 bytes:512
              browser                    frames:2 bytes:512
        ntp                              frames:2 bytes:180
      tcp                                frames:18241 bytes:44157392
        tls                              frames:1039 bytes:2515029
          tls                            frames:327 bytes:1942199
        http                             frames:2146 bytes:3287606
          data-text-lines                frames:1069 bytes:3026300
          ocsp                           frames:2 bytes:1327
          media                          frames:1 bytes:8084
          png                            frames:1 bytes:471
      icmp                               frames:198 bytes:19960
    arp                                  frames:18 bytes:756
===================================================================
```

Looking at the pcap the *media* and *png* items in http look interesting. We also have many ICMP packets as well as many cleartext HTTP requests. There is also a possibility that we can find a key for the TLS packets. No IRC chat this year.

The png and media files can be found:

```bash
$ tshark -r clean.pcapng -Y "http.response" -T fields -e http.request.uri -e http.content_type -e http.response.code -E header=y -E separator=, | grep -v text/html
http.request.uri,http.content_type,http.response.code
/,application/ocsp-response,200
/success.txt?ipv4,text/plain,200
/,,204
/Om_oss.odt,application/vnd.oasis.opendocument.text,200
/white_wallpaper.png,image/png,200
```

Without the grep I observed many requests of the type `/<one char>/...`. URL-encode `[` and `]` and grep for it:

```bash
# I have two aliases for urlencode and urldecode that are used in this README:
$ alias | grep ^url
urldecode='python3 -c "import sys, urllib.parse as up; print(up.unquote_plus(sys.argv[1]))"'
urlencode='python3 -c "import sys, urllib.parse as up; print(up.quote_plus(\" \".join(sys.argv[1:])))"'
$ tshark -r clean.pcapng -Y "http.response" -T fields -e http.request.uri -e http.content_type -e http.response.code -E header=y -E separator=, | grep -E "$(urlencode [)|$(urlencode ])"
/%5B/blog.html,text/html;charset=utf-8,403
/%5D/security.html,text/html;charset=utf-8,403
```

Both have status code 403 and that is something to look at later.

## PNG flag

Looking at the pcap we can see that the user has read about whitespace characters. The PNG image has an interesting name *white_wallpaper.png* so let's check if the pixels are all white:

```bash
$ magick white_wallpaper.png -format %k info:
209
```

We have 209 colours in an image that appears to be white and that indicates that we have found something interesting.

Let us continue with `magick`:

```bash
$ magick white_wallpaper.png txt:- | head
# ImageMagick pixel enumeration: 4096,2160,0,255,srgba
0,0: (255,255,255,255)  #FFFFFFFF  white
1,0: (255,255,255,255)  #FFFFFFFF  white
2,0: (255,255,255,255)  #FFFFFFFF  white
3,0: (255,255,255,255)  #FFFFFFFF  white
4,0: (255,255,255,255)  #FFFFFFFF  white
5,0: (255,255,255,255)  #FFFFFFFF  white
6,0: (255,255,255,255)  #FFFFFFFF  white
7,0: (255,255,255,255)  #FFFFFFFF  white
8,0: (255,255,255,255)  #FFFFFFFF  white
```

Remove the clear white lines and look at that result:

```bash
$ magick white_wallpaper.png txt:- | grep -v '#FFFFFFFF' | tail -n +2 | head
12,5: (255,255,254,166)  #FFFFFEA6  srgba(255,255,254,0.65098)
3102,6: (255,255,254,13)  #FFFFFE0D  srgba(255,255,254,0.0509804)
2609,26: (254,255,255,42)  #FEFFFF2A  srgba(254,255,255,0.164706)
3174,41: (254,255,255,96)  #FEFFFF60  srgba(254,255,255,0.376471)
2732,56: (254,255,255,90)  #FEFFFF5A  srgba(254,255,255,0.352941)
1837,68: (254,255,255,179)  #FEFFFFB3  srgba(254,255,255,0.701961)
3590,116: (255,255,254,152)  #FFFFFE98  srgba(255,255,254,0.596078)
1027,121: (255,255,254,107)  #FFFFFE6B  srgba(255,255,254,0.419608)
1486,129: (254,255,255,18)  #FEFFFF12  srgba(254,255,255,0.0705882)
3557,133: (255,255,254,142)  #FFFFFE8E  srgba(255,255,254,0.556863)
```

I assumed that red = 254 should be 1 and blue = 254 should be 0 and that alpha is a position parameter. Let us only keep them and do a numerical sort and look at the first 20 lines.

```bash
$ magick white_wallpaper.png txt:- | grep -v '#FFFFFFFF' | tail -n +2 | sed -E 's/^[0-9]+,[0-9]+: \(([0-9]+),[0-9]+,[0-9]+,([0-9]+)\).*/\2 \1/' | sort -n | head -20
1 255
2 254
3 254
4 255
5 255
6 255
7 254
8 254
9 255
10 254
11 254
12 254
13 255
14 254
15 255
16 255
17 255
18 254
19 254
20 255
```

Use all lines and convert to binary:

```bash
$ magick white_wallpaper.png txt:- | grep -v '#FFFFFFFF' | tail -n +2 | sed -E 's/^[0-9]+,[0-9]+: \(([0-9]+),[0-9]+,[0-9]+,([0-9]+)\).*/\2 \1/' | sort -n | awk '{printf "%d", ($2==254)} END{print ""}' | fold -w8
01100011
01110100
01100110
01011011
01101000
01101001
01100100
01100100
01100101
01101110
01011111
01101001
01101110
01011111
01110000
01101100
01100001
01101001
01101110
01011111
01110011
01101001
01100111
01101000
01110100
01011101
```

CyberChef **Magic** function solves this with the function **From_Binary('Line%20feed',8)** and gives the flag **ctf[hidden_in_plain_sight]** but we can also convert in the shell:

```bash
$ magick white_wallpaper.png txt:- | grep -v '#FFFFFFFF' | tail -n +2 | sed -E 's/^[0-9]+,[0-9]+: \(([0-9]+),[0-9]+,[0-9]+,([0-9]+)\).*/\2 \1/' | sort -n | awk '{printf "%d", ($2==254)} END{print ""}' | fold -w8 | while read b; do printf "\\$(printf %o $((2#$b)))"; done; echo
ctf[hidden_in_plain_sight]
```

And we have the second flag: **ctf[hidden_in_plain_sight]**

## Flag in odt document

Since odt is a zip container we first use `7z x Om_oss.odt` to extract the content. I first looked at the image, *Thumbnails/thumbnail.png*, which was a dead end. Then looked at *content.xml* which had a suspicious ending with different numbers of `<text:tab/>`.

```bash
$ xmllint --xmlout --format content.xml | tail -20
      <text:p text:style-name="P2">
        <text:tab/>
      </text:p>
      <text:p text:style-name="P2">
        <text:tab/>
      </text:p>
      <text:p text:style-name="P2">
        <text:tab/>
      </text:p>
      <text:p text:style-name="P2">
        <text:tab/>
        <text:tab/>
        <text:tab/>
      </text:p>
      <text:p text:style-name="P2">
        <text:tab/>
      </text:p>
    </office:text>
  </office:body>
</office:document-content>
```

I used knowledge from cleaning and creating RSS feeds with XML tools which has forced me to learn more about XPath then what I would have liked.

```bash
$ xmllint --xpath '//*[local-name()="p"][@*[local-name()="style-name"]="P2"]' content.xml | head
<text:p text:style-name="P2">Här hittar du information om hur vi behandlar personuppgifter: <text:a xlink:type="simple" xlink:href="https://fra.se/omfra/informationombehandlingavpersonuppgifter.106.55af049f184e92956c42b4e.html" text:style-name="Internet_20_link" text:visited-style-name="Visited_20_Internet_20_Link">https://fra.se/omfra/informationombehandlingavpersonuppgifter.106.55af049f184e92956c42b4e.html</text:a></text:p>
<text:p text:style-name="P2"/>
<text:p text:style-name="P2"><text:tab/><text:tab/></text:p>
<text:p text:style-name="P2"/>
<text:p text:style-name="P2"/>
<text:p text:style-name="P2"><text:tab/><text:tab/></text:p>
<text:p text:style-name="P2"><text:tab/><text:tab/><text:tab/></text:p>
<text:p text:style-name="P2"><text:tab/></text:p>
<text:p text:style-name="P2"/>
<text:p text:style-name="P2"/>
```

Then after some trial and error over which part should be 0 and 1, the final and correct one is shown below with the same binary conversion used in the image case above (fold works this time without extra newline):

```bash
$ xmllint --xpath '//*[local-name()="p"][@*[local-name()="style-name"]="P2"]' content.xml | tail -n +2 | sed -e 's#<text:tab/>#1#g' | sed -e 's#<[^>]*>##g' | tr '\n' '0' | fold -w8 | while read x; do printf "\\$(printf %o $((2#$x)))"; done; echo
ctf[not_every_whitespace_is_the_same]
```

This gives us the third flag: **ctf[not_every_whitespace_is_the_same]**

## DNS flag

Searching for the string *flag* in the pcap I saw what looked like base64 encoded strings as questions to the domain flag.com. The next flag can be retrieved via:

```bash
$ tshark -r clean.pcapng -n -Y 'dns contains "flag"' -Tfields -e dns.qry.name | head -1 | cut -d. -f1 | base64 -d
ctf[simple_dns_exfil]
```

Fourth flag: **ctf[simple_dns_exfil]**

## ICMP flag

As there were a lot of ICMP packets in the overview I saw that the TTL value changed between 64 and 128. After some failures with converting this to binary representations as in the examples above I saw the timing also alternated between two values. That got me thinking about Morse code.

So extract relevant data with `tshark` and then use `sed` and `tr` to clean up the output:

```bash
$ tshark -r clean.pcapng -n -Y 'icmp.type == 8' -Tfields -e frame.time_delta_displayed -e ip.ttl | sed -E "s/0\.[0-9]+//" | sed -E "s/6\.[0-9]+/,/" | sed -e "s/64/./" | sed -e "s/128/-/" | tr -d '\n\t '
..,-.,-.-,.,--,.--,..---,..-,.---,..-.,--.,..-,...,-,...,....,.-..,.....,.,...-,--.,-..-,..---,--.,-.-,...-,....,..-.,..---
```

Using CyberChef this is *INKEMW2UJFGUSTSHL5EVGX2GKVHF2* and after a first default test with base64 the correct solution was to use base32 giving us the fifth flag: **CTF[TIMING_IS_FUN]**

## URL path for status 403 flag

As shown when we first looked at the cleaned pcap the 403 responses had the `[` and `]` chars in their paths. That was a sign that this might be where a flag might be hiding. If we select those requests with status 403 from the pcap and print the second field separated by */* with `cut` and then use `urldecode` on the result we get:

```bash
$ urldecode $(tshark -r clean.pcapng -n -Y 'http.response.code == 403' -Tfields -e http.request.uri | cut -f2 -d/ | tr -d '\n' )
ctf[inspect_the_codes]
```

That was the last flag: **ctf[inspect_the_codes]**

## List of all flags

- **ctf[first_flag]**
- **ctf[hidden_in_plain_sight]**
- **ctf[not_every_whitespace_is_the_same]**
- **ctf[simple_dns_exfil]**
- **CTF[TIMING_IS_FUN]**
- **ctf[inspect_the_codes]**

As always a big thanks to [CERT-SE](https://www.cert.se) for a good and fun CTF.

