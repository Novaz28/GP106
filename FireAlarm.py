from pyfirmata import Arduino,util
import time
import pyfirmata
from math import log

board= Arduino('COM3')

iterator= util.Iterator(board)
iterator.start()
R1 = 10000
c1 = 1.43291542079688e-03
c2 = 2.292319937659526e-04
c3 = -4.58846025754717e-07
c4 = 1.087721342921284e-07

thermistor= board.get_pin('a:0:i')
buzz = board.get_pin('d:10:p')

while True:
    temp_value= thermistor.read()
    if temp_value!=None:
        V=temp_value
        R2 = R1 * (1 / (1-V))
        logR2 = log(R2)
        T = (1.0 / (c1 + c2*logR2 + c3*logR2*logR2*logR2+c4*(logR2)**3))
        Tc = T - 273.15
        print(Tc)
        Tf = (Tc * 9.0)/ 5.0 + 32.0
        time.sleep(0.5)

        if Tc > 57:
            buzz.write(1.0)

        else:
            buzz.write(0.0)

    

    

