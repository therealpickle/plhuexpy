
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