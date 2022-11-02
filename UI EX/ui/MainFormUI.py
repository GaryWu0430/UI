# -*- coding:utf-8 -*-
try:
    # python 2
    from Tkinter import *
    import ttk
except Exception:
    # python 3
    from tkinter import *
    from tkinter import ttk
from PIL import Image, ImageTk  # pip install Pillow
import sys
import platform
import os


class MainFormUI:
    def __init__(self, main_program):
        self.main_program = main_program
        self.num_of_frames = main_program.num_of_frames   # 版面數量

        self.assets_path = 'ui/assets/'  # 圖檔路徑
        self.image = []  # 圖片位址
        self.input_sn = []  # 輸入框的序號

        self.window = Tk()
        self.window_init()
        self.ui_init()
        self.bind_events()

    # 圖檔處理函數
    def image_process(self, file_name):
        image_path = self.assets_path + file_name + '.png'
        self.image.append(Image.open(image_path))  # 讀入圖檔
        image_w = int(self.image[-1].width * self.scale)  # 圖檔寬度
        image_h = int(self.image[-1].height * self.scale)  # 圖檔高度
        self.image[-1] = self.image[-1].resize((image_w, image_h))  # 縮放圖片
        self.image[-1] = ImageTk.PhotoImage(self.image[-1])  # 轉換成tkinter格式
        return self.image[-1]

    # 建立文字函數
    def new_text(self, x, y, size, text, color='black', center=False, bold=False):
        color_list = {
            'black': '#000000',  # 黑
            'dark': '#444444',  # 深灰
            'light': '#888888',  # 淺灰
            'white': '#FFFFFF',  # 白
            'blue':'#0000FF',#藍
            'red':'#FF0000',#紅
        }
        anchor = 'n' if center else 'nw'  # 是否左右置中
        weight = 'bold' if bold else 'normal'  # 是否粗體
        font_name = 'Consolas'  # 字體
        font_size = int(size * -1 * self.scale)  # 字體大小

        text = self.canvas.create_text(
            x * self.scale,
            y * self.scale,
            anchor=anchor,
            text=text,
            fill=color_list.get(color, color),
            font=(font_name, font_size, weight)
        )
        return text

    # 似圓角矩形函數
    def round_rectangle(self, x, y, w, h, r, shadow_stytle='', **arg):
        if shadow_stytle == 'bg':
            c1, c2 = '#E5E5E5', '#000000'
            d, xo, yo = 8, 2.5, 5
            self.gradient_shadow(x, y, w, h, r, c1, c2, d, xo, yo)
        elif shadow_stytle == 'white':
            c1, c2 = '#FFFFFF', '#444444'
            d, xo, yo = 14, 3, 6
            self.gradient_shadow(x, y, w, h, r, c1, c2, d, xo, yo)

        x1 = x * self.scale
        y1 = y * self.scale
        x2 = (x + w) * self.scale
        y2 = (y + h) * self.scale
        r *= self.scale
        arg['fill'] = '' if not arg.get('fill') else arg['fill']
        points = (
            x1 + r, y1, x1 + r, y1, x2 - r, y1, x2 - r, y1, x2, y1,
            x2, y1 + r, x2, y1 + r, x2, y2 - r, x2, y2 - r, x2, y2,
            x2 - r, y2, x2 - r, y2, x1 + r, y2, x1 + r, y2, x1, y2,
            x1, y2 - r, x1, y2 - r, x1, y1 + r, x1, y1 + r, x1, y1
        )
        return self.canvas.create_polygon(points, smooth=True, **arg)

    # 圓角矩形陰影函數
    def gradient_shadow(self, x, y, w, h, r, c1, c2, d, xo=0, yo=0):
        x10 = x * self.scale
        y10 = y * self.scale
        x20 = (x + w) * self.scale
        y20 = (y + h) * self.scale
        r0 = r * self.scale

        c10, c20 = [], []
        for i in range(1, 7, 2):
            c10.append(int(c1[i:i + 2], 16))
            c20.append(int(c2[i:i + 2], 16))

        for i in range(d - 1, 0, -1):
            x1 = x10 + (xo * (0.3 * (2.5 + (i / d))) - i) * self.scale
            y1 = y10 + (yo * (0.3 * (2.5 + (i / d))) - i) * self.scale
            x2 = x20 + (xo * (0.3 * (2.5 + (i / d))) + i) * self.scale
            y2 = y20 + (yo * (0.3 * (2.5 + (i / d))) + i) * self.scale
            r = r0 + i * self.scale
            c = '#'
            for j in range(3):
                c00 = int(c20[j] + (c10[j] - c20[j]) * i**0.2 / d**0.2)
                c += str(hex(c00))[-2:].replace('x', '0').upper()
            points = (
                x1 + r, y1, x1 + r, y1, x2 - r, y1, x2 - r, y1, x2, y1,
                x2, y1 + r, x2, y1 + r, x2, y2 - r, x2, y2 - r, x2, y2,
                x2 - r, y2, x2 - r, y2, x1 + r, y2, x1 + r, y2, x1, y2,
                x1, y2 - r, x1, y2 - r, x1, y1 + r, x1, y1 + r, x1, y1
            )
            self.canvas.create_polygon(points, smooth=True, fill=c)

    # 初始化視窗
    def window_init(self):
        # Window
        self.window.title(self.main_program.title)
        self.window.configure(bg="#E5E5E5")
        if platform.system() == 'Windows':
            self.window.iconbitmap(self.assets_path + 'delta_icon.ico')
            self.window.state('zoomed')
            self.window.update()
            self.ww = self.window.winfo_width()  # 視窗寬度
            self.wh = self.window.winfo_height()  # 視窗高度
        else:
            self.ww = self.window.winfo_screenwidth()  # 視窗寬度
            self.wh = self.window.winfo_screenheight() - 64  # 視窗高度
        self.window.geometry('%dx%d' % (self.ww, self.wh))

        # Canvas
        bg_w = 2400  # 寬度基數
        bg_h = 1280  # 高度基數
        self.scale = min(float(self.ww) / bg_w, float(self.wh) / bg_h)  # 自適應分辨率縮放比例
        self.cw = int(bg_w * self.scale)  # 畫布寬度
        self.ch = int(bg_h * self.scale)  # 畫布高度
        self.cx = (self.ww - self.cw) * 0.5  # 畫布x座標
        self.cy = (self.wh - self.ch) * 0.5  # 畫布y座標

        # 創建畫布
        self.canvas = Canvas(self.window, width=self.cw, height=self.ch, highlightthickness=0, bg='#E5E5E5')
        self.canvas.place(x=self.cx, y=self.cy)

    # 初始化UI
    def ui_init(self):
        # 左側白框
        self.round_rectangle(x=20, y=20, w=400, h=740, r=20, fill='#FFFFFF', shadow_stytle='bg')
        self.round_rectangle(x=20, y=780, w=400, h=280, r=20, fill='#FFFFFF', shadow_stytle='bg')
        self.round_rectangle(x=20, y=1080, w=400, h=180, r=20, fill='#FFFFFF', shadow_stytle='bg')

        # 左側資訊欄
        info_text = self.main_program.info_text
        if len(info_text) == 0:
            info_text = [['', '']]  # noqa

        info_nums = len(info_text)
        item_frame_y_distance = 720 / info_nums
        text_size = 240 / info_nums
        text_y1 = 38 + 90 / info_nums
        text_y2 = text_y1 + 192 / info_nums

        for i in range(info_nums):
            content_text = info_text[i][1]
            content_text_size = text_size

            if len(info_text[i][1]) * content_text_size > 600:
                content_text_size *= 0.5
                n = int(570 / content_text_size)
                content_text = content_text[:n] + '\n' + content_text[n:]

            self.round_rectangle(
                x=40,
                y=40 + item_frame_y_distance * i,
                w=360,
                h=item_frame_y_distance - 20,
                r=20,
                outline='#D8D8D8',
                width=3 * self.scale
            )
            self.new_text(x=65, y=text_y1 + item_frame_y_distance * i, size=int(text_size * 0.7), text=info_text[i][0], color='light')
            self.new_text(x=65, y=text_y2 + item_frame_y_distance * i, size=int(content_text_size), text=content_text, color='black')

        # Total
        self.total_text = self.new_text(x=218, y=790, size=50, text='0', color='dark', center=True)
        self.new_text(x=180, y=850, size=32, text='TOTAL', color='dark')
        # Pass
        self.round_rectangle(x=40, y=900, w=170, h=140, r=20, fill='#30EE30', shadow_stytle='white')
        self.pass_text = self.new_text(x=125, y=920, size=58, text='0', color='white', center=True, bold=True)
        self.new_text(x=90, y=985, size=36, text='PASS', color='white', bold=True)
        # Fails
        self.round_rectangle(x=230, y=900, w=170, h=140, r=20, fill='#EE3E3E', shadow_stytle='white')
        self.fail_text = self.new_text(x=317, y=920, size=58, text='0', color='white', center=True, bold=True)
        self.new_text(x=282, y=985, size=36, text='FAIL', color='white', bold=True)
        # Test time
        self.canvas.create_image(74 * self.scale, 1134 * self.scale, anchor="nw", image=self.image_process('clock'))
        self.round_rectangle(x=40, y=1100, w=360, h=140, r=20,outline='#D8D8D8', width=3 * self.scale)
        self.new_text(x=170, y=1128, size=28, text='TEST TIME', color='light')
        self.time_text = self.new_text(x=170, y=1160, size=40, text='0:00:00.0', color='dark')

        # 視窗上方UI
        self.round_rectangle(x=440, y=20, w=1940, h=140, r=20, fill='#FFFFFF', shadow_stytle='bg')

        self.sn_entry = []
        self.sn_entry_bg = []
        for i in range(self.num_of_frames):
            if self.num_of_frames == 1:  # 單板版型
                entry_font_size = 60  # 輸入框文字大小
                entry_x = self.cx + 650 * self.scale
                entry_y = self.cy + 45 * self.scale
                entry_w = 1300 * self.scale
                entry_h = 90 * self.scale
                bx, bw = 640, 1320
                by, bh = 40, 100
                # 文字'S/N:'
                self.new_text(x=500, y=60, size=50, text='S/N:', color='dark')
            else:  # 多連版版型
                tx = i * 380 * 4 / self.num_of_frames    # x座標間距
                entry_font_size = 40  # 輸入框文字大小
                entry_x = self.cx + (470 + tx) * self.scale
                entry_y = self.cy + 78 * self.scale
                entry_w = (1520 / self.num_of_frames - 40) * self.scale
                entry_h = 60 * self.scale
                bx = 460 + tx
                bw = 1520 / self.num_of_frames - 30
                by, bh = 40, 100
                # 文字'S/N:'
                self.new_text(x=475 + tx, y=45, size=30, text='S/N %d:' % (i + 1), color='dark')

            # 輸入框
            self.sn_entry_bg.append('')
            self.sn_entry_bg[i] = self.round_rectangle(
                x=bx,
                y=by,
                w=bw,
                h=bh,
                r=20,
                fill='#E3E3E3'
            )
            self.sn_entry.append('')
            self.input_sn.append(StringVar())
            self.sn_entry[i] = Entry(
                bd=0,
                bg='#E3E3E3',
                font=('Consolas', int(entry_font_size * -1 * self.scale)),
                textvariable=self.input_sn[i],
                highlightthickness=0,fg = 'red'
            )
            self.sn_entry[i].place(
                x=entry_x,
                y=entry_y,
                width=int(entry_w),
                height=int(entry_h)
            )

            # 文字'S/N:'
            if self.num_of_frames == 1:  # 單板版型
                self.new_text(x=500, y=60, size=50, text='S/N:', color='dark')  # 文字'S/N:'
            else:  # 多連版版型
                self.new_text(x=475 + tx, y=45, size=30, text='S/N %d:' % (i + 1), color='dark')  # 文字'S/N:'

        self.sn_entry[0].focus()  # 輸入焦點移至第一個輸入框

        # Start按鈕
        self.bt_start_img = self.image_process('start')
        self.bt_start_img_hover = self.image_process('start_hover')
        self.bt_start = Button(
            image=self.bt_start_img,
            borderwidth=3 * self.scale,
            relief="flat",
        )
        self.bt_start.place(
            x=self.cx + 1980 * self.scale,
            y=self.cy + 40 * self.scale,
            width=self.bt_start_img.width(),
            height=self.bt_start_img.height()
        )

        # Start鍵hover樣式
        def bt_start_enter(event):
            if self.bt_start['state'] == 'normal':
                self.bt_start['image'] = self.bt_start_img_hover

        def bt_start_leave(event):
            self.bt_start['image'] = self.bt_start_img

        self.bt_start.bind('<Enter>', bt_start_enter)
        self.bt_start.bind('<Leave>', bt_start_leave)

        # Finish按鈕
        self.bt_finish_img = self.image_process('finish')
        self.bt_finish_img_hover = self.image_process('finish_hover')
        self.bt_finish = Button(
            image=self.bt_finish_img,
            borderwidth=3 * self.scale,
            relief="flat",
            state='disabled'
        )
        self.bt_finish.place(
            x=self.cx + 2180 * self.scale,
            y=self.cy + 40 * self.scale,
            width=self.bt_finish_img.width(),
            height=self.bt_finish_img.height()
        )

        # Finish鍵hover樣式
        def bt_finish_enter(event):
            if self.bt_finish['state'] == 'normal':
                self.bt_finish['image'] = self.bt_finish_img_hover

        def bt_finish_leave(event):
            self.bt_finish['image'] = self.bt_finish_img

        self.bt_finish.bind('<Enter>', bt_finish_enter)
        self.bt_finish.bind('<Leave>', bt_finish_leave)

    # 綁定事件
    def bind_events(self):
        self.bt_start['command'] = self.start_button_click  # Start按鈕
        self.bt_finish['command'] = self.finish_button_click  # Finish按鈕
        self.window.bind('<Return>', self.enter_key_down)  # Enter鍵

        # 按下Z自動填入ZZ99999
        self.window.bind('<Key-z>', self.sn_zz99999)
        self.window.bind('<Key-Z>', self.sn_zz99999)

        # 當輸入框S/N值有變動時轉為大寫
        for i in range(len(self.input_sn)):
            self.input_sn[i].trace('w', self.set_upper)

        # 點選輸入框時自動全選
        for entry in self.sn_entry:
            entry.bind("<FocusIn>", self.auto_select)

        # F10 壓力測試
        self.window.bind('<F10>', self.main_program.stress_test)

    # Star按鈕按下
    def start_button_click(self):
        self.main_program.start()

    # Finish按鈕按下
    def finish_button_click(self):
        self.main_program.interrupt()

    # Enter鍵按下
    def enter_key_down(self, event):
        index = self.sn_entry.index(self.window.focus_get())
        if index == self.num_of_frames - 1:  # 如果被選中輸入框為最後一個
            if self.bt_start['state'] == 'normal':
                self.start_button_click()
        else:
            self.sn_entry[index + 1].focus()  # 焦點移至下一個輸入框

    # 自動填入ZZ99999
    def sn_zz99999(self, event):
        if self.window.focus_get() in self.sn_entry:
            index = self.sn_entry.index(self.window.focus_get())
            if len(self.input_sn[index].get()) == 1:
                self.input_sn[index].set("ZZ99999")
                self.sn_entry[index].icursor(7)

    # 輸入框S/N轉為大寫
    def set_upper(self, *event):
        for sn in self.input_sn:
            sn.set(sn.get().upper())

    # 自動全選文字
    def auto_select(self, event):
        if self.window.focus_get() in self.sn_entry:
            index = self.sn_entry.index(self.window.focus_get())
            self.sn_entry[index].selection_range(0, END)

    # 主迴圈
    def main_loop(self):
        self.window.mainloop()


