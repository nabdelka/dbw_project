# This Script reads data from wireless serial, and send it to arduino serial.
# Abdelkader, Noor
# Kayal, Ameer

import serial
import time

communication_prefix = 'S' # 'S' OR 'B' OR 'T'

# Serial Defining #
ser = serial.Serial("/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A601EQ99-if00-port0", baudrate = 115200) # Blue Dongle
#ser     = serial.Serial("/dev/serial/by-id/usb-FTDI_FT231X_USB_UART_DN05LPCT-if00-port0", baudrate = 115200) # Red Dongle
arduino = serial.Serial("/dev/serial/by-id/usb-Arduino__www.arduino.cc__0043_55431313737351408062-if00", baudrate = 9600) # Arduino

# Notes:
#  - Servo motor supports 90deg/1.5sec


curr_str = ""
curr_num = 0
curr_angle = 0


arduino.write(str(curr_angle).encode()) # Initial angle
time.sleep(1.5)            

while(1):
    ret=ser.read(1)   # Read one byte
    if(ret == "\n"):
      if(curr_str != ""):
        if( curr_str[0] == communication_prefix ):
          in_str = curr_str[1:]
          if(communication_prefix == 'S'):
            if( in_str[0] == '-' ):
              angle = 180*(-1*float(in_str[1:-1])+7.85398163)/(2*7.85398163)
            else:
              angle = 180*(float(in_str[:-1])+7.85398163)/(2*7.85398163)
          else:
            angle = 180*float(in_str)
          arduino.write(str(int(angle)).encode())
          print(str(int(angle)),str(int(angle)).encode())
          time.sleep(2)            # wait (sleep) 0.1 seconds
      curr_str = ""
    else:
      if(ret != "\r"):
        curr_str = curr_str + ret
      
    






#while(True):
#    #in_str = str(input("Gabi ay zawye?"))
#    res = ser.read(1)
#    print("Got ", res.decode('utf-8'))
#    arduino.write(in_str.encode())


ser.close()             # close port

