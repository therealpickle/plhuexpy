#!/usr/bin/python
import cherrypy
import phue
import yaml
import time
import json
import os


from rules import RuleSet

cherrypy.config.update({'server.socket_port': 38148,
                        'tools.encode.encoding': "utf-8",
                        'tools.json_in.on': True,
                        'tools.json_in.force': False,
                       })

class PlexHandler(object):
    def __init__(self,rule_file):
        super(PlexHandler,self).__init__()

        if os.path.exists(rule_file):
            with open(rule_file,'r') as f:
                self.rule_set = RuleSet(yaml.load(f))
        else:
            self.rule_set = None
            print "Rule file does not exist."

    @cherrypy.expose
    def index(self, *args, **kwargs):
        plex_state = json.loads(kwargs['payload'])
        if 'thumb' in kwargs.keys():
            plex_thumb = kwargs['thumb']
        else:
            plex_thumb = None

        hue_state = bridge.get_api()

        if self.rule_set is not None:
            self.rule_set.run(hue_state,plex_state,bridge)



if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument('-r','--rules', dest="rules",
        default='plhuexpy_rules.yaml')
    parser.add_argument('-b','--bridge-ip', dest='bridge_ip',
        default = '10.0.1.128')

    args = parser.parse_args()

    bridge = phue.Bridge(args.bridge_ip)
    
    connected = False
    while not connected:
        try:
            bridge.connect()
            connected = True
            print "Hue bridge connected."
        except:
            print "Hue bridge connection failed."
            time.sleep(2)

    cherrypy.quickstart(PlexHandler(args.rules))
