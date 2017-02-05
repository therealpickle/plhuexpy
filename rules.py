import colorsys

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

        if len(light_list) > 0 and 'settings' in self.task.keys():
            for light in light_list:
                command = {}
                if 'turn_on' in self.task['settings']:
                    command['on'] = self.task['settings']['turn_on']
                if 'color' in self.task['settings']:
                    color = self.task['settings']['color']
                    rgb = [float(c)/255.0 for c in color]
                    h,s,v = colorsys.rgb_to_hsv(*rgb)

                    command['hue'] = int(h*65535.0)
                    command['sat'] = int(s*255.0)
                    
                if 'brightness' in self.task['settings']:
                    command['bri'] = int(self.task['settings']['brightness'])
                if 'transition_time' in self.task['settings']:
                    command['transitiontime'] = \
                        int(self.task['settings']['transition_time'])

                print "Setting",light,"to",command
                
                bridge.set_light(light,command)

class Rule(object):
    def __init__(self,element_list):
        self.conditions = []
        self.actions = []
        for element in element_list:
            if 'plex_condition' in element.keys():
                cond = PlexCondition(element['plex_condition'])
                self.conditions.append(cond)
            elif 'hue_action' in element.keys():
                act = HueAction(element['hue_action'])
                self.actions.append(act)

    def apply(self,hue_state,plex_state,bridge):
        cond_tests = []
        for cond in self.conditions:
            if isinstance(cond, PlexCondition):
                test = cond.test(plex_state)
            cond_tests.append(test)

        if False not in cond_tests:
            for action in self.actions:
                if isinstance(action,HueAction):
                    action.execute(bridge)


class RuleSet(object):
    """docstring for RuleSet"""
    def __init__(self, rule_list):
        self.rules = []
        for element in rule_list:
            if 'rule' in element.keys():
                self.rules.append(Rule(element['rule']))


    def run(self,hue_state,plex_state,bridge):
        for rule in self.rules:
            rule.apply(hue_state,plex_state,bridge)


if __name__ == '__main__':
    import yaml

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