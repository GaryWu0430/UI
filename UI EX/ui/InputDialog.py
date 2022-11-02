# -*- coding:utf-8 -*-
try:
    from Tkinter import *  # python 2
except Exception:
    from tkinter import *  # python 3
from PIL import Image, ImageTk
from textwrap import fill
from sys import argv, stdout
import base64
from io import BytesIO
import platform
import datetime


class InputDialog():
    def __init__(self, text='', check_way=False):
        self.text = text
        self.check_way = check_way

        try:
            self.text = argv[1]
        except Exception:
            pass
        try:
            self.check_way = argv[2].lower()
        except Exception:
            pass

        self.image = []

        self.window = Tk()
        self.window.attributes("-topmost", True)
        self.window_init()
        self.UI_init()
        self.bind_events()

        self.window.mainloop()

    # Return value
    def get(self):
        return self.input_value.get()

    # 圖檔處理函數
    def image_process(self, file_name):
        byte_data = base64.b64decode(eval(file_name))
        image_data = BytesIO(byte_data)
        self.image.append(Image.open(image_data))  # 讀入圖檔
        image_w = int(self.image[-1].width * self.scale)  # 圖檔寬度
        image_h = int(self.image[-1].height * self.scale)  # 圖檔高度
        self.image[-1] = self.image[-1].resize((image_w, image_h))  # 縮放圖片
        self.image[-1] = ImageTk.PhotoImage(self.image[-1], master=self.window)  # 轉換成tkinter格式
        return self.image[-1]

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
        # Icon
        if platform.system() == 'Windows':
            icondata = base64.b64decode(quanta_icon_ico)
            icon_file_name = 'quanta_icon.ico'
            temp_icon = open(icon_file_name, "wb")
            temp_icon.write(icondata)
            temp_icon.close()
            self.window.iconbitmap(icon_file_name)

        # Window
        self.window.title('Input Dialog')
        self.window.configure(bg="#E5E5E5")
        self.wh = self.window.winfo_screenheight() * 0.28  # 視窗高度
        self.ww = self.wh * 1.6  # 視窗寬度
        self.wx = (self.window.winfo_screenwidth() - self.ww) / 2
        self.wy = (self.window.winfo_screenheight() - self.wh) / 2
        self.window.geometry('%dx%d+%d+%d' % (self.ww, self.wh, self.wx, self.wy))
        self.window.focus_force()

        # Canvas
        bg_w = 640  # 寬度基數
        bg_h = 400  # 高度基數
        self.scale = min(float(self.ww) / bg_w, float(self.wh) / bg_h)  # 自適應分辨率縮放比例
        self.cw = int(bg_w * self.scale)  # 畫布寬度
        self.ch = int(bg_h * self.scale)  # 畫布高度
        self.cx = (self.ww - self.cw) * 0.5  # 畫布x座標
        self.cy = (self.wh - self.ch) * 0.5  # 畫布y座標

        # 創建畫布
        self.canvas = Canvas(self.window, width=self.cw, height=self.ch, highlightthickness=0)
        self.canvas.place(x=self.cx, y=self.cy)

    # 初始化UI
    def UI_init(self):
        # 外框
        self.round_rectangle(x=20, y=20, w=600, h=360, r=20, fill='#FFFFFF', shadow_stytle='bg')

        # 顯示文字
        text = fill(self.text, 25)  # 超過25個字自動換行
        try:
            text = text.decode('big5')
        except Exception:
            pass
        self.canvas.create_text(
            320 * self.scale,
            80 * self.scale,
            anchor='center',
            text=text,
            fill='#333333',
            font=('Consolas', int(30 * self.scale))
        )

        # 輸入框
        self.round_rectangle(
            x=100,
            y=140,
            w=440,
            h=80,
            r=20,
            fill='#E5E5E5'
        )

        self.input_value = StringVar()
        self.entry = Entry(
            master=self.window,
            bd=0,
            bg='#E5E5E5',
            font=('Consolas', int(-40 * self.scale)),
            textvariable=self.input_value
        )
        self.entry.place(
            x=self.cx + 110 * self.scale,
            y=self.cy + 150 * self.scale,
            width=int(420 * self.scale),
            height=int(60 * self.scale)
        )

        self.entry.focus()  # 焦點移至輸入框

        # enter按鈕
        self.bt_enter_img = self.image_process('enter_img')
        self.bt_enter_img_hover = self.image_process('enter_hover_img')

        self.bt_enter = Button(
            master=self.window,
            image=self.bt_enter_img,
            borderwidth=2 * self.scale,
            relief="flat",
            command=self.enter_button_click
        )
        self.bt_enter.place(
            x=self.cx + 245 * self.scale,
            y=self.cy + 240 * self.scale,
            width=self.bt_enter_img.width(),
            height=self.bt_enter_img.height()
        )

        # enter鍵hover樣式
        def bt_enter_enter(event):
            if self.bt_enter['state'] == 'normal':
                self.bt_enter['image'] = self.bt_enter_img_hover

        def bt_enter_leave(event):
            self.bt_enter['image'] = self.bt_enter_img

        self.bt_enter.bind('<Enter>', bt_enter_enter)
        self.bt_enter.bind('<Leave>', bt_enter_leave)

        # error文字
        self.error_code = self.canvas.create_text(
            320 * self.scale,
            350 * self.scale,
            anchor='center',
            text='',
            fill='#FF3333',
            font=('Consolas', int(24 * self.scale))
        )

    # enter按鈕按下
    def enter_button_click(self, event=''):
        if self.check_way == 'opid':
            if len(self.input_value.get()) != 8:  # 是否有8碼
                self.canvas.itemconfig(self.error_code, text='OPID should be 8 bits!')
                return
            elif not self.input_value.get().isdigit() and not self.input_value.get() == "ZZZZZZZZ":  # 是否皆為數字
                self.canvas.itemconfig(self.error_code, text='OPID should be numbers!')
                return
            elif not self.input_value.get() == "ZZZZZZZZ":
                # 計算是否符合OPID規則(前三碼為民國，四五碼為月份)
                id = self.input_value.get()
                date = id[:5]
                date = int(date)
                date_now = datetime.date.today()
                date_now = date_now.strftime("%Y%m")
                date_now = int(date_now)
                date_now = date_now-191100
                month = int(id[3:5])
                if date >= date_now or not 1 <= month <= 12:
                    self.canvas.itemconfig(self.error_code, text='Invalid! Enter your OPID!')
                    return
        elif self.check_way == 'sn':
            if len(self.input_value.get()) == 0:
                self.canvas.itemconfig(self.error_code, text='S/N can not be empty!')
                return
        elif self.check_way == 'csn':
            if len(self.input_value.get()) == 0:
                self.canvas.itemconfig(self.error_code, text='CSN can not be empty!')
                return
            elif len(self.input_value.get()) != 14:  # 是否有14碼
                self.canvas.itemconfig(self.error_code, text='CSN should be 14 bits!')
                return
            elif "C045" not in self.input_value.get():
                self.canvas.itemconfig(self.error_code, text='CSN format is wrong!')
                return
        elif self.check_way == 'value':
            if not self.input_value.get().replace(".", "").isdigit():
                self.canvas.itemconfig(self.error_code, text='Enter numbers only!')
                return
        stdout.write(self.input_value.get())
        self.window.destroy()

    # 綁定事件
    def bind_events(self):
        # Enter鍵
        self.window.bind('<Return>', self.enter_button_click)

        # OPID
        if self.check_way == 'opid':
            self.input_value.trace('w', self.opid_check)
            # 按下Z自動填入ZZZZZZZZ
            self.window.bind('<Key-z>', self.opid_zzzzzzzz)
            self.window.bind('<Key-Z>', self.opid_zzzzzzzz)

        # S/N
        if self.check_way == 'sn':
            self.input_value.trace('w', self.sn_check)
            # 按下Z自動填入ZZ99999
            self.window.bind('<Key-z>', self.sn_zz99999)
            self.window.bind('<Key-Z>', self.sn_zz99999)

    # check way == opid
    def opid_check(self, *event):
        self.input_value.set(self.input_value.get().upper()[:8])
        self.canvas.itemconfig(self.error_code, text='')

    # check way == sn
    def sn_check(self, *event):
        self.input_value.set(self.input_value.get().upper())
        self.canvas.itemconfig(self.error_code, text='')

    # 自動填入ZZ99999
    def sn_zz99999(self, event):
        if len(self.input_value.get()) == 1:
            self.input_value.set("ZZ99999")
            self.entry.icursor(7)

    # 自動填入ZZZZZZZZ
    def opid_zzzzzzzz(self, event):
        if len(self.input_value.get()) == 1:
            self.input_value.set("ZZZZZZZZ")
            self.entry.icursor(8)


