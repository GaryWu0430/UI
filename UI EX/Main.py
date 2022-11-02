# -*- coding:utf-8 -*-
import json
import io
from collections import OrderedDict
import os
import threading
import time
from datetime import date
import textwrap
from func.ConnectDB import ConnectDB
from ui.InputDialog import InputDialog
from ui.MainFormUI import MainFormUI, FrameUI
from testPlan import testPlan
import sys

try:
    import Queue as queue  # python 2
except:
    import queue  # python 3


class Main:
    def __init__(self):
        self.is_running = False

        self.total_pass = 0
        self.total_fail = 0
        self.run_times = 0  # for stress test

        self.config_init()
        self.opid_init()
        self.main_form_init()
        self.frame_init()
        self.frame_queue_monitor()
        self.sn_scan()

        self.main_form.main_loop()  # 必需在最後執行

    # 抓Config.json資料
    def config_init(self):
        config_path = 'Config.json'
        with io.open(config_path, 'r', encoding="utf-8") as f:
            data = json.load(f)

        # 將json中的key,value逐項宣告至self
        for key, value in data.items():
            # 處理python 2編碼問題
            if sys.version_info.major == 2:
                if isinstance(value, list):
                    value = [word.encode('utf-8') for word in value]
                elif isinstance(value, str):
                    value = value.encode('utf-8')

            self.__dict__[key] = value


        fixture_config_path = 'fixture.json'
        with io.open(fixture_config_path, 'r', encoding="utf-8") as f:
            data = json.load(f)

        # 將json中的key,value逐項宣告至self
        for key, value in data.items():
            # 處理python 2編碼問題
            if sys.version_info.major == 2:
                if isinstance(value, list):
                    value = [word.encode('utf-8') for word in value]
                elif isinstance(value, str):
                    value = value.encode('utf-8')

            self.__dict__[key] = value
        print self.result 

    # 初始化OPID對話框
    def opid_init(self):
        self.opid = InputDialog(text='OPID:', check_way='opid').get()
        if self.opid == '':
            exit("Need to input OPID.")

    # 初始化主視窗
    def main_form_init(self):
        # 視窗標題
        self.title = self.model_name + ' ' + self.station_name + '  ' + os.path.dirname(os.path.abspath(__file__))
        # 視窗左側資訊欄文字(建議4至8項)
        self.info_text = [
            ['MODEL', self.model_name],
            ['STATION', self.station_name],
            ['LINE ID', self.line_id],
            ['UPDATE DATE', self.update_date],
            ['OPID', self.opid],
            ['LOG PATH', self.log_path],
        ]
        # 表格欄位標題/寬度 (版面顯示寬度為100)
        self.heading_list = [
            {'name': 'No.', 'width': 5},
            {'name': 'Item', 'width': 30},
            {'name': 'Result', 'width': 10},
            {'name': 'Low Limit', 'width': 10},
            {'name': 'High Limit', 'width': 10},
            {'name': 'Key Word', 'width': 25},
            {'name': 'Cycle Time', 'width': 10},
            {'name': 'Memo', 'width': 100},
        ]
        # 建立視窗
        self.main_form = MainFormUI(self)

    # 初始化測項頁框
    def frame_init(self):
        self.frame_list = []
        for i in range(self.num_of_frames):
            print('range:%s' % self.num_of_frames)
            self.frame_list.append(TestFrame(self, i))
    
    # 初始化Log路徑
    def log_path_init(self):
        today = date.today().strftime("%Y%m%d")
        log_path = self.log_path + today

        self.pass_log = log_path + "\\fixture" + self.fixtureID +"\\PASS\\"
        self.fail_log = log_path + "\\fixture" + self.fixtureID + "\\FAIL\\"

        if not os.path.exists(self.pass_log):
            os.makedirs(self.pass_log)
        if not os.path.exists(self.fail_log):
            os.makedirs(self.fail_log)

    # 抓StationConfig.json資料
    def station_config_init(self):
        config_path = 'Station_Config.json'
        with io.open(config_path, 'r', encoding="utf-8") as f:
            data = json.load(f, object_pairs_hook=OrderedDict) #  字典順序參照json順序
        self.CheckFail = data['Global']['CheckFail']

        # 將json中的測項逐項append到self.station_config_data
        self.station_config_data = []
        for item_key in data['Station']:
            item = data['Station'][item_key]

            # 處理python 2編碼問題
            if sys.version_info.major == 2:
                for var_key in item:
                    if var_key == 'execute': # execute為二維陣列，跳過不處理
                        continue
                    elif isinstance(item[var_key], list):
                        item[var_key] = [word.encode('utf-8') for word in item[var_key]]
                    elif isinstance(item[var_key], str):
                        item[var_key] = item[var_key].encode('utf-8')

            self.station_config_data.append(item)

    # 頁框列隊監聽
    def frame_queue_monitor(self):
        for frame in self.frame_list:
            while not frame.execute_queue.empty():
                exec(frame.execute_queue.get())
        
        self.main_form.window.after(50, self.frame_queue_monitor)  # 每50毫秒重新執行

    def stress_test(self, event=''):
        self.run_times = int(os.popen('python ui/InputDialog.py "Run Times:"').read())

        # for sn in self.main_form.input_sn:
            # sn.set('ZZ99999')
        
        print('Run Times: {}'.format(self.run_times))
        self.run_times -= 1
        self.start()

    def auto_catch_QSN(self, event=''):
        QSN = os.popen("adb shell cat /pip/QSN").read()
        QSN = QSN.replace("\r","").replace("\n","")
        print("QSN:",QSN)
        for sn in self.main_form.input_sn:
            sn.set(QSN)
        self.start()
    
    def sn_scan(self):
        SN_get_value = os.popen('func\Scansn.py').read()
        print("SN_get_value:",SN_get_value)
        for sn in self.main_form.input_sn:
            sn.set(SN_get_value)
        self.start()

    # Start (Start鍵按下時觸發)
    def start(self):
        # 頁框回復初始狀態
        for frame in self.frame_list:
            frame.set_sn('')
            frame.set_log('')
            frame.set_state('READY')
            frame.clear_table()

        # 檢查序號
        if not self.check_sn():
            self.main_form.sn_entry[0].focus()  # 焦點移至第一個輸入框
            self.main_form.sn_entry[0].selection_range(0, 'end') #SN第一個輸入框全選
            return

        # 切換狀態
        self.is_running = True
        self.main_form.bt_start['state'] = 'disabled'
        self.main_form.bt_finish['state'] = 'normal'
        for i in range(self.main_form.num_of_frames):
            self.main_form.sn_entry[i]['state'] = 'disabled'
            self.main_form.canvas.itemconfig(self.main_form.sn_entry_bg[i], fill='#F0F0F0')

        # 初始化Log路徑 / 抓StationConfig.json資料
        self.log_path_init()
        self.station_config_init()

        # 關治具
        if self.station_on_start != '' and self.station_on_start != 'NONE':
            self.frame_list[0].set_log('Station starting...')
            self.main_form.window.update()

            # 執行
            print(os.popen(self.station_on_start).read())
            
            self.frame_list[0].set_log('')

        #  開始測試
        for frame in self.frame_list:
            # 跳過空序號
            if frame.sn == '':
                continue

            frame.set_state('RUNNING')
            frame.interrupt = False
            frame.test_plan = testPlan()
            frame.thread = threading.Thread(target=frame.test_plan.main, args=(frame, self.iParamAll, ))
            frame.thread.setDaemon(True)
            frame.thread.start()

        # 開始計時
        self.start_time = time.time()
        self.timer()

    # 檢查序號
    def check_sn(self):
        # 如果序號全為空則return False
        empty = 0
        for i in range(self.num_of_frames):
            self.frame_list[i].set_sn(self.main_form.input_sn[i].get())
            if self.frame_list[i].sn == '':
                empty += 1
        if empty == self.num_of_frames:
            self.frame_list[0].set_log('S/N is empty')
            return False

        # check sn for 機種
        for frame in self.frame_list:
            if frame.sn == '' or frame.sn == 'ZZ99999':
                continue
            if "YJ6" not in frame.sn:
                frame.set_log('S/N is wrong!')
                return False

        # Check Routing
        db = ConnectDB()
        is_pass = True
        self.iParamAll = ""

        for frame in self.frame_list:
            if frame.sn == '' or frame.sn == 'ZZ99999':
                continue

            iResult, iMessage, self.iParamAll = db.CheckRoutingFA(frame.sn, self.station_name, self.opid, "1")
            print('S/N: {} FAIL, iResult: {}, iMessage: {}, iParamAll: {}.'.format(frame.sn, iResult, iMessage, self.iParamAll))

            if iResult.upper() != 'PASS':
                frame.set_state('FAIL')
                frame.set_log('S/N: {} FAIL, Message: {}'.format(frame.sn, iMessage))
                is_pass = False

        return is_pass

    # 計時器
    def timer(self):
        if self.is_running:
            elapse = float(time.time() - self.start_time)
            time_str = '%d:%02d:%02d.%d' % (elapse // 3600, elapse % 3600 // 60, elapse % 60 // 1, int(elapse % 1 * 10))
            self.main_form.canvas.itemconfig(self.main_form.time_text, text=time_str)

            self.main_form.window.after(100, self.timer)  # 每100毫秒繼續計時

    # 中斷 (Finish鍵按下時觸發)
    def interrupt(self):
        # 告知頁框中斷執行續
        for frame in self.frame_list:
            if frame.state == 'RUNNING':
                frame.set_log('Stopping...')
                frame.interrupt = True

    # 結束
    def finish(self):
        # 結束running狀態
        print('test result')
        self.is_running = False
        self.main_form.bt_finish['state'] = 'disabled'
        self.main_form.bt_start['state'] = 'normal'
        for i in range(self.main_form.num_of_frames):
            self.main_form.sn_entry[i]['state'] = 'normal'
            self.main_form.canvas.itemconfig(self.main_form.sn_entry_bg[i], fill='#E3E3E3')
        self.main_form.sn_entry[0].focus_set()
        
        # 更新 TOTAL PASS FAIL
        self.set_total_pass_fail()

        # 開治具
        if self.station_on_finish != '' and self.station_on_finish != 'NONE':
            self.frame_list[0].set_log('Station finishing... ' + self.frame_list[0].log)
            self.main_form.window.update()

            # 執行
            print(os.popen(self.station_on_finish).read())

            self.frame_list[0].set_log(self.frame_list[0].log[21:])

        # 檢查Stress test計數
        if self.run_times > 0:
            self.run_times -= 1
            time.sleep(5)
            self.start()
        
        self.main_form.sn_entry[0].selection_range(0, 'end') #SN第一個輸入框全選
        self.sn_scan()

    # PASS FAIL 計數
    def set_total_pass_fail(self):
        for frame in self.frame_list:
            if frame.state == 'PASS':
                self.total_pass += 1
            elif frame.state == 'FAIL':
                self.total_fail += 1
        self.main_form.canvas.itemconfig(self.main_form.total_text, text=self.total_pass+self.total_fail)
        self.main_form.canvas.itemconfig(self.main_form.pass_text, text=self.total_pass)
        self.main_form.canvas.itemconfig(self.main_form.fail_text, text=self.total_fail)


class TestFrame:
    def __init__(self, main_program, id):
        self.main_program = main_program
        self.main_form = main_program.main_form
        self.id = id  # 第幾個頁框(index)
        self.num_of_frames = main_program.num_of_frames  # 版面(頁框)數量

        self.sn = ''  # 序號
        self.state = ''  # 狀態
        self.log = ''  # log
        self.interrupt = False  # 是否中斷
        self.execute_queue = queue.Queue()  # 暫存列隊，避免thread直接呼叫tk方法

        self.frame_ui_init()
        self.set_state('READY')

    # 初始化頁框UI
    def frame_ui_init(self):
        self.frame_ui = FrameUI(self.main_program.main_form, self.id)

    # 設定sn
    def set_sn(self, sn):
        self.sn = sn.strip()  # 去掉前後空格
        self.main_form.canvas.itemconfig(self.frame_ui.sn_text, text=sn)

    # 設定狀態
    def set_state(self, state):
        self.state = state.upper()
        self.main_form.canvas.itemconfig(self.frame_ui.state_text, text=self.state)
        self.frame_ui.set_state_color(self.state)  # 改變顏色
        print('test')
        

        # 在running狀態時檢查
        if self.main_program.is_running:
            for frame in self.main_program.frame_list:
                if frame.state == 'RUNNING':
                    print('-----')
                    return
            # 全部頁框都已經結束
            self.main_program.finish()

    # 設定log
    def set_log(self, log):
        self.log = log
        log = textwrap.fill(log, 88)
        if 'PASS' in self.log:
            self.main_form.canvas.itemconfig(self.frame_ui.log_text, text=log, fill='#000000')
        else:
            self.main_form.canvas.itemconfig(self.frame_ui.log_text, text=log, fill='#DD0000')

    # 新增列
    def add_item(self, *arg):
        if  arg[2] == 'PASS':  # 2為check_result的index位置
            self.frame_ui.table.insert('', 'end', values=arg, tags = ('pass',))
        else:
            self.frame_ui.table.insert('', 'end', values=arg, tags = ('fail',))
        # 畫面滾動至底部
        self.frame_ui.table.yview_moveto(1)

    # 清空表格
    def clear_table(self):
        self.frame_ui.table.delete(*self.frame_ui.table.get_children())

    # Thread 設定狀態
    def t_set_state(self, state):
        self.execute_queue.put("frame.set_state('{}')".format(state))
        
    # Thread 設定log
    def t_set_log(self, log):
        self.execute_queue.put(("frame.set_log('{}')".format(log)))
        
    # Thread 新增列
    def t_add_item(self, *arg):
        self.execute_queue.put(("frame.add_item{}".format(arg)))

if __name__ == '__main__':
    app = Main()
