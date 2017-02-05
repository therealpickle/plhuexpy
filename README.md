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

# Still TODO
* add scene handling in hue action
* Web interface to setup rules


