#/usr/bin/env python
'open the file and return the content'

import sys
from SerialSetting import SerialSettingClass
from Screw_MDC import  Serial_Set

def scansn():
    com = Serial_Set(baudrate=115200,port="COM5", timeout=0.5)
    cmd = "16540D"
    # print("cmd",cmd)
    while True:
        _SERIAL_ = com.Send_Receive(cmd, 1, readhex=False).strip()
        print("%s" % _SERIAL_)
        # _SERIAL_ = "ZZ99999"
        #print "now scanning time: %d" % i
        if _SERIAL_ != "":
            break
        else:
            continue

    return _SERIAL_
    
if __name__ == '__main__':
    scansn()
