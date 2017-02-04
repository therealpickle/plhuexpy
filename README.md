# plhuexpy
A python server to control Hue lights with Plex webhooks.

# Requirements
cherrypy
pyyaml
phue


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
