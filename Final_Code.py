from pyfirmata import Arduino
import time
from Utility.Event import TimedEventManager
from Network.mqtt import MQTT_Handler
import Topics as tp
from math import log
#Initiate the board
board = Arduino('COM18')

#Loop
#iterator = util.Iterator(board)
#iterator.start()

locked = True 
#true -> knock not entered/wrong knock, false -> correct knock

#pass_knock is a list containing the times between two consecutive knocks in the correct knock sequence.

durations = [] #the set where input durations are stored
recording = False #whether recording a seq: or not
MAX_time = 5 #max time between 2 knocks
MIN_DURATION = 0.05 #minimum duration between 2 knocks

pre_t = time.time() #current time

pin = board.get_pin("d:4:i")
panick_btn = board.get_pin('d:13:i')
buzz = board.get_pin('d:10:p')
reset_btn = board.get_pin('d:8:i')
thm = board.get_pin('a:0:i')


MQTT_NAME = "G9_PO"
MQTT_SERVER = "vpn.ce.pdn.ac.lk"
MQTT_PORT = 8883
#Instantiating the mqtt handler
mqtt_handler = MQTT_Handler(MQTT_NAME,MQTT_SERVER,MQTT_PORT)
#Creating timed event managers
#mainly for the purpose of reporting temperature data
timed_event_manager = TimedEventManager()

R1 = 10000
c1 = 1.43291542079688e-03
c2 = 2.292319937659526e-04
c3 = -4.58846025754717e-07
c4 = 1.087721342921284e-07

def convert_voltage_to_temperature(V):
    if V != None:
        R2 = R1 * (1 / (1 - V))
        logR2 = log(R2)
        T = (1.0 / (c1 + c2 * logR2 + c3 * logR2 * logR2 * logR2 + c4 * (logR2) ** 3))
        Tc = T - 273.15
        return Tc
    return 25

def process_acess_code(msg_payload):
    '''
    Processes the access code send in reply to the knock and
    does the appropriate task
    '''
    if(msg_payload == tp.PO.ACESS_GRANTED):
        print("Right")
    else:
        print("Wrong")
        buzz.write(1.0)
    
def on_lockdown(msg_payload):
    '''
    What to do in a lockdwon situation
    '''
    buzz.write(1.0)
    print('Locking down')

publish_temp_func = lambda : mqtt_handler.publish(tp.PO.TEMPERATURE,f"{convert_voltage_to_temperature(thm.read()):.2f}")

timed_event_manager.add_event(1,publish_temp_func) #publish temperature values every second

#When the reply to the knock is sent process it
mqtt_handler.observe_event(tp.PO.KNOCK_ACCESS,process_acess_code)

#When a lockdown event happens react accordingly
mqtt_handler.observe_event(tp.PO.LOCKDOWN,on_lockdown)

while True:
    board.iterate()
    if pin.read() is None or panick_btn.read() is None or thm.read() is None:
        continue
    print('Ready')
    break

    #knock


while True:

    timed_event_manager.run()


    board.iterate()
    temp = thm.read()

    if temp > 0.5:
        buzz.write(1.0)



    #panick button
    if panick_btn.read() == True:
        #print('if passed')
        buzz.write(1.0)
        mqtt_handler.publish(tp.PO.PANIC_BUTTON,tp.PO.PANIC)

    if reset_btn.read() == True:
        #print('reset btn - ' + reset_btn.read())
        buzz.write(0.0)




    pin_status = pin.read()

    if(pin_status):
        if(not recording):
            recording = True
        else:
            duration = (time.time() - pre_t)
            if(duration > MIN_DURATION):
                durations.append(time.time() - pre_t)
        pre_t = time.time()
    else:
        if(time.time()-pre_t > MAX_time and recording):
            recording = False
            mqtt_handler.publish(tp.PO.KNOCK_SEND,str(durations))
            durations.clear()

    if reset_btn.read() == True:
        buzz.write(0.0)

    #time.sleep(0.01)
    #board.iterate()