import yaml

from hue_helper import rgb_to_xy, xy_to_rgb


class Condition(object):
    def __init__(self,req):
        self.req = req

    def test(self,input):
        ''' 
        input is a dict of something made from plex json or 
        hue dict. will return true if this condition is satisfied
        '''
        return False


class PlexCondition(Condition):
    '''
    handles the folowing requirements
    events: [] # items in list are or'd, must be a list
    players:
        local: [] 
        title: []
    '''
    def test(self, plex_state):
        if 'events' in self.req.keys():
            if plex_state['event'] not in self.req['events']:
                return False

        if 'players' in self.req.keys():
            if 'title' in self.req['players'].keys():
                if plex_state['Player']['title'] not in self.req['players']['title']:
                    return False

            if 'local' in self.req['players'].keys():
                if plex_state['Player']['local'] not in self.req['players']['local']:
                    return False
        return True

class Action(object):
    def __init__(self, task):
        self.task = task

    def execute(self):
        return False


class HueAction(Action):
    '''
    items: [] #can be room, group or light name
    settings:    
        turn_on: <true or false>  
        color: [r,g,b]
        brightness: 0 - 255
    '''

    def execute(self,bridge):
        # first thing to do is get a list of lights that are described
        # by a room, group or lights
        light_list = []
        if 'items' in self.task.keys():
            for item in self.task['items']:
                if item in [g.name for g in bridge.groups]:
                    gdict = bridge.get_group(item)
                    for lid in gdict['lights']:
                        light = bridge.get_light(light_id=int(lid))
                        light_list.append(light['name'])
                elif item in [l.name for l in bridge.lights]:
                    light = bridge.get_light(item)
                    light_list.append(light['name'])

        print light_list
        if len(light_list) > 0 and 'settings' in self.task.keys():
            for light in light_list:
                command = {}
                if 'turn_on' in self.task['settings']:
                    command['on'] = self.task['settings']['turn_on']
                if 'color' in self.task['settings']:
                    pass
                if 'brightness' in self.task['settings']:
                    command['bri'] = int(self.task['settings']['brightness'])
                if 'transition_time' in self.task['settings']:
                    command['transitiontime'] = int(self.task['settings']['transition_time'])

                print light, command
                
                bridge.set_light(light,command)

class Rule(object):
    def __init__(self,conditions,actions):
        self.conditions = conditions
        self.actions = actions




if __name__ == '__main__':
    test_req = '''
    plex:
        event: media.pause
    hue:
        lights:
            name: Hearth Color
            state:
                on: true
    '''

    req = yaml.load(test_req)

    if 'plex' in req.keys():
        print req['plex']

        cond = PlexCondition(req['plex'])