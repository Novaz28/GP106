'''
wrappers around the paho mqtt library
'''

import paho.mqtt.client as mqtt
from typing import Dict,List,Callable,Optional
import logging

class MQTT_NETWORK_ERROR(Exception):
    """
    Exception to be raised when there is an mqtt error
    """
    pass
class MQTT_Handler(mqtt.Client):
    """
    Wrapper class around the paho-mqtt client class
    """
    def __init__(self,id:str,server:str,port:int,on_failure:Optional[Callable[[],None]] = None,max_reconects:Optional[int] = None):
        """
        Args:

            id (str)            : Name of the client

            server (str)        : borker adress

            port (int)          : port the mqtt broker is running on

            on_failuer ()->None : function to be called when the system fails (optional)

            max_reconnects      : Maximum number of times the server tries to reconnect
                                Before raising an error when a disconnect event happens

        On instantiation a thread is automatically started to handle mqtt events
        """
        super().__init__(id)
        self.my_server = server
        self.my_port = port
        self.on_failure = on_failure
        if(max_reconects is None):
            self.max_count = float('inf') #Reconnect Infintely many times
        else:
            self.max_count = max_reconects
        try:
            super().connect(server,port)
        except Exception:
            if(self.on_failure is None):
                raise MQTT_NETWORK_ERROR(f"There was a server error while connecting to server {server} at port {port}")
            else:
                self.on_failure()
                return
        self.events:Dict[str,List[Callable[[str],None]]] = {}
        self.loop_start()

    def observe_event(self,topic:str,func:Callable[[str],None]):
        """
        This function is used to add events to be called when a certain topic
        is recieved.

        Args:

            topic (str)         :   topic for when a mqtt message under the said topic arrives 
                                    the function will be called

            func  (str)->None   :   A function that takes in the message payload, 
                                    that is called when a message of the given topic arrives
            
            
        Several functions can be added to the same topic
        
        """
        logging.debug(topic)
        if(topic not in self.events):
            self.subscribe(topic)
            self.events[topic] = []
        self.events[topic].append(func)

    def on_connect(self,client,userdata, flags, rc):
        """
        Runs on connect
        """
        logging.info("Connected with result code "+str(rc))

    def on_message(self,client,userdata,msg):
        """
        Custom implementation for on_message for observe event to work
        """
        topic = msg.topic
        message = str(msg.payload.decode("utf-8"))
        logging.debug(topic,message)
        if(topic in self.events):
            for func in self.events[topic]:
                func(message)
    
    def on_disconnect(self, userdata, flags, rc):
        """
        Custom on diconnect function so that it tries to reconnect for max_reconnect amount
        """
        logging.warning("Disconnected with result code "+str(rc))
        logging.warning("trying to reconnect")
        counter = 0
        while (counter < self.max_count):
            try:
                self.connect(self.my_server,self.my_port)
            except Exception:
                logging.warning("Reconnection Failed trying again")

            counter += 1
        if(self.on_failure is None):
            raise MQTT_NETWORK_ERROR(f"There was a server error while connecting to server {self.my_server} at port {self.my_port}")
        self.on_failure()
        self.loop_stop()




    
