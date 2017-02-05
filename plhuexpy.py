#!/usr/bin/python
import cherrypy
import phue
import yaml
import time
import json

from rules import PlexCondition, HueAction

cherrypy.config.update({'server.socket_port': 38148,
                        'tools.encode.encoding': "utf-8",
                        'tools.json_in.on': True,
                        'tools.json_in.force': False,
                       })

class PlexHandler(object):
    @cherrypy.expose
    def index(self, *args, **kwargs):
        plex_state = json.loads(kwargs['payload'])
        if 'thumb' in kwargs.keys():
            plex_thumb = kwargs['thumb']
        else:
            plex_thumb = None
        
        hue_state = bridge.get_api()

        # print hue_state
        # print plex_state
        
        req = '''
        events: [media.play,media.resume]
        players: 
            local: [true]
            title: [Plex Web (Chrome)]
        '''
        
        # condition test
        cond = PlexCondition(yaml.load(req))
        res = cond.test(plex_state)
        # print res
        



        # action test
        task_on = '''
        items: ['Bedroom Ceiling Color 1','Bedroom Ceiling Color 2','Family Room']
        settings:
            brightness: 150
            transition_time: 20
        '''

        task_off = '''
        items: ['Bedroom Ceiling Color 1','Bedroom Ceiling Color 2','Family Room']
        settings:
            brightness: 25
        '''


        action_on = HueAction(yaml.load(task_on))
        action_off = HueAction(yaml.load(task_off))
        
        if res:
            print "off"
            action_off.execute(bridge)
        else:
            print "on"
            action_on.execute(bridge)

        # lights = bridge.get_light_objects('name')
        # for light in ['Bedroom Ceiling Color 1','Bedroom Ceiling Color 2']:
        #     if light in lights.keys():
        #         lights[light].on = not res
        #         print lights[light]

if __name__ == '__main__':

    bridge = phue.Bridge('10.0.1.128')
    
    connected = False
    while not connected:
        try:
            bridge.connect()
            connected = True
            print "Hue bridge connected."
        except:
            print "Hue bridge connection failed."
            time.sleep(2)

    cherrypy.quickstart(PlexHandler())
