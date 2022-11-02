#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os
import re
import time
from func.ConnectDB import ConnectDB
from func.SerialSetting import SerialSettingClass
import numpy as np


class Station_class():

    def __init__(self, n, config_data):
        self.res = ""
        self.Item_n = n
        self.RunType = config_data[self.Item_n]['RunType']
        self.Name = config_data[self.Item_n]['Name']
        self.ErrorCode = config_data[self.Item_n]['ErrorCode']
        self.UploadType = config_data[self.Item_n]['UploadType']
        self.keyword = config_data[self.Item_n]['keyword']
        if len(np.array(self.keyword).shape) == 0:
            self.keyword = self.keyword
        self.checkway = config_data[self.Item_n]['checkway']
        self.parsertype = config_data[self.Item_n]['parsertype']
        self.mValue = config_data[self.Item_n]['value']
        self.max = config_data[self.Item_n]['max']
        self.min = config_data[self.Item_n]['min']
        self.retry = config_data[self.Item_n]['retry']
        self.exe_list = config_data[self.Item_n]['execute']

    def execute(self, deviceName="", tmp=""):
        execute_str = ""
        execute_strs = []

        if self.RunType == "run_system":
            for i in range(0, len(self.exe_list)):
                self.exe_list[i][0] = self.exe_list[i][0].replace('deviceName', deviceName)
                self.exe_list[i][0] = self.exe_list[i][0].replace('tmp', tmp)
                execute_str = os.system(self.exe_list[i][0])
            return execute_str
        elif self.RunType == "read_popen":
            for i in range(0, len(self.exe_list)):
                self.exe_list[i][0] = self.exe_list[i][0].replace('deviceName', deviceName)
                self.exe_list[i][0] = self.exe_list[i][0].replace('tmp', tmp)

            for i in range(0, len(self.exe_list)):
                if self.exe_list[i][1]:  # self.exe_list[i][1]==1
                    # print("commend:", self.exe_list[i][0])
                    execute_str += os.popen(self.exe_list[i][0]).read()
                else:  # self.exe_list[i][1]==0
                    os.system(self.exe_list[i][0])

            return execute_str
        elif self.RunType == "adb devices":
            retry = 70
            cmd = os.popen("adbdevices.bat").read()
            mretry = retry
            while deviceName.lower() not in cmd.lower():
                print(cmd)
                print("deviceName= %s ...countdown= %d" % (deviceName, mretry))
                time.sleep(1)
                mretry = mretry-1
                if mretry <= 0:
                    return self.ErrorCode
                cmd = os.popen("adbdevices.bat").read()
            return "PASS"
        elif self.RunType == "input_data":
            InputData =  os.popen('python ui/InputDialog.py "DSN:" "CSN"').read().replace("\n","")
            return InputData
        elif self.RunType == "serial":
            serial_str = ""

            self.mser = SerialSettingClass(115200, sendhex=False, readhex=False)
            self.mser.connectPort()

            for i in range(0, len(self.exe_list)):
                if self.exe_list[i][1]:  # self.exe_list[i][1]==1
                    self.mser.write((self.exe_list[i][0] + "\r\n").encode())
                    serial_str = self.mser.Receive_data().decode()
                else:
                    self.mser.write((self.exe_list[i][0] + "\r\n").encode())

            self.mser.closePort()
            return serial_str

    def parser(self, result):

        if  self.parsertype == "Get_int":
            try:
                result = [int(temp)for temp in result.split() if temp.isdigit()] #擷取int
                return result[0]
            except:
                return result
        elif  self.parsertype == "Get_float":
            try:
                result = [float(s) for s in re.findall(r'-?\d+\.?\d*', result)] #擷取float
                return result[0]
            except:
                return result
        else:
            return result

    def check(self, result, tmp=""):
        if tmp != "":
            self.keyword = tmp

        #if result == None or result == "":
            #return self.ErrorCode

        if self.checkway == "Than size":  # 使用json中的min與max判斷是否Pass
            try:
                if self.min <= float(result) <= self.max:
                    return "PASS"
                else:
                    return self.ErrorCode
            except:
                return self.ErrorCode
        elif self.checkway == "!=keyword":  # 當回傳值不是keyword時回傳Pass
            if result.lower().find(self.keyword) == -1:
                return "PASS"
            else:
                return self.ErrorCode
        elif self.checkway == "=Count":  # 當指定字串出現特定次數時Pass
            if self.keyword.find(r"=") == -1:
                return self.ErrorCode
            Array = self.keyword.split(r"=")
            if result.count(Array[0]) == int(Array[1]):
                return "PASS"
            else:
                return self.ErrorCode

        elif self.checkway == "CatchKeyword":  # 當回傳值是指定字串時回傳Pass
            if self.keyword in result:
                return "PASS"
            else:
                return self.ErrorCode
        elif self.checkway == "FindKeyword":  # 當回傳值有指定字串時回傳Pass
            if result.find(self.keyword) != -1:
                return "PASS"
            else:
                return self.ErrorCode
        elif self.checkway == "FindAnyKeyword":  # 當回傳值有任一指定字串時回傳Pass
            if any(keyword in result for keyword in self.keyword):
                return "PASS"
            else:
                return self.ErrorCode
        elif self.checkway == "Lens":  # 當指定字串符合長度時回傳Pass，如SN
            result = result.replace('\n', '').replace(' ', '')
            if len(result) == int(self.keyword):
                return "PASS"
            else:
                return self.ErrorCode
        elif self.checkway == "Mac":  # 當指定字串符合MAC格式時回傳Pass
            print("result.count(':') =" + str(result.count(':')))
            if result.count(':') == 5:
                if result == tmp:
                    return "PASS"
                else:
                    return self.ErrorCode
            else:
                return self.ErrorCode
        elif self.checkway == "==PASS":  # 當回傳值含Pass回傳Pass
            if result == "PASS":
                return "PASS"
            else:
                return self.ErrorCode
        elif self.checkway == "AutoPass":  # 一律Pass
            return "PASS"
        else:
            return self.ErrorCode

    def ReturntoValue(self, Return, PassFail):
        if self.mValue == "value":
            return Return
        else:
            if PassFail == "PASS":
                return "1"
            else:
                return "0"


