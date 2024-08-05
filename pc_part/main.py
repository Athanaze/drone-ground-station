'''
Serial settings:

Serial line
/dev/ttyACM0

Speed
9600
'''

import serial

PORT = "/dev/ttyACM0"
BAUDRATE = 9600
BYTE_SIZE = 8
TIMEOUT = 2

serialPort = serial.Serial(port = PORT, baudrate=BAUDRATE, bytesize=BYTE_SIZE, timeout=TIMEOUT, stopbits=serial.STOPBITS_ONE)

serialString = ""  


while(1):

    # Wait until there is data waiting in the serial buffer
    if(serialPort.in_waiting > 0):

        # Read data out of the buffer until a carraige return / new line is found
        serialString = serialPort.readline()

        # Print the contents of the serial data
        print("====================")
        print(serialString.decode('Ascii'))
    
    serialPort.write('1'.encode('Ascii'))