enter_img = b'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'
enter_hover_img = b'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'
quanta_icon_ico = b'AAABAAEAQEAAAAEAIAAoQgAAFgAAACgAAABAAAAAgAAAAAEAIAAAAAAAAEAAAAAAAAAAAAAAAAAAAAAAAAD////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////+/v3//////////////////////////////////////////////////////////////////////////////////////////////////v7///n5/v/29f7/9fT+//X0/v/z8v7/8vH+//Lx/v/y8f7/8vH+//Lx/v/y8f7/8vH+//r6//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////jy7v/r2s3/3L+q/86lh//Dkm7/xJNv//Tr5f///////////////////////////////////////////////////////////////////////f3//+bk/P+/uvj/lY7z/3Jn7/9dUO3/VEfs/1NG7P9QQ+z/TD/r/0k86/9JPOv/STzr/0k86/9JPOv/STzr/01A7P/BvPj////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////69vP/5c6+/8iZd/+vbDv/oFAV/5lEBf+WPwD/lTwA/6BRF//u4Nb////////////////////////////////////////////////////////////08/7/vLf3/3Np7/88Lur/HQzm/xEA5f8OAOX/DgDl/w8A5f8PAOX/DwDl/w8A5f8PAOX/DwDl/w8A5f8PAOX/DwDl/w8A5f8UA+X/raf2//////////////////////////////////////////////////////////////////////////////////////////////////////////////////n08P/avKX/tHZI/51LD/+WPgD/lj4A/5Y/AP+XQAD/l0AA/5Y/AP+iVBv/7+HX//////////////////////////////////////////////////j4/v+4s/f/Wk/t/x4O5v8PAOX/DwDl/xEA5f8RAOX/EQDl/xEA5f8RAOX/EQDl/xEA5f8RAOX/EQDl/xEA5f8RAOX/EQDl/xEA5f8RAOX/Fgbl/66o9v///////////////////////////////////////////////////////////////////////////////////////////////////////v38/+TNvf+2eUz/mkYI/5Y9AP+XPwD/l0AA/5dAAP+XQAD/l0AA/5dAAP+WPwD/olQb/+/h1////////////////////////////////////////////97b+/9xZu//Hg7m/w8A5f8RAOX/EgHl/xIB5f8SAeX/EgHl/xIB5f8SAeX/EgHl/xIB5f8SAeX/EgHl/xIB5f8SAeX/EgHl/xIB5f8SAeX/EQDl/xYG5f+uqPb/////////////////////////////////////////////////////////////////////////////////////////////////9/Hs/8uff/+gUBb/lj4A/5c/AP+XQAD/l0AA/5dAAP+XQAD/l0AA/5dAAP+XQAD/lj8A/6JUG//v4df//////////////////////////////////v7+/8C79/8/Mur/EADl/xAA5f8RAOX/EQDl/xEA5f8RAOX/EQDl/xEA5f8RAOX/EQDl/xEA5f8RAOX/EQDl/xEA5f8RAOX/EQDl/xEA5f8RAOX/EQDl/xEA5f8WBuX/rqj2////////////////////////////////////////////////////////////////////////////////////////////8OPa/7l+U/+YQQL/lj8A/5dAAP+XQAD/l0AA/5dAAP+XQAD/l0AA/5dAAP+XQAD/l0AA/5Y/AP+iVBv/7+HX//////////////////////////////////j2/f+yrfb/lI3z/5eQ9P+XkPT/l5D0/5eQ9P+XkPT/l5D0/5eQ9P+XkPT/l5D0/5eQ9P+XkPT/l5D0/5eQ9P+XkPT/l5D0/5eQ9P+XkPT/l5D0/5eQ9P+XkPT/mZH0/9vZ+///////////////////////////////////////////////////////////////////////////////////////7NzR/69tPP+WPgD/l0AA/5dAAP+XQAD/l0AA/5dAAP+XQAD/l0AA/5dAAP+XQAD/l0AA/5Y/AP+VPAD/oFEX/+7g1v//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////7d/U/65rOf+WPgD/l0AA/5dAAP+XQAD/l0AA/5dAAP+XQAD/l0AA/5dAAP+WPgD/lj4A/5tHCv+kWCH/rWk3/7yEW//06uT/////////////////9/b9/7ex9/+jnPX/pJ31/6Sd9f+knfX/oZr1/5+Y9P+fmPT/n5j0/56X9P+blPT/mZH0/5mR9P+YkfT/mJD0/5iQ9P+YkPT/mJD0/5iQ9P+YkPT/mJD0/5iQ9P+YkPT/mJD0/5iQ9P+akvT/29j7////////////////////////////////////////////////////////////////////////////9Orj/7NzRP+WPgD/l0AA/5dAAP+XQAD/l0AA/5dAAP+XQAD/l0AA/5Y+AP+YQgP/qmIu/8eXdf/hyLb/8eTc//jz7//8+ff///7+/////////////f3//5aO8/8cC+b/EgLl/xMC5f8TAuX/EwLl/xMC5f8TAuX/EwLl/xMC5f8TAuX/EgLl/xEB5f8RAeX/EQDl/xEA5f8RAOX/EQDl/xEA5f8RAOX/EQDl/xEA5f8RAOX/EQDl/xEA5f8RAOX/FQXl/62n9v//////////////////////////////////////////////////////////////////////+/j2/8KOaf+XPwD/l0AA/5dAAP+XQAD/l0AA/5dAAP+XQAD/lz8A/5c/AP+qYi7/062T//Pq4////////////////////////////////////////////765+P8lFef/EADl/xEB5f8RAeX/EQHl/xEB5f8RAeX/EQHl/xEB5f8RAeX/EQHl/xEB5f8RAeX/EQHl/xEB5f8RAeX/EQHl/xEB5f8RAeX/EQHl/xEB5f8RAeX/EQHl/xEB5f8RAeX/EQDl/xYG5f+uqPb//////////////////////////////////////////////////////////////////////9i2n/+bRwr/lz8A/5dAAP+XQAD/l0AA/5dAAP+XQAD/lj8A/5pGCP/BjWf/8eXc/////////////////////////////////////////////////+3r/f9QQ+z/DgDl/xEB5f8RAeX/EQHl/xEB5f8RAeX/EQHl/xEB5f8RAeX/EQHl/xEB5f8RAeX/EQHl/xEB5f8RAeX/EQHl/xEB5f8RAeX/EQHl/xEB5f8RAeX/EQHl/xEB5f8RAeX/EQHl/xEA5f8WBuX/rqj2//////////////////////////////////////////////////////////////////Dj2v+pYCv/lj4A/5dAAP+XQAD/l0AA/5dAAP+XQAD/lj8A/51LD//PqIr/+/j2//////////////////////////////////////////////////////+dlfP/EwLl/w4A5f8PAOX/DwDl/w8A5f8PAOX/DwDl/w8A5f8PAOX/DwDl/w8A5f8PAOX/DwDl/w8A5f8PAOX/DwDl/w8A5f8PAOX/DwDl/w8A5f8PAOX/DwDl/w8A5f8PAOX/DwDl/w8A5f8PAOX/EwPl/62n9v////////////////////////////////////////////////////////////7+/v/Imnj/lz8A/5dAAP+XQAD/l0AA/5dAAP+XQAD/lz8A/5tIC//SrJH//v38///////////////////////////////////////////////////////19P7/eG7w/0U36/9IOuv/SDrr/0g66/9IOuv/SDrr/0g66/9IOuv/SDrr/0g66/9IOuv/SDrr/0g66/9IOuv/SDrr/0g66/9IOuv/SDrr/0g66/9IOuv/SDrr/0g66/9IOuv/SDrr/0g66/9IOuv/SDrr/0w/6//Cvfj////////////////////////////////////////////////////////////u39T/pFcf/5Y+AP+XQAD/l0AA/5dAAP+XQAD/l0AA/5hBAf/GlnT//fr5//////////////////////////////////////////////////////////////////Tz/v/z8v7/8/L+//Py/v/z8v7/8/L+//Py/v/z8v7/8/L+//Py/v/z8v7/8/L+//Py/v/z8v7/8/L+//Py/v/z8v7/8/L+//Py/v/z8v7/8/L+//Py/v/z8v7/8/L+//Py/v/z8v7/8/L+//Py/v/z8v7/+/v+////////////////////////////////////////////////////////////zaOF/5dAAP+XQAD/l0AA/5dAAP+XQAD/l0AA/5Y+AP+wbj7/9ezm/////////////////////////////////////////////////////////////Pz+/9/d+//X1Pv/2NX7/9jV+//Y1fv/2NX7/9jV+//Y1fv/2NX7/9jV+//Y1fv/2NX7/9jV+//Y1fv/2NX7/9jV+//Y1fv/2NX7/9jV+//Y1fv/2NX7/9jV+//Y1fv/2NX7/9jV+//Y1fv/2NX7/9jV+//Y1fv/2db7//Hw/v//////////////////////////////////////////////////////9/Hs/69rOv+WPgD/l0AA/5dAAP+XQAD/l0AA/5c/AP+cSAz/3sKu/////////////////////////////////////////////////////////////////9TQ+v87Len/Jhfn/ygY5/8oGOf/KBjn/ygY5/8oGOf/KBjn/ygY5/8oGOf/KBjn/ygY5/8oGOf/KBjn/ygY5/8oGOf/KBjn/ygY5/8oGOf/KBjn/ygY5/8oGOf/KBjn/ygY5/8oGOf/KBjn/ygY5/8oGOf/Jxjn/ywd6P+1sPf//////////////////////////////////////////////////////+bRwv+dSxD/lz8A/5dAAP+XQAD/l0AA/5dAAP+WPQD/tnhL//r28v////////////////////////////////////////////////////////////////+RifP/EADl/xAA5f8QAOX/EADl/xAA5f8QAOX/EADl/xAA5f8QAOX/EADl/xAA5f8QAOX/EADl/xAA5f8QAOX/EADl/xAA5f8QAOX/EADl/xAA5f8QAOX/EADl/xAA5f8QAOX/EADl/xAA5f8QAOX/EADl/xAA5f8VBOX/raf2///////////////////////////////////////////////////////QqYz/l0AA/5dAAP+XQAD/l0AA/5dAAP+XQAD/mEIE/9e1nf/////////////////////////////////////////////////////////////////4+P7/XFHt/w4A5f8SAeX/EgHl/xIB5f8SAeX/EgHl/xIB5f8SAeX/EgHl/xIB5f8SAeX/EgHl/xIB5f8SAeX/EgHl/xIB5f8SAeX/EgHl/xIB5f8SAeX/EgHl/xIB5f8SAeX/EgHl/xIB5f8SAeX/EgHl/xIB5f8RAOX/Fgbl/66o9v/////////////////////////////////////////////////+/fz/vYZe/5U9AP+XQAD/l0AA/5dAAP+XQAD/lj8A/6NWHv/u4Nb/////////////////////////////////////////////////////////////////6ef9/zst6v8OAOX/EQDl/xEA5f8RAOX/EQDl/xEA5f8RAOX/EQDl/xEA5f8RAOX/EQDl/xEA5f8RAOX/EQDl/xEA5f8RAOX/EQDl/xEA5f8RAOX/EQDl/xEA5f8RAOX/EQDl/xEA5f8RAOX/EQDl/xEA5f8RAOX/EQDl/xYF5f+uqPb/////////////////////////////////////////////////+fTx/69tPf+WPQD/l0AA/5dAAP+XQAD/l0AA/5Y9AP+ycUL/+vbz/////////////////////////////////////////////////////////////////+Hf/P82KOn/GAjm/xoK5v8aCub/Ggrm/xoK5v8aCub/Ggrm/xoK5v8aCub/Ggrm/xoK5v8aCub/Ggrm/xoK5v8aCub/Ggrm/xoK5v8aCub/Ggrm/xoK5v8aCub/Ggrm/xoK5v8aCub/Ggrm/xoK5v8aCub/Ggrm/xoK5v8fD+b/sqz2//////////////////////////////////////////////////Tq4/+nXij/lj4A/5dAAP+XQAD/l0AA/5dAAP+VPQD/v4pj//7+/f/////////////////////////////////////////////////////////////////29f7/w774/7u29/+7tvf/u7b3/7u29/+7tvf/u7b3/7u29/+7tvf/u7b3/7u29/+7tvf/u7b3/7u29/+7tvf/u7b3/7u29/+7tvf/u7b3/7u29/+7tvf/u7b3/7u29/+7tvf/u7b3/7u29/+7tvf/u7b3/7u29/+7tvf/vbj4/+jm/P/////////////////////////////////////////////////w5Nv/o1Ye/5Y/AP+XQAD/l0AA/5dAAP+XQAD/lj4A/8iZd///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////7t/V/6FTGv+WPwD/l0AA/5dAAP+XQAD/l0AA/5Y+AP/MoYL///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////jz7//bvKX/1rOa/9a0mv/WtJr/1rSa/9azmv/XtZz/8OPa/////////////////////////////////////////////////////////////////////////////////////////////////+/i2f+iVRz/lj8A/5dAAP+XQAD/l0AA/5dAAP+WPQD/x5d1///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////r2s7/oVEY/5dAAP+YQQL/mEEC/5hBAv+YQQH/mUMF/9q6o//////////////////////////////////////////////////////////////////////////////////////////////////y59//pVkj/5Y+AP+XQAD/l0AA/5dAAP+XQAD/lT0A/76IYP/+/f3/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////48y7/5tIC/+XPwD/l0AA/5dAAP+XQAD/l0AA/5pFB//fw7D/////////////////////////////////////////////////////////////////////////////////////////////////9/Dr/6xnNf+WPgD/l0AA/5dAAP+XQAD/l0AA/5Y9AP+wbj7/+fTx/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////9azmv+YQQL/l0AA/5dAAP+XQAD/l0AA/5c/AP+dSg7/5tLD//////////////////////////////////////////////////////////////////////////////////////////////////z5+P+3ek7/lT0A/5dAAP+XQAD/l0AA/5dAAP+WPwD/olMa/+3d0v////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////7+/f/BjWj/lj4A/5dAAP+XQAD/l0AA/5dAAP+WPwD/o1Ye//Dj2v//////////////////////////////////////////////////////////////////////////////////////////////////////x5l3/5Y+AP+XQAD/l0AA/5dAAP+XQAD/l0AA/5hBAv/TrpT////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////06uP/qWEs/5Y+AP+XQAD/l0AA/5dAAP+XQAD/lj4A/7BuPv/59PD//////////////////////////////////////////////////////////////////////////////////////////////////////93BrP+aRQf/l0AA/5dAAP+XQAD/l0AA/5dAAP+WPgD/sXBA//jz7///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////2Lih/5lEBv+XQAD/l0AA/5dAAP+XQAD/l0AA/5Y+AP/FlHH////////////////////////////////////////////////////////////////////////////////////////////////////////////x5d3/pVok/5Y+AP+XQAD/l0AA/5dAAP+XQAD/lz8A/5tGCf/bvKb/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////+PHt/7JyQ/+WPgD/l0AA/5dAAP+XQAD/l0AA/5dAAP+aRQf/3cGt/////////////////////////////////////////////////////////////////////////////////////////////////////////////fz7/76IYf+WPQD/l0AA/5dAAP+XQAD/l0AA/5dAAP+WPgD/rWk3//Pp4v///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////9Kskf+ZRAX/l0AA/5dAAP+XQAD/l0AA/5dAAP+WPgD/qmMv//Tr5f/////////////////////////////////////////////////////////////////////////////////////////////////////////////////hx7X/nEkN/5c/AP+XQAD/l0AA/5dAAP+XQAD/l0AA/5dAAP/Cj2r/+/j2/////////////////////////////////////////////////////////////////////////////////////////////////////////////////+bRwv+jVh7/lj8A/5dAAP+XQAD/l0AA/5dAAP+XQAD/lj8A/8qefv//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////+vbz/7d6Tv+VPgD/l0AA/5dAAP+XQAD/l0AA/5dAAP+XPwD/mkYI/8yhg//8+vj//////////////////////////////////////////////////////////////////////////////////////////////////////+3e1P+taDb/lj4A/5dAAP+XQAD/l0AA/5dAAP+XQAD/lj4A/6RXIP/t3tP////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////gxrP/nUoO/5Y/AP+XQAD/l0AA/5dAAP+XQAD/l0AA/5Y/AP+bRwn/y5+A//r18v///////////////////////////////////////////////////////////////////////////////////////////+nXyv+vazr/lj8A/5dAAP+XQAD/l0AA/5dAAP+XQAD/l0AA/5dAAP/JnHz///7+/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////Pr4/8GMZv+WPwD/l0AA/5dAAP+XQAD/l0AA/5dAAP+XQAD/lz8A/5lEBv+9hVz/7uDW////////////////////////////////////////////////////////////////////////////+/n2/9q7pP+nXSf/lj4A/5dAAP+XQAD/l0AA/5dAAP+XQAD/l0AA/5Y+AP+taDb/8+nh///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////w49r/q2Uy/5Y+AP+XQAD/l0AA/5dAAP+XQAD/l0AA/5dAAP+XPwD/lj8A/6deKP/Pp4v/8ebe///+/v/////////////////////////////////////////////////79/X/5c++/7yDWv+cSAv/lj4A/5dAAP+XQAD/l0AA/5dAAP+XQAD/l0AA/5Y/AP+eTRP/38Sx/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////+HItv+hUhn/lj4A/5dAAP+XQAD/l0AA/5dAAP+XQAD/l0AA/5dAAP+WPgD/mEEC/6deKf/Ekm7/3sKu/+7f1f/27+r/+vXy//r28//59PH/9Ork/+jVx//TrpP/tnlM/55MEf+WPgD/lz8A/5dAAP+XQAD/l0AA/5dAAP+XQAD/l0AA/5c/AP+ZQwX/zaOE//79/P//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////1rSc/51KDv+WPwD/l0AA/5dAAP+XQAD/l0AA/5dAAP+XQAD/l0AA/5dAAP+WPgD/lj4A/5pFB/+iVBv/q2Qw/7BtPv+wbj//rmo6/6deKf+eTRL/l0EB/5Y+AP+XPwD/l0AA/5dAAP+XQAD/l0AA/5dAAP+XQAD/l0AA/5c/AP+YQgL/wo9q//r28v////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////38+//TrZL/nUsQ/5Y+AP+XQAD/l0AA/5dAAP+XQAD/l0AA/5dAAP+XQAD/l0AA/5dAAP+XQAD/lj8A/5Y+AP+WPQD/lj0A/5Y+AP+WPgD/lz8A/5dAAP+XQAD/l0AA/5dAAP+XQAD/l0AA/5dAAP+XQAD/l0AA/5Y/AP+YQgP/wY1n//jy7v///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////v38/9i3oP+iVR3/lj4A/5dAAP+XQAD/l0AA/5dAAP+XQAD/l0AA/5dAAP+XQAD/l0AA/5dAAP+XQAD/l0AA/5dAAP+XQAD/l0AA/5dAAP+XQAD/l0AA/5dAAP+XQAD/l0AA/5dAAP+XQAD/l0AA/5Y+AP+bRwr/x5d1//n08P//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////5c+//69sPP+XQAD/lj8A/5dAAP+XQAD/l0AA/5dAAP+XQAD/l0AA/5dAAP+XQAD/l0AA/5dAAP+XQAD/l0AA/5dAAP+XQAD/l0AA/5dAAP+XQAD/l0AA/5dAAP+XQAD/lz8A/5Y+AP+kWSH/1rSb//z6+P/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////06uP/yJl4/6FTGf+WPgD/lj8A/5dAAP+XQAD/l0AA/5dAAP+XQAD/l0AA/5dAAP+XQAD/l0AA/5dAAP+XQAD/l0AA/5dAAP+XQAD/l0AA/5dAAP+XPwD/lj0A/5xIC/+7glj/6tjM//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////79/f/o1cj/v4pj/6FTGv+XQAD/lj0A/5Y/AP+XQAD/l0AA/5dAAP+XQAD/l0AA/5dAAP+XQAD/l0AA/5dAAP+XQAD/lz8A/5Y+AP+WPgD/nUsP/7Z5TP/ew6//+/f0//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////37+v/r28//zaSF/7JxQv+gURf/mEIE/5Y+AP+VPQD/lT0A/5U9AP+WPQD/lT0A/5U9AP+WPQD/l0AB/51LD/+rZTL/xZNw/+TNvf/69vP////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////59fH/69vP/9m5of/Imnn/vYVd/7V2Sv+xcUH/sG4+/7N0Rv+6f1X/xZVx/9Swlv/m0cL/9u7p///+/v////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////79/P/8+ff/+vbz//n08f/7+Pb//fv6////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA='

if __name__ == '__main__':
    app = InputDialog()