class FrameUI:
    def __init__(self, main_form, id):
        self.main_form = main_form
        self.id = id  # 第幾個頁框

        self.num_of_frames = main_form.num_of_frames  # 版面數量

        self.frame_init()
        self.table_init()
        self.status_bar_init()

    # 初始化頁框
    def frame_init(self):
        self.frame = Frame(self.main_form.window)

        self.frame_height = (1100 - self.num_of_frames * 20) / self.num_of_frames  # 頁框高度
        self.frame_y = 179 + (self.frame_height + 20) * self.id  # 頁框y座標

        # 頁框底色
        self.bg = self.main_form.round_rectangle(
            x=440,
            y=self.frame_y,
            w=1940,
            h=self.frame_height,
            r=20,
            shadow_stytle='bg'
        )
        # 頁框
        self.frame.place(
            x=self.main_form.cx + 460 * self.main_form.scale,
            y=self.main_form.cy + (self.frame_y + 20) * self.main_form.scale,
            width=1900 * self.main_form.scale,
            height=(self.frame_height - 100) * self.main_form.scale
        )
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)

        self.main_form.window.update()

    # 初始化表格
    def table_init(self):
        # 內容尺寸
        if self.num_of_frames < 4:
            table_font_size = int(-32 * self.main_form.scale)  # 文字大小
            table_row_height = int(40 * self.main_form.scale)  # 行高
        else:
            table_font_size = int(-25 * self.main_form.scale)  # 文字大小
            table_row_height = int(28 * self.main_form.scale)  # 行高

        # 欄位標題/寬度
        heading_list = self.main_form.main_program.heading_list

        # 欄位寬度自適應分辨率
        table_width_ratio = float(self.frame.winfo_width() - 16) / 100  # 16為滾動條近似寬度

        # 建立表格
        self.table = ttk.Treeview(self.frame, height=25, show="headings", takefocus=False)
        ttk.Style().configure("Treeview.Heading", font=("Consolas", table_font_size), )  # 標題列樣式
        ttk.Style().configure("Treeview", font=("Consolas", table_font_size), rowheight=table_row_height)  # 內容樣式
        ttk.Style().layout("Treeview", [('Treeview.treearaquaea', {'sticky': 'nswe'})])  # 去掉邊框
        self.table.grid(row=0, column=0)

        # 建立欄位
        str_code_list = []
        for column in heading_list:
            table_columns = list(self.table["columns"])
            table_columns.append(column['name'])
            self.table["columns"] = table_columns
            str_code_list.append("self.table.column('%s', width=%d, anchor='center')" % (column['name'], int(column['width'] * table_width_ratio)))
            str_code_list.append("self.table.heading('%s', text='%s')" % (column['name'], column['name']))
        for i in str_code_list:
            exec(i)

        # 修正 python 3 Treeview row background color 問題
        if sys.version_info.major == 3:
            background = [elm for elm in ttk.Style().map("Treeview", query_opt="background") if elm[:2] != ("!disabled", "!selected")]
            ttk.Style().map("Treeview", background=background)

        # 表格列顏色
        self.table.tag_configure('pass', background='#DDFFE4')
        self.table.tag_configure('fail', background='#FFBBBB')

        # 滾動條
        self.Scroll_bar_y = ttk.Scrollbar(self.frame, command=self.table.yview)
        self.Scroll_bar_y.grid(row=0, column=1, sticky='NS')
        self.scroll_bar_x = ttk.Scrollbar(self.frame, command=self.table.xview, orient=HORIZONTAL)
        self.scroll_bar_x.grid(row=1, column=0, sticky='EW')
        self.table.configure(xscrollcommand=self.scroll_bar_x.set, yscrollcommand=self.Scroll_bar_y.set)

    # 初始化狀態欄
    def status_bar_init(self):
        # SN文字
        text_x = 470
        text_y = self.frame_y + self.frame_height - 70
        self.main_form.new_text(x=text_x, y=text_y, size=20, text='S/N:', color='dark')
        self.sn_text = self.main_form.new_text(x=text_x, y=text_y + 24, size=32, text='')

        # 狀態
        self.state_bg = self.main_form.round_rectangle(
            x=text_x + 350,
            y=text_y,
            w=200,
            h=60,
            r=20,
        )
        self.state_text = self.main_form.new_text(x=text_x + 450, y=text_y + 5, size=44, text='', center=True)

        # Log
        self.log_text = self.main_form.new_text(x=text_x + 575, y=text_y - 2, size=28, text='')

    # 設定狀態顏色
    def set_state_color(self, state):
        bg_color, bg_state_color = '#FFFFFF', '#FFFFFF'

        if state == 'READY':
            bg_color, bg_state_color = '#DDE8FF', '#AAD0FF'

        elif state == 'RUNNING':
            bg_color, bg_state_color = '#EEFFC8', '#EEFF60'

        elif state == 'PASS':
            bg_color, bg_state_color = '#C8FFC8', '#00FF00'

        elif state == 'FAIL':
            bg_color, bg_state_color = '#FFDDDD', '#FF0000'

        self.main_form.canvas.itemconfig(self.bg, fill=bg_color)
        self.main_form.canvas.itemconfig(self.state_bg, fill=bg_state_color)
