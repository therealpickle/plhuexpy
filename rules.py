from conditions import PlexCondition
from actions import HueAction,HueSaveAction,BaseHueAction,HueLoadAction

# keyword_map maps the yaml keyword to the action/condition object
action_map = {
    'hue_action': HueAction,
    "hue_save_action": HueSaveAction,
    "hue_load_action": HueLoadAction,
}

condition_map = {
    'plex_condition': PlexCondition,
}

class Rule(object):
    def __init__(self,element_list):
        self.conditions = []
        self.actions = []


        for element in element_list:
            keyword = element.keys()[0]
            payload = element[keyword]

            if keyword in condition_map.keys():
                self.conditions.append(condition_map[keyword](payload))

            if keyword in action_map.keys():
                self.actions.append(action_map[keyword](payload))
        
        print "New Rule:"
        print "\tConditions:",[c.__class__.__name__ for c in self.conditions]
        print "\tActions:",[a.__class__.__name__ for a in self.actions]
        


    def apply(self,hue_state,plex_state,bridge):
        cond_tests = []
        for cond in self.conditions:
            if isinstance(cond, PlexCondition):
                test = cond.test(plex_state)
            cond_tests.append(test)

        if False not in cond_tests:
            #make sure hue save actions happen first
            for action in self.actions:
                if isinstance(action,HueSaveAction):
                    print "Executing", action.__class__.__name__
                    action.execute(bridge)


            #then do other hue actions
            for action in self.actions:
                if not isinstance(action,HueSaveAction) and \
                        isinstance(action,BaseHueAction):
                    print "Executing", action.__class__.__name__  
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