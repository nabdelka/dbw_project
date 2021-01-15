# This script Reads & Shows data from Logitech G920 kit

# Noor Abdelkader
# Ameer Kayal

import pygame
import serial
import time
from numpy import *
from pyqtgraph import QtGui, QtCore
import pyqtgraph as pg


# COM3 -> Red Dongle
# COM8 -> Blue Dongle
serial_port = "COM3"
serial_baudrate = 115200
ser = serial.Serial(serial_port, baudrate = serial_baudrate)


def count_joysticks():
    # Added for debug purpose
    # Doc = https://www.pygame.org/docs/ref/joystick.html
    pygame.init()
    pygame.joystick.init()
    joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
    print("Found",len(joysticks),"Joysticks")



def init_pygame():
    # initialize pygame
    pygame.init()
    pygame.joystick.init()
    js = pygame.joystick.Joystick(0)  # initialzie joystick
    js.init()

    jsInit = js.get_init()
    jsId = js.get_id()
    print(js.get_name() + "Joystick ID: %d Init status: %s" % (jsId, jsInit))
    numAxes = js.get_numaxes()

    print("Please press A to start, praess the xBox button to quit")
    # waiting for initial keys
    while (True):
        pygame.event.pump()
        keys = [js.get_button(i) for i in range(js.get_numbuttons())]

        if keys[0] != 0:
            break
        if keys[10] != 0:
            sys.exit();


    ### START QtApp ####
    app = QtGui.QApplication([])  # you MUST do this once (initialize things)
    ####################

    win = pg.GraphicsWindow(title="Realtime Signals from Driving Kit")  # creates a window
    p1 = win.addPlot(title="Steering Wheel Signal [radians]")  # creates empty space for the plot in the window
    curve1 = p1.plot(pen=pg.mkPen('r', width=1))               # create an empty "plot" (a curve to plot)
    p2 = win.addPlot(title="Throttle Signal [Fraction 0-1]")
    curve2 = p2.plot(pen=pg.mkPen('b', width=1))
    p3 = win.addPlot(title="Break Signal [Fraction 0-1]")
    curve3 = p3.plot(pen=pg.mkPen('g', width=1))

    windowWidth = 500                  # width of the window displaying the curve
    Xm1 = linspace(0, 0, windowWidth)  # create array that will contain the relevant time series
    ptr1 = -windowWidth                # set first x position
    Xm2 = linspace(0, 0, windowWidth)
    ptr2 = -windowWidth
    Xm3 = linspace(0, 0, windowWidth)
    ptr3 = -windowWidth


    
    t1 = time.time()
    while (True):

        Xm1[:-1] = Xm1[1:]  # shift data in the temporal mean 1 sample left
        Xm2[:-1] = Xm2[1:]
        Xm3[:-1] = Xm3[1:]


        pygame.event.pump()
        jsInputs = [float(js.get_axis(i)) for i in range(numAxes)]

        steerVal = float(round(round(jsInputs[0], 5) * 7.85398163,5))
        throtVal = float(round(1 - (((jsInputs[2] - (-1)) * (1.0 - 0)) / (1.0 - (-1.0))) + 0, 4))
        breakVal = float(round(1 - (((jsInputs[3] - (-1)) * (1.0 - 0)) / (1.0 - (-1.0))) + 0, 4))

        str_steerVal = 'S' + str(steerVal)
        str_throtVal = 'T'+ str(throtVal)
        str_breakVal = 'B' + str(breakVal)

        packet_steer = str_steerVal + "\r\n"
        packet_throt= str_throtVal + "\r\n"
        packet_break= str_breakVal + "\r\n"
        print(packet_steer,packet_throt,packet_break,"\n")
        
        if ser.isOpen():

            ser.write(str.encode(packet_steer))
            ser.write(str.encode(packet_throt))
            ser.write(str.encode(packet_break))
            #time.sleep(2.1)


        else:
            print ("Serial Communication Failed")
            sys.exit();


        Xm1[-1] = float(steerVal) # vector containing the instantaneous values
        ptr1 += 1                 # update x position for displaying the curve
        curve1.setData(Xm1)       # set the curve with this data
        curve1.setPos(ptr1, 0)    # set x position in the graph to 0

        Xm2[-1] = float(throtVal)
        ptr2 += 1
        curve2.setData(Xm2)
        curve2.setPos(ptr2, 0)

        Xm3[-1] = float(breakVal)
        ptr3 += 1
        curve3.setData(Xm3)
        curve3.setPos(ptr3, 0)

        QtGui.QApplication.processEvents()  # you MUST process the plot now



        keys = [js.get_button(i) for i in range(js.get_numbuttons())]

        if keys[10] != 0:
            print("Ending program")
            win.close()
            break


init_pygame()
