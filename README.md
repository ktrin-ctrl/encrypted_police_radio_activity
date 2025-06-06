# encrypted_police_radio_activity
This project uses a software defined radio dongle to detect when specific talkgroups are in use on a P25 trunking public safety radio. It was written specifically for Indianapolis, Indiana but could be adapted for other radio systems.

This project uses the wonderful SDR Trunk cross-platform java application to 
decode trunked mobile radio protocols using a RTL-SDR USB dongle and then 
launches a small script to record transmission metadata in a SQLite database and announces encrypted broadcasts in a skeet.

(C)opyright Kristina Trinity 2025, released under the GPL3

SDR Trunk is (c)opyright Denny Sheirer, released under GPL  
https://github.com/DSheirer/sdrtrunk