# -*- coding:utf-8 -*-
import serial
import time
import serial.tools.list_ports
#import libscrc

'''
    open serial port example:
    mser = SerialSettingClass()  # Example 01
    mser = SerialSettingClass(115200)  # Example 02
    mser = SerialSettingClass(115200, "USB\VID_1A86&PID_7523")  # Example 03 # noqa
    mser = SerialSettingClass(115200, "COM3")  # Example 04
'''


class SerialSettingClass:

    def __init__(self, baudrate=115200, port="COM?", timeout=0.7, sendhex=True, readhex=True):
        self.baudrate = baudrate
        self.port = port
        self.timeout = timeout
        self.sendHex = sendhex
        self.readHex = readhex
        self.ser = None

    def connectPort(self):
        if self.port == "COM?":
            actualPort = self.getPort()
            if 1 == len(actualPort):
                self.port = actualPort[0]
            elif self.port in actualPort:
                pass
            else:
                print("port incorrect!! only find: {}".format(actualPort))
                return False
        elif self.port.find('USB') != -1:
            self.port = self.getPortVIDPID(self.port)
            if self.port == None:
                return False

        print("connect port.. using PORT:{} ,Baudrate:{} ,Timeout:{}".format(self.port, self.baudrate, self.timeout))
        try:
            self.ser = serial.Serial(port=self.port, baudrate=self.baudrate, timeout=self.timeout)
        except Exception as e:
            print("connect port fail: {}".format(e))
            return False

        return True

    def closePort(self):
        self.ser.close()

    def Send_Command(self, command):
        try:
            if self.sendHex:
                command = command.decode('hex')
            self.ser.flushInput()
            self.ser.flushOutput()
            self.ser.writelines(command)
        except IOError as e:
            print("Send command Fail: {}".format(e))

    def write(self, data):
        try:
            self.ser.write(data)
        except IOError as e:
            print("write Fail: {}".format(e))

    def Receive_data(self):
        ret = self.ser.read(2048)
        if self.readHex:
            return ret.encode('hex').upper()
        return ret

    def SendAndReceive(self, command, timeout=0.1):
        self.Send_Command(command)
        time.sleep(timeout)
        return self.Receive_data()

    def getPort(self):
        portList = []
        for port in serial.tools.list_ports.comports():
            portList.append(port.device)
        return portList

    def getPortVIDPID(self, usbvidpid=r"USB\VID_0000&PID_FFFF"):
        vidpid = usbvidpid.split('\\')
        if len(vidpid) < 2:
            return None
        usbdatalist = vidpid[1].split('&')
        if len(usbdatalist) < 2:
            return None
        vid = usbdatalist[0][4:]
        pid = usbdatalist[1][4:]
        check_for = "USB VID:PID=%s:%s" % (vid, pid)
        ports = serial.tools.list_ports.comports()
        for check_port in ports:
            if hasattr(serial.tools, 'list_ports_common'):
                if (check_port.vid, check_port.pid) == (int(vid, 16), int(pid, 16)):
                    return check_port.device
                continue
            if check_for in check_port[2].upper() == check_port[1]:
                return check_port[0]
        return None

    def setTorqueForScrew(self, torque):
        torque_str = "01060002"
        torque = float(torque) * 100
        torqueHex = self.__getHex(torque)
        command = self.__getCheckCode(torque_str + torqueHex)
        self.sendHex = True
        self.Send_Command(command.upper())

    def __getHex(self, n):
        n = str(int(n))
        n = hex(int(n, 10))
        n = str(n).replace("x", "")[-4:]
        return n.zfill(4)

    # 校驗碼生成
    # def __getCheckCode(self, n):
    #     n = str(n)
    #     crc16 = libscrc.modbus(n.decode("hex"))
    #     crc16_MSB = self.__getHex(crc16)
    #     crc16_Modbus = crc16_MSB[2:] + crc16_MSB[:2]
    #     return (n + crc16_Modbus).upper()


if __name__ == '__main__':
    s = SerialSettingClass()
    if s.connectPort():
        s.setTorqueForScrew("3.2")
