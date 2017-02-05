import yaml



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
        on: <true or false>  
        color: [r,g,b]
        brightness: 0 - 255
    '''


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