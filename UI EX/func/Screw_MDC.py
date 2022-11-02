#!/usr/bin/env python
# -*- coding:utf-8 -*-
import serial
import time

class Serial_Set:
    
    def __init__(self, baudrate, port, timeout, stopbits=1):
        self.baudrate = baudrate
        self.port = port
        self.timeout = timeout
        self.stopbits= stopbits
        self.ser = serial.Serial(port=self.port, baudrate=self.baudrate, timeout=self.timeout, stopbits=self.stopbits)

    def Send_Command(self, command, sendhex=True):
        try:
            if sendhex:
                command = command.decode('hex')
                self.ser.flushInput()  # 清除输入缓存区，放弃所有内容
                self.ser.flushOutput()  # 清除输出缓冲区，放弃输出  
                self.ser.writelines(command)
            else:
                self.ser.writelines(command)
        except IOError as e:
            print ("Send command Fail")
        
    def Receive_data(self, readhex=True):
        ret = self.ser.read(66)
        if readhex:            
            receive = ret.encode('hex').upper()
            return receive
        return ret

    def Open_COM_Port(self):
        self.ser.open()

    def Close_COM_Port(self):
        self.ser.close()
        
    def Send_Receive(self, command, timeout=0.5, readhex=True ):
        self.Send_Command(command)
        time.sleep(timeout)
        ret = self.Receive_data(readhex)
        #print(ret)
        return ret

    def Set_Torque(self, torque=3):
        command_dict={'12':'0106000204B02B7E',\
                      '2.1':'0106000200D2A857',\
                      '10.2':'0106000203FC28BB',\
                      '30.6':'010600020BF42EBD',\
                      '3.2':'010600020140286A',\
                      '15':'0106000205DC2AC3',\
                      '8':'0106000203202922',\
                      '9.2':'0106000203982950',\
                      '3.0':'01060002012C2847',\
                      '13.8':'0106000205642AB1',\
                      '32.3':'010600020C9EACA2',\
                      '8.6':'01060002035C28C3',\
                      '2.8':'0106000201182990',\
                      '1.2':'0106000200782828',\
                      '14':'01060002008C29AF'}

        #print(command_dict[int(torque)])
        self.Send_Command(command_dict[torque])
