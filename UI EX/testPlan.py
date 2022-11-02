# -*- coding:utf-8 -*-
import os
import time
from datetime import datetime
from serial.tools.list_ports_windows import NULL
from Station import *
import shutil
import csv
from func.ConnectDB import ConnectDB
import random  # for test
from threading import Lock
from copy import deepcopy
from collections import OrderedDict

mutex = Lock()  # 互斥鎖


class testPlan:
    def main(self, frame, iParamAll):
        self.frame = frame
        self.iParamAll = iParamAll
        self.main_program = frame.main_program

        self.pass_log = self.main_program.pass_log
        self.fail_log = self.main_program.fail_log
        self.CheckFail = self.main_program.CheckFail
        self.FixtureID = self.main_program.fixtureID
        self.fixture_com_port = self.main_program.fixture_com_port
        self.com_port = self.main_program.com_port
        self.station_config_data = deepcopy(self.main_program.station_config_data)

        self.sf_data_init()
        self.test_on_start()
        self.test_item()
        self.test_on_finish()

        self.frame.t_set_state(self.pass_fail)  # 輸出結果(告知Main測試結束)

    # 抓SF資料
    def sf_data_init(self):

        #  excemple
        debug = True
        sn = self.frame.sn
        if sn != "ZZ99999":
            SF_Data_All = self.iParamAll.split(";")
            for i in SF_Data_All:
                SF_Data = i.split("=")
                if SF_Data[0] == "CSN":
                    self.DSN = SF_Data[1]
                    print("DSN:",self.DSN)
                elif SF_Data[0] == "TARGET":
                    self.CLOVER_TARGET = SF_Data[1]
                    print("TARGET:",self.CLOVER_TARGET)
                elif SF_Data[0] == "WiFi_Area":
                    self.WiFi_Area = SF_Data[1]
                    print("WiFi_Area:",self.WiFi_Area)
                elif SF_Data[0] == "SB_CPUID":
                    self.SB_CPUID = SF_Data[1].replace("DEK_","")
                    print("SB_CPUID:",self.SB_CPUID)
                elif SF_Data[0] == "CPUID":
                    self.MB_CPUID = SF_Data[1].replace("DEK_","")
                    print("MB_CPUID:",self.MB_CPUID)
                elif SF_Data[0] == "EMac":
                    self.LANMac = SF_Data[1]
                    print("LANMac:",self.LANMac)
                elif SF_Data[0] == "MB":
                    self.MBSN = SF_Data[1]
                    print("MBSN:",self.MBSN)
                elif SF_Data[0] == "BMac":
                    self.BTMac = SF_Data[1]
                    print("BTMac:",self.BTMac)
                elif SF_Data[0] == "WMac":
                    self.WiFiMac = SF_Data[1]
                    print("WiFiMac:",self.WiFiMac)
                elif SF_Data[0] == "HW version":
                    self.HW_VERSION = SF_Data[1]
                    print("HW_VERSION:",self.HW_VERSION)
                elif SF_Data[0] == "MB ID":
                    self.MBID = SF_Data[1]
                    print("MB ID:",self.MBID)
                elif SF_Data[0] == "Platform ID":
                    self.Platform_ID = SF_Data[1]
                    print("Platform ID:",self.Platform_ID)
                elif SF_Data[0] == "SB FW Version":
                    self.SB_FW = SF_Data[1]
                    print("SB FW Version:",self.SB_FW)
                elif SF_Data[0] == "Test image Version":
                    self.MFG_Ver = SF_Data[1].replace(".","")
                    print("MFG Version:",self.MFG_Ver)
                
            if self.DSN[4] == "U":
                self.LTE_model="MC116-NA"
            elif self.DSN[4] == "E" or self.DSN[4] == "A" or self.DSN[4] == "L":
                self.LTE_model="MC116-EUL"
            print("LTE model:",self.LTE_model)
                
    # 個別測項處理
    def tmp(self, item):
        execute_tmp = ""
        check_tmp = ""
        auto_pass = False
        
        sn = self.frame.sn

        if item.Name == "QSN Test":
            if sn != "ZZ99999":
                execute_tmp = str(sn)
                check_tmp = str(sn)
            else:
                item.retry = 0
        elif item.Name == "DSN Test":
            if sn != "ZZ99999":
                execute_tmp = self.DSN
                check_tmp = self.DSN
            else:
                item.retry = 0
        elif item.Name == "CLOVER_TARGET Test":
            if sn != "ZZ99999":
                execute_tmp = self.CLOVER_TARGET
                check_tmp = self.CLOVER_TARGET
            else:
                item.retry = 0
        elif item.Name == "WIFI_AREA Test":
            if sn != "ZZ99999":
                execute_tmp = self.WiFi_Area
                check_tmp = self.WiFi_Area
            else:
                item.retry = 0
        elif item.Name == "HW VERSION":
            if sn != "ZZ99999":
                execute_tmp = self.HW_VERSION
                check_tmp = self.HW_VERSION
            else:
                execute_tmp = "1.01"
                check_tmp = "1.01"
        elif item.Name == "WIFI_MAC Test":
            if sn != "ZZ99999":
                check_tmp = self.WiFiMac
            else:
                auto_pass = True
        elif item.Name == "BT_MAC Test":
            if sn != "ZZ99999":
                check_tmp = self.BTMac
            else:
                auto_pass = True
        elif item.Name == "EMAC Test":
            if sn != "ZZ99999":
                check_tmp = self.LANMac
            else:
                auto_pass = True
        elif item.Name == "MB_SN Test":
            if sn != "ZZ99999":
                check_tmp = self.MBSN
            else:
                auto_pass = True
        elif item.Name == "CPUID":
            if sn != "ZZ99999":
                check_tmp = self.MB_CPUID
            else:
                auto_pass = True
        elif item.Name == "SB CPUID Test":
            if sn != "ZZ99999":
                check_tmp = self.SB_CPUID
            else:
                auto_pass = True
        elif item.Name == "LTE modem model type":
            if sn != "ZZ99999":
                check_tmp = self.LTE_model
            else:
                auto_pass = True
        elif item.Name == "SB firmware":
            if sn != "ZZ99999":
                check_tmp = self.SB_FW
        elif item.Name == "ROM Version" or item.Name == "UART debug port":
            if sn != "ZZ99999":
                check_tmp = self.MFG_Ver
        elif item.Name == "MB ID":
            if sn != "ZZ99999":
                check_tmp = self.MBID
        elif item.Name == "Platform ID":
            if sn != "ZZ99999":
                check_tmp = self.Platform_ID
        
        


        return execute_tmp, check_tmp, auto_pass

    # 測試前準備 (上電)
    def test_on_start(self):
        try:
            test_on_start = self.main_program.test_on_start[self.frame.id]
        except Exception:
            test_on_start = ''
        if test_on_start != '' and test_on_start != 'NONE':
            self.frame.t_set_log('Test starting...')
            time.sleep(0.1)

            # 執行
            mutex.acquire()  # 上鎖
            print(os.popen(test_on_start).read())
            mutex.release()  # 解鎖

            self.frame.t_set_log('')

    # 主程式
    def test_item(self):
        first_error = 'PASS'
        input_string = ''

        frame = self.frame
        frame_id = frame.id  # 0, 1, 2 or 3
        sn = frame.sn
        station_name = self.main_program.station_name
        line_id = self.main_program.line_id
        opid = self.main_program.opid
        adb_id = self.main_program.adb_id[frame.id]
        CheckFail = self.CheckFail
        item_sum = len(self.station_config_data)  # Total numbers of items

        # 超過1版時，用來判別Log
        if self.main_program.num_of_frames == 1:
            id_str = ''
        else:
            id_str = 'ID:{}, '.format(frame_id)

        print(
            '----------------------------------------\n'
            'Frame ID: {frame_id}\n'
            'Test S/N: {sn}\n'
            'Station name: {station_name}\n'
            'ADB ID: {adb_id}\n'
            'CheckFail: {CheckFail}\n'
            'Sum Items: {item_sum}\n'
            '----------------------------------------\n'
            .format(frame_id=frame_id, sn=sn, station_name=station_name, adb_id=adb_id, CheckFail=CheckFail, item_sum=item_sum)
        )

        # 開始測試
        self.openHtmlFile()
        total_start_time = time.time()

        for i in range(item_sum):
            item = Station_class(i, self.station_config_data)

            # CheckFail
            if self.CheckFail == 'Y' and first_error != 'PASS':
                self.outputHtml(i, item.Name, '', item.min, item.max, item.keyword, "", 0.0, "")
                continue

            start_time = time.time()

            # 個別測項處理
            execute_tmp, check_tmp, auto_pass = self.tmp(item)
            print('execute_tmp:%s, check_tmp:%s, auto_pass:%s'%(execute_tmp, check_tmp, auto_pass))

            if item.retry == 0:
                execute_result = 'Skip'
                parser_result = 'Skip'
                check_result = 'PASS'
                value = 'PASS'

            # Retry
            while item.retry > 0:
                # run execute and check result
                execute_result = item.execute(adb_id, execute_tmp)
                parser_result = item.parser(execute_result)
                check_result = item.check(parser_result, check_tmp)
                value = item.ReturntoValue(parser_result, check_tmp)  # 依設定邏輯決定輸出Value是 default(0 or 1) or Value

                if item.UploadType != "NONE" and sn != "ZZ99999" and check_result == "PASS": # Record to SF (Link)
                    db = ConnectDB()
                    Uploadres = db.SFCompareFA(sn, parser_result, item.UploadType, station_name, line_id)
                    print("res:", Uploadres)
                    print("Upload res:", Uploadres.get('Result'))
                    if Uploadres.get('Result') != "1":
                        execute_result += "\r" + Uploadres.get('Message')
                        check_result = item.ErrorCode
                        
                if auto_pass:
                    check_result = 'PASS'

                # Just for test
                '''
                time.sleep(random.uniform(0.1, 0.5))
                execute_result = 'execute result......'
                parser_result = 'parser result......'
                r = random.random()
                if r > 0.03:
                    check_result = 'PASS'
                else:
                    check_result = 'FAIL'
                value = item.ReturntoValue(parser_result, check_result)
                '''
                print(
                    '----------------------------------------\n'
                    'Frame ID: {frame_id}\n'
                    'Run the NO.{no} {item_name} ({retry}) times:\n'
                    'Execute result: {execute_result}\n'
                    'Parser result: {parser_result}\n'
                    'Check result: {check_result}\n'
                    'Value: {value}\n'
                    '----------------------------------------\n'
                    .format(
                        frame_id=frame_id,
                        no=i + 1,
                        item_name=item.Name,
                        retry=item.retry,
                        execute_result=execute_result,
                        parser_result=parser_result,
                        check_result=check_result,
                        value=value
                    )
                )

                item.retry -= 1
                if check_result == "PASS":
                    break
                if item.Name == "adb devices" and check_result != "PASS":
                    self.CheckFail = "Y"
                time.sleep(1)

            cycle_time = '{:.02f}'.format(time.time() - start_time)

            # 處理parser_result過長
            parser_result = str(parser_result)
            if len(parser_result) >= 50:
                parser_result = check_result
                value = check_result

            # 輸出測項結果
            frame.t_add_item(i + 1, item.Name, check_result, item.min, item.max, item.keyword, cycle_time, parser_result)
            self.outputHtml(i + 1, item.Name, value, item.min, item.max, item.keyword, check_result, cycle_time, execute_result)

            parser_result = parser_result.replace("#", "_")
            result_str = '##{}={}'.format(item.Name, value)  # for normal

            input_string += result_str

            # First error
            if check_result != 'PASS' and first_error == 'PASS':
                first_error = check_result

            #  監聽中斷訊號
            if frame.interrupt:
                frame.t_set_log('Test interrupted.')
                time.sleep(0.1)
                self.pass_fail = 'FAIL'
                return

        # 結束測試
        if first_error == 'PASS':
            self.pass_fail = 'PASS'
        else:
            self.pass_fail = 'FAIL'
        #  first_error may be 'PASS', 'FAIL' or ErrorCode that defined in 'Station_Config.json'.
        #  self.pass_fail will only be 'PASS' or 'FAIL'.

        total_cycle_time = '{:.02f}'.format(time.time() - total_start_time)
        self.closeHtmlFile(self.pass_fail, total_cycle_time)

        # 處理 input_string
        input_string = (
            '##Appraiser={opid}'
            '{input_string}'
            '##Result={pass_fail}'
            '##ErrorCode={first_error}'
            '##TestTime={total_cycle_time}'
            '##FixtureID={FixtureID}'
            .format(opid=opid, input_string=input_string, pass_fail=self.pass_fail, first_error=first_error, total_cycle_time=total_cycle_time, FixtureID=self.FixtureID)
        )
        input_string = input_string.replace("\n", "").replace("\r", "").replace("!", "")

        # 上傳Shop Floor/顯示結果
        if sn != 'ZZ99999':
            db = ConnectDB()
            iResult, iMessage = db.UpdateToFADB(sn, station_name, first_error, input_string)

            print('{}S/N: {}, {}, {}, {}.\n'.format(id_str, sn, iResult, iMessage, first_error))
            frame.t_set_log('Message: {}, {}'.format(iMessage, first_error))
        else:
            print('{}S/N: {}, SF Disabled, {}.\n'.format(id_str, sn, first_error))
            frame.t_set_log('SF Disabled , {}'.format(first_error))

        # 寫入txt
        try:
            self.output_input_string_to_txt(input_string)
        except Exception:
            print('Write inputstring_to_SF{}.txt Fail!'.format(self.frame.id + 1))

        # 寫入csv
        mutex.acquire()  # 上鎖
        try:
            self.output_input_string_to_csv(input_string)
        except Exception:
            print('Write QmsFormatData.csv Fail!')
        finally:
            mutex.release()  # 解鎖

    # 測試後收尾 (下電)
    def test_on_finish(self):
        try:
            test_on_finish = self.main_program.test_on_finish[self.frame.id]
        except Exception:
            test_on_finish = ''
        if test_on_finish != '' and test_on_finish != 'NONE':
            message = 'Test finishing...'
            self.frame.t_set_log(message + self.frame.log)
            time.sleep(0.1)

            # 執行
            mutex.acquire()  # 上鎖
            print(os.popen(test_on_finish).read())
            mutex.release()  # 解鎖

            self.frame.t_set_log(self.frame.log[len(message):])

    def openHtmlFile(self):
        tmp_datetime = datetime.now()
        self.log_file_name = tmp_datetime.strftime("%Y%m%d%H%M%S")
        self.timestamp = tmp_datetime.strftime("%Y-%m-%d %H:%M:%S")

        self.tmp_log_file_name = 'log%d.html' % (self.frame.id + 1)
        self.output_html = open(self.tmp_log_file_name, 'w')
        tmp = """<!DOCTYPE html>
            <html lang='en'>
            <head>
            <meta charset='utf-8'>
            <title>{} Test Report</title>
            </head>
            <body>
            <font COLOR='#0000AF' size='6'><div align='left'>{} Test Report</div></font>
            <div align='left'>
            <table border='1'  width='100%'>
            <tr>
            <td><font><B>No</B></font></td>
            <td><font><B>Description</B></font></td>
            <td width ='16%'><font><B>Value</B></font></td>
            <td><font><B>LowLimit</B></font></td>
            <td><font><B>HighLimit</B></font></td>
            <td><font><B>KeyWord</B></font></td>
            <td><font><B>ErrorCode</B></font></td>
            <td><font><B>CycleTime</B></font></td>
            <td><font><B>Memo</B></font></td>
            </tr>"""
        tmp = tmp.format(self.main_program.station_name, self.main_program.station_name)
        self.output_html.write(tmp)

    def outputHtml(self, i, tName, result, LowLimit, HighLimit, KeyWord, ErrorCode, CycleTime, Memo):
        htmlColor = "#0000AF"
        if "PASS" not in ErrorCode:
            htmlColor = "#FF0000"
        if isinstance(Memo, str):
            Memo = Memo.replace('\n', '<br />')
        html = (
            "<tr>"
            "<td><FONT COLOR='#0000AF'>{i}</FONT></td>"
            "<td><FONT COLOR='{htmlColor}'>{tName}</FONT></td>"
            "<td><FONT COLOR='{htmlColor}'>{result}</FONT></td>"
            "<td><FONT COLOR='{htmlColor}'>{LowLimit}</FONT></td>"
            "<td><FONT COLOR='{htmlColor}'>{HighLimit}</FONT></td>"
            "<td><FONT COLOR='{htmlColor}'>{KeyWord}</FONT></td>"
            "<td><FONT COLOR='{htmlColor}'>{ErrorCode}</FONT></td>"
            "<td><FONT COLOR='{htmlColor}'>{CycleTime}</FONT></td>"
            "<td><FONT COLOR='{htmlColor}'>{Memo}</FONT></td>"
            "</tr>"
            .format(
                htmlColor=htmlColor,
                i=i,
                tName=tName,
                result=result,
                LowLimit=LowLimit,
                HighLimit=HighLimit,
                KeyWord=KeyWord,
                ErrorCode=ErrorCode,
                CycleTime=CycleTime,
                Memo=Memo
            )
        )
        self.output_html.write(html)

    def closeHtmlFile(self, result, total_cycle_time):
        hhh = """</table></div><br><br><div><table border='1'  width='30%%'>
            <tr><td><font>Line ID</font></td><td><font COLOR='#0000AF'>{}</font></td></tr>
            <tr><td><font>OP ID</font></td><td><font COLOR='#0000AF'>{}</font></td></tr>
            <tr><td><font>S/N</font></td><td><font COLOR='#0000AF'>{}</font></td></tr>
            <tr><td><font>Start time</font></td><td><font COLOR='#0000AF'>{}</font></td></tr>
            <tr><td><font>Cycle Time(s)</font></td><td><font COLOR='#0000AF'>{}</font></td></tr>
            <tr><font><td>Result</font></td><td><font COLOR='#0000AF'>{}</font></td></tr>
            </table>
            </div></body></html>"""
        hhh = hhh.format(self.main_program.line_id, self.main_program.opid, self.frame.sn, self.timestamp, total_cycle_time, result)
        self.output_html.write(hhh)
        self.output_html.close()
        self.output_html = None
        outPath = (self.fail_log, self.pass_log)["PASS" in result] + self.main_program.station_name + "_" + self.frame.sn + '_' + result + '_' + str(self.frame.id) + '_' + self.log_file_name + '.html'
        sensorPath = (self.fail_log,self.pass_log)["PASS" in result] + "\\" + self.frame.sn  + "\\" + self.log_file_name
        shutil.copyfile(self.tmp_log_file_name, outPath)
        try:
            self.filesRename("sensor_test/",self.frame.sn)
            shutil.move("sensor_test", sensorPath)
        except:
            print("can't find log")
    
    def filesRename(self,path,sn):
        # path='儲存的路徑' #這就是欲進行檔名更改的檔案路徑，路徑的斜線是為/，要留意下！
        files=os.listdir(path)
        print('files:',files) #印出讀取到的檔名稱，用來確認自己是不是真的有讀到

        n=0 #設定初始值
        for i in files: #因為資料夾裡面的檔案都要重新更換名稱
            oldname=path+files[n] #指出檔案現在的路徑名稱，[n]表示第n個檔案
            newname=path+sn+"_"+self.log_file_name+"_"+files[n] 
            os.rename(oldname,newname)
            print(oldname+'>>>'+newname) #印出原名與更名後的新名，可以進一步的確認每個檔案的新舊對應
            n=n+1 #當有不止一個檔案的時候，依次對每一個檔案進行上面的流程，直到更換完畢就會結束

    # 本機儲存 input_string 到 inputstring_to_SF?.txt
    def output_input_string_to_txt(self, input_string):
        inputstring_file = open('inputstring_to_SF{}.txt'.format(self.frame.id + 1), 'w')
        inputstring_file.write(input_string)
        inputstring_file.close()

    # 本機儲存 input_string 到 QmsFormatData.csv
    def output_input_string_to_csv(self, input_string):
        sn = self.frame.sn
        line_id = self.main_program.line_id
        station_name = self.main_program.station_name
        opid = self.main_program.opid
        tmp_datetime = datetime.now()

        file_name = 'QmsFormatData.csv'
        input_string_dic = OrderedDict()
        input_string_dic['SerialNumber'] = sn
        input_string_dic['Line_ID'] = line_id
        input_string_dic['Station'] = station_name
        input_string_dic['Appraiser'] = opid
        input_string_dic['Date'] = tmp_datetime.strftime("%Y/%m/%d")
        input_string_dic['Time'] = tmp_datetime.strftime('%H:%M:%S')

        for item in input_string.strip('##').split('##'):
            item = item.split('=')
            input_string_dic[item[0]] = item[1]

        if os.path.isfile(file_name):
            write_header = False
        else:
            Upper_string = {'SerialNumber': 'Upper Limit ----->'}
            Lower_string = {'SerialNumber': 'Lower Limit ----->'}
            item_sum = len(self.station_config_data)
            for i in range(item_sum):
                item = Station_class(i, self.station_config_data)
                item_name = item.Name.replace(" ", "")
                Upper_string[item_name] = item.max
                Lower_string[item_name] = item.min
            write_header = True

        with open(file_name, 'a') as csvfile:
            writer = csv.DictWriter(csvfile, [key for key in input_string_dic], lineterminator='\n')
            if write_header:
                writer.writeheader()
                writer.writerow(Upper_string)
                writer.writerow(Lower_string)
            writer.writerow(input_string_dic)
