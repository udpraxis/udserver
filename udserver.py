

#!/usr/bin/env python3

#Above code enable the executing command for linux
__author__ = 'udlab'

from twisted.internet.protocol import Factory, Protocol
from twisted.internet import reactor
import serial
import time



#Server Initialization code
debugmode = False
loop = True
device_configured = bool
configure_now = True

#used to choose the port number in configure session
port_string = "testing"



#This function ensure the ease of change the port without entering into the code level. Increase User Friendly
#Function return the value of port destination in string form
def inputConfigure():

        try:
            print("Please chooose one of the Serial port destination type where the Arduino  is connected or please insert custom Serial Port")
            print()
            print("1. /dev/ttyACM'x' ")
            print("2. /dev/cu.usbmodem'x' ")
            print("3. /dev/ttyUSB'x' ")
            print("4. /dev/ttyS'x' ")
            print("5. Custom Serial Port")
            port_input = input()


            if port_input == '1':
                print("What is the Port number?")
                port_input = input()
                port_string = '/dev/ttyACM'+str(port_input)
                return port_string

            elif port_input == '2':
                print("What is the Port number?")
                port_input = input()
                port_string = '/dev/cu.usbmodem'+str(port_input)
                return port_string
            elif port_input == '3':
                print("What is the Port number?")
                port_input = input()
                port_string = '/dev/ttyUSB'+str(port_input)
                return  port_string
            elif port_input == '4':
                print("What is the Port number?")
                port_input = input()
                port_string = '/dev/ttyS'+str(port_input)
                return port_string
            elif port_input == '5':
                print("Please insert your custom Serial Port destination")
                port_input = input()
                port_string = port_input
                return port_string
        except:
            print("There is error in the code section inputConfigure")
            if debugmode:
                    print(port_string)


#The Main Program loop starts here
while loop:
    print("Hello Darwin Welcome back    ")
    print("please initialize certian parameters before running the server")
    print()
    print("Setting the Server in debugmode? yes = y/Y or no  = n/N")
    x = input()
    print()

    if x == 'y' or x == 'Y':
        debugmode = True
        print("Server is running in a debugging mode")
        print(debugmode)
        loop = False
    elif x == 'n' or x == 'N':
        debugmode = False
        print("Server is in none debugging mode ")
        loop = False
    else:
        print("The answer is not acceptable")

time.sleep(1)

print()



while configure_now:
    #Configure server and arduino starts now
    print("Connecting Device in serial port...")

    #The Port is determined here
    arduino_port = inputConfigure()

    try:
        # Initializing the arduino Connection in mac change /dev/cu.usbmodem1441 to apprioprate '/dev/cu.usbmodem1431'
        #device_connected = serial.Serial('/dev/cu.usbmodem1411', 9600, timeout=1) #timeout is important action
        device_connected = serial.Serial(arduino_port, 9600, timeout=1)
        time.sleep(2)
        print("Arduino initialization Complete")
        print("The arduino is connected in port =" + arduino_port)

        device_configured = True
        configure_now = False
        print()
    except:
        print("The Arduino could not be connected!")
        print("1.This could be due to another serialCommunication is busy with Arduino")
        print("2.The Arduino is not connect to the given USB Port")
        print()

        #Configure Arduino later
        print("Do you want to connect the device now?")
        x_1 = input()
        if x_1 == 'y' or x_1 == 'Y':
            print("Connect the Device to the server")

            print("Reconnect by pressing c ")
            connect_now = input()
            if connect_now == 'c' or connect_now == 'C':
                connect_now = True

        if x_1 == 'n' or x_1 == 'N':
            device_configured = False
            configure_now = False


print()









# Server Side
class Server(Protocol):
    def connectionMade(self):
        self.factory.clients.append(self)
        print(" clients are ", self.factory.clients)

    def connectionLost(self, reason):
        self.factory.clients.remove(self)


    #This part deal with information recieved from Client
    def dataReceived(self, data):
       print(data)
       if device_configured :
           device_connected.write(data)
       time.sleep(0.4)


    def message(self, message):
        self.transport.write(message)




class deviceConnected_sent_msg():
    def device_send_msg(self):

        if debugmode:
            print("Iam currently in the waiting for device send msg function")

        devicemsg_byte = device_connected.readline()

        if debugmode:
            print("msg from device is read")
            print("This is the msg:", devicemsg_byte)

        devicemsg_string = str(devicemsg_byte.decode('utf-8'))
        print(devicemsg_string)




factory = Factory()
factory.clients = []
factory.protocol = Server
reactor.listenTCP(8000, factory)
time.sleep(0.5)
print("Darwin :server started")

if debugmode:
    print("Device is connected", device_configured)

reactor.run()
