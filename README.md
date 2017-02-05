# plhuexpy
A python server to control Hue lights with Plex webhooks. Rules are set with a yaml file.

# Requirements
* cherrypy
* pyyaml
* phue


# Example Rule Set
```yaml
- rule:
    - plex_condition:
        events: [media.resume]
        players:
            local: [true]
            title: [Plex Web (Chrome)]
    - hue_action:
        items: [Bedroom]
        settings:
            turn_on: true
            brightness: 25
            color_cie: [0.7,0.3]
- rule:
    - plex_condition:
        events: [media.pause]
        players:
            local: [true]
            title: [Plex Web (Chrome)]
    - hue_action:
        items: [Bedroom]
        settings:
            turn_on: true
            brightness: 25
            color_hsv: [0.666,1,1]
- rule:
    - plex_condition:
        events: [media.play]
        players:
            local: [true]
            title: [Plex Web (Chrome)]
    - hue_save_action:
        name: before_play
        items: [Bedroom]
    - hue_action:
        items: [Bedroom]
        settings:
            brightness: 25
- rule:
    - plex_condition:
        events: [media.stop]
        players:
            local: [true]
            title: [Plex Web (Chrome)]
    - hue_load_action: 
        name: before_play
        transition_time: 30
```

# Example Usage
`python plhuexpy.py --bridge-ip <ip_address_of_bridge> --rules path/to/rule/file`

# Wishlist / ToDo
* add scene handling in hue action
* web interface to setup rules
    * Start easy and maybe just have a web interface to edit yaml
* add support for other color spaces
* daemonize
* add server port to CL args
* named action/conditions. can be used multiple times in rules
* implement logging instead of this print crap
* web interface for RGB/CIE/HSV colorpicker
* flesh out the PlexCondition to take more options. Ideally, it would just
    match anything that is in the plex json data and the rule yaml without 
    much special handling

# More details
## Rules
The rule base is read from a yaml document. Rules are made up of any number 
of conditions and any number of actions. The
conditions must ALL test true in order for the actions to execute.

## Conditions
Within a single condition, the options are basically or'd. For example, if
a condition has `event: [media.play,media.resume]` and the event is media.play 
OR media.resume, the condition will pass (test true).

### Plex Condition
Tests agains the data that Plex posts via json.
```yaml
- plex_condition
    events: [] # items in list are or'd, must be a list
    players:
        local: [] 
        title: []
```
## Actions

### Hue Action
Basic action to do most things with a hue light.
```yaml
- hue_action
    items: [] #can be room, group or light name
    settings:    
        turn_on: <true or false>  
        color_rgb: [r,g,b] 
        color_hsv: [h,s,v] 
        color_cie: [x,y]
        color_temp: 153 (6500K) to 500 (2000K)
        brightness: 0 - 1
```
Notes: 
* color_* options are mutually exclusive, only one may be used.
* for rgb,hsv,cie colors, range is 0-1

### Hue Save Action
Saves the states of lights to be loader later:
```yaml
- hue_save_action:
    name: <name to save state to>
    items: ['A list', 'of lights or', 'groups to save']
```

### Hue Load Action
Loads light states from a previously saved state
```yaml
- hue_load_action:
    name: <name of state to load>
    transition_time: <integer of deciseconds>
```
