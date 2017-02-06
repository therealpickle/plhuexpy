import colorsys
import yaml
import os

class Action(object):
    ''' Base class for all actions. Every action will have a set
    of tasks wich is a dictionary that comes from the yaml
    '''
    def __init__(self, task):
        self.task = task

    def execute(self):
        ''' this will be overridden by subclasses. '''
        pass


class BaseHueAction(Action):
    '''
    Base class for hue actions. common functions, etc...
    '''
    def execute(self, bridge):
        pass
    
    def expand_lights(self, element_name, bridge):
        '''
        expands a list of groups and lights to a list of just lights
        '''
        light_list = []
        if element_name in self.task.keys():
            for item in self.task[element_name]:
                if item in [g.name for g in bridge.groups]:
                    gdict = bridge.get_group(item)
                    for lid in gdict['lights']:
                        light = bridge.get_light(light_id=int(lid))
                        light_list.append(light['name'])
                elif item in [l.name for l in bridge.lights]:
                    light = bridge.get_light(item)
                    light_list.append(light['name'])
        return light_list

class HueSaveAction(BaseHueAction):
    '''
    Saves the states of lights to be loader later:

    - hue_save_action:
        name: <name to save state to>
        items: ['A list', 'of lights or', 'groups to save']
    '''
    def execute(self, bridge):
        light_list = self.expand_lights('items',bridge)
        if len(light_list)>0 and 'name' in self.task.keys():
            name = self.task['name']

            #get the states of all the lights and put into a dict:
            save_list = []
            for light_name in light_list:
                save_list.append(bridge.get_light(light_name))

            fname = name + ".hsa"
            if not os.path.exists(fname):
                with open(fname,'w') as f:
                    f.write(yaml.dump(save_list))
                    print "Saved state to", fname

class HueLoadAction(BaseHueAction):
    '''
    Loads light states from a previously saved state
    - hue_load_action:
        name: <name of state to load>
        transition_time: <integer of deciseconds>
    '''
    def execute(self, bridge):
        print "Execute load"
        if 'name' in self.task.keys():
            name = self.task['name']

            fname = name+".hsa"
            if os.path.exists(fname):
                with open(fname,'r') as f:
                    load_list = yaml.load(f)
                os.remove(fname)

                for load in load_list:
                    lname = load['name']
                    state = load['state']
                    if 'transition_time' in self.task.keys():
                        state['transitiontime'] = self.task['transition_time']
                    bridge.set_light(lname,state)


class HueAction(BaseHueAction):
    '''
    Basic action to do most things with a hue light

    items: [] #can be room, group or light name
    settings:    
        turn_on: <true or false>  
        color_rgb: [r,g,b] 
        color_hsv: [h,s,v] 
        color_cie: [x,y]
        color_temp: 153 (6500K) to 500 (2000K)
        brightness: 0 - 1
    
    Notes: 
        * color_* options are mutually exclusive, only one may be used.
        * for rgb,hsv,cie colors, range is 0-1
    '''

    def execute(self,bridge):
        # first thing to do is get a list of lights that are described
        # by a room, group or lights
        light_list = self.expand_lights('items',bridge)

        if len(light_list) > 0 and 'settings' in self.task.keys():
            for light in light_list:
                command = {}
                if 'turn_on' in self.task['settings']:
                    command['on'] = self.task['settings']['turn_on']
                
                if 'color_rgb' in self.task['settings']:
                    rgb = self.task['settings']['color_rgb']
                    h,s,v = colorsys.rgb_to_hsv(*rgb)
                    command['colormode'] = 'hs'
                    command['hue'] = int(h*65535.0)
                    command['sat'] = int(s*255.0)
                elif 'color_hsv' in self.task['settings']:
                    h,s,v = self.task['settings']['color_hsv']
                    command['colormode'] = 'hs'
                    command['hue'] = int(h*65535.0)
                    command['sat'] = int(s*255.0)
                    command['bri'] = int(v*255.0)
                elif 'color_cie' in self.task['settings']:
                    x,y = self.task['settings']['color_cie']
                    command['colormode'] = 'xy'
                    command['xy'] = [x,y]
                elif 'color_temp' in self.task['settings']:
                    command['colormode'] = 'ct'
                    command['ct'] = self.task['settings']['color_temp']

                if 'brightness' in self.task['settings']:
                    b = self.task['settings']['brightness']
                    command['bri'] = int(b*255.0)
                
                if 'transition_time' in self.task['settings']:
                    command['transitiontime'] = \
                        int(self.task['settings']['transition_time'])

                print "Setting",light,"to",command
                
                bridge.set_light(light,command)

class HueRunSceneAction(BaseHueAction):
    '''
    Actives a scene.
    - hue_activate_scene:
        name: <name of the scene to activate>
        group: <room or qroup the scene is for>
    '''
    def execute(self,bridge):
        if 'name' in self.task.keys() and 'group' in self.task.keys():
            bridge.run_scene(self.task['group'],self.task['name'])



