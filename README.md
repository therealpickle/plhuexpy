# plhuexpy
A python server to control Hue lights with Plex webhooks.

# Requirements
cherrypy
pyyaml
phue
colormath


# Starting Goals

* Use Plex events to dim, turn on/off, set color of lights
* Configurable and persistent rule set

# Stretch Goals
* Web interface to setup rules
* 

# Rule inputs
Start off with just handling the basic events:
* media.play
* media.pause
* media.resume
* media.stop
* media.scrobble
* media.rate

With these rule outputs for each light:
* Scene activation

# other thoughts
* need to handle the initial connection and token with hue
* 


('127.0.0.1', 42937)
POST
/

header:

User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36
Host: localhost:38148
Accept: */*
Accept-Encoding: gzip
Content-Length: 6984
Content-Type: multipart/form-data; boundary=----------------------------d046b704a3fd

