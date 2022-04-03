from pyfirmata import Arduino, util
import time
import pyfirmata

#Initiate the board
board = Arduino('COM18')

#Loop
#iterator = util.Iterator(board)
#iterator.start()

locked = True 
#true -> knock not entered/wrong knock, false -> correct knock

#pass_knock is a list containing the times between two consecutive knocks in the correct knock sequence.
pass_knock = [0.16655588150024414, 0.13585114479064941, 0.3684210777282715, 0.11480975151062012, 0.1613321304321289, 0.4034092426300049, 0.40139293670654297, 0.38600611686706543]
durations = [] #the set where input durations are stored
recording = False #whether recording a seq: or not
MAX_time = 5 #max time between 2 knocks
MIN_DURATION = 0.05 #minimum duration between 2 knocks
tolerence = 0.2 #time variation to avoid human errors
pre_t = time.time() #current time

pin = board.get_pin("d:4:i")
panick_btn = board.get_pin('d:13:i')
buzz = board.get_pin('d:10:p')
reset_btn = board.get_pin('d:8:i')
thm = board.get_pin('a:0:i')

while True:
    board.iterate()
    if pin.read() is None or panick_btn.read() is None or thm.read() is None:
        continue
    print('Ready')
    break

    #knock
def compare_knocks(pass_knocks,rec_knocks):
    if len(pass_knocks) != len(rec_knocks):
        return False

    for pass_k,rec_k in zip(pass_knocks,rec_knocks):
        diff = abs(pass_k-rec_k)
        if(diff > tolerence):
            return False

    return True

while True:
    board.iterate()
    temp = thm.read()

    if temp > 0.5:
        buzz.write(1.0)



    #panick button
    if panick_btn.read() == True:
        #print('if passed')
        buzz.write(1.0)

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
            #print(durations,len(durations))

            correct = compare_knocks(pass_knock,durations)
            #pass_knock = durations[:]
            if correct:
                print("Right")
            else:
                print("Wrong")
                buzz.write(1.0)
            #print(durations)
            durations.clear()

    if reset_btn.read() == True:
        buzz.write(0.0)

    #time.sleep(0.01)
    #board.iterate()

board.exit()
