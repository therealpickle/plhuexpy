# plhuexpy
A python server to control Hue lights with Plex webhooks.

# Requirements
* cherrypy
* pyyaml
* phue


# Example Rule Set
```yaml
- rule:
    - plex_condition:
        events: [media.play,media.resume]
        players:
            local: [true]
            title: [Plex Web (Chrome)]
    - hue_action:
        items: ["Mason's Nightstand"]
        settings:
            turn_on: true
            brightness: 25
            color: [255,0,0]
- rule:
    - plex_condition:
        events: [media.pause,media.stop]
        players:
            local: [true]
            title: [Plex Web (Chrome)]
    - hue_action:
        items: ["Mason's Nightstand"]
        settings:
            turn_on: true
            brightness: 25
            color: [0,0,255]
```

# Example Usage
`python plhuexpy.py --bridge-ip <ip_address_of_bridge> --rules path/to/rule/file`

# Wishlist / ToDo
* add scene handling in hue action
* web interface to setup rules
    * Start easy and maybe just have a web interface to edit yaml
* have a way to save a state before an action, then restore it later
* add support for other color spaces
* daemonize
* add server port to CL args
* named action/conditions. can be used multiple times in rules
* implement logging instead of this print crap
