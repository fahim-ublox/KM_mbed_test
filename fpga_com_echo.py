import serial
import random
import string
from threading import Thread
from subprocess import call
import os
from time import *

class MyThread(Thread):
    def __init__(self):
        Thread.__init__(self)
    def run(self):
        call(["C:\\u-blox\\gallery\\ubx\\pts\\win\\2017.09_KM\\bin\\tracecap.bat", "--config", "UFP1_KM", "--axf",
              "CORTEX_M7_APP", "KM_Serial_Fifo\\BUILD\\R5XXX\\ARM\\KM_Serial_Fifo.elf", "--start", "CORTEX_M7_APP", "--address", "10.17.4.114" ,"--timeout","400","--nohwtrace","--notrace"])

#tracecap --config UFP1_KM --axf CORTEX_M7_APP <mbed application> --start CORTEX_M7_APP --address 10.17.4.114

class EchoSerial():

    def __init__(self,port = 'COM7', baud_Rate = 9600):
        self.ser = serial.Serial()
        self.ser.baudrate = baud_Rate
        self.ser.port = port
        self.ser.timeout = 5
        print "Port and baud rate is set"

    def Start_Server(self):
        self.ser.open()
        print "Port opened"
    def create_data(self, size):
        return ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(size)])
        
        
    def Echo(self, size):
        data = self.create_data(size)
        print "\n\nWriting on "+ self.ser.port + ":" + data
        self.ser.write(data)
        rx = self.ser.read(size)
        print "Read from  "+ self.ser.port + ":" + rx

        if rx == data:
            print "\n\nTest step pass on data size : " + str(size) 
        else:
            print "Else test failed due to received data is expected"
            self.ser.close()
            raise Exception

        


if __name__ == '__main__':

    baudrate = 9600
    myThreadOb1 = MyThread()
    myThreadOb1.setName('Tracecap Thread')
    myThreadOb1.start()
    sleep(10)

    
    server = EchoSerial('COM7', baudrate)
    server.Start_Server()
    for i in range (1, baudrate/20):
        server.Echo(i)

    myThreadOb1.join()
