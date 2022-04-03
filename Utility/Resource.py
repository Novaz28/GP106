'''
Classes for handling various resources that is accessed by many parties simultaneously
'''



from typing import Callable,List




class Multi_Or_Switch:
    '''
    This is a switch which can be turned on or off.
    There can be several handlers to the Multi_Switch

    The switch is turned on if one or more handlers request it to be on
    The swithc is off if no handler has requested it to be on (every handler has requested off state)
    (Hence the Or in the name)

    A handler can't turn off the switch if someone else need it to be on

    This is especially usefull in the buzzer for example as it is a shared resource and
    naively turning it on or off might make one process turn off the buzzer that some other process
    has requested to be on.
    '''
    def __init__(self,on_turn_on:Callable[[],None],on_turn_off:Callable[[],None]):
        """
        Args:

            on_turn_on ()->None     : function to be run when the switch is on

            on_turn_off ()->None    : function to be run when the of turned off
        """
        
        self._on_turn_on:Callable[[],None] = on_turn_on
        self._on_turn_off:Callable[[],None] = on_turn_off
        self._handlers:List[Multi_Or_Switch_handle] = []
        self._on_counter = 0

    
    def on(self):
        if(not self._on_counter):
            self._on_turn_on()
        self._on_counter += 1
    def off(self):
        self._on_counter -=1
        if(not self._on_counter):
            self._on_turn_off()
    def master_off(self):
        for handle in self._handlers:
            handle.request_off()
    def get_handle(self)->'Multi_Or_Switch_handle':
        '''
        returns a handle to the switch so multiple components can acess it
        without interference
        '''
        handle = Multi_Or_Switch_handle(self)
        self._handlers.append(handle)
        return handle




class Multi_Or_Switch_handle:
    '''
    Handle for a multi_or_switch
    '''
    def __init__(self,parent:Multi_Or_Switch):
        self._parent:Multi_Or_Switch = parent
        self.on = False
    def request_on(self):
        '''
        Request the parent swithc to turn on
        '''
        if(not self.on):
            self.on = True
            self._parent.on()
    def request_off(self):
        '''
        Request the parent switch to turn off
        The parent switch will only turn off
        if all handles are requesting the off state
        '''
        if(self.on):
            self.on = False
            self._parent.off()
        