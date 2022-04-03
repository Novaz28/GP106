'''
Contains utility functions and classes to handle events
'''

import time
from typing import Callable, List,Dict

class TimedEvent:
    '''
    performs a certain function every t seconds
    '''
    def __init__(self,current_time:float,interval:float,function:Callable[[],None]):
        """
        Args:

            current_time (float)    : The time of instantiation 
            function ()->None       : Function to be called after time elapsed

        """
        self.function:Callable[[],None] = function
        self.delay:float = interval
        self.previous_time:float = current_time
    def run(self,current_time:float)->None:
        '''
        runs the function if the set time has elapsed
        '''
        #print(current_time,self.previous_time,self.delay)
        if(current_time - self.previous_time > self.delay):
            self.function()
            self.previous_time = current_time
    def reset(self,current_time:float):
        """
        reset the time
        """
        self.previous_time = current_time



class TimedEventManager:
    '''
    Manages a lot of TimedEvent
    '''
    def __init__(self,timer:Callable[[],float]=time.time):
        '''
        Args:

            timer: ()->float: a function that proveides the current time when called,
                              default is time.time
        
        '''
        self.timed_events:List[TimedEvent] = []
        self.timer:Callable[[],float] = timer
    
    def add_event(self,delay:float,function:Callable[[],None]):
        """
        Add an event to be run on an interval specified

        Args:

            delay (float)       : delay between function calls

            function ()->None   : Function to be called on intervals
        """
        self.timed_events.append(
            TimedEvent(self.timer(),delay,function)
        )

    def reset_all(self):
        '''
        Reset all timed events
        '''
        for te in self.timed_events:
            te.reset(self.timer())

    def run(self):
        """
        This function must be called in a loop for the events to function correctly
        """
        for te in self.timed_events:
            te.run(self.timer())


class Event_Manager:
    '''
    This class is used to manage different events
    For an event driven style programming
    '''
    def __init__(self):
        self.events : Dict[str,List[Callable[[],None]]] = dict()

    def on_event(self,event_name:str,function: Callable[[],None]):
        '''
        Event and the function to be called on the event is added hear

        Args:

            event_name(str)     : event name to identify the event

            function ()->None   : function to be called when the event_name occurs

        '''
        if(event_name not in self.events):
            self.events[event_name] = []
        self.events[event_name].append(function)
    def publish_event(self,event_name:str):
        '''
        Create and event of the name event_name, all functions under event_name will be called
        '''
        if(event_name in self.events):
            for func in self.events[event_name]:
                func()
                

