# -*- coding:utf-8 -*-
import file_os
import os
import sqlite3
import sqlites          #sqlite类（包含对数据的增加和获取）
from tkinter import  *
from tkinter import messagebox
from tkinter import filedialog  #日志
import login_register       #用户登录注册
import time

uid = -1
user_name = ''
sql = sqlites.sqlite()

def main_1():   #主函数调用函数
    global uid
    global user_name
    login_register.win_init()
    if login_register.init:
        uid = login_register.uid
        user_name = login_register.user_name
        print('uid: %d' % uid)
        print('username: %s' % user_name)
        mains()

def insert(filename, num):  #自动读取文件数据并插入到数据库中
    global sql
    data = file_os.readfile(filename, num)
    if data:
        sql.insert_class(uid, data, num)
        sql.sqlite_insert()



def insert_input(): #主页“插入数据”函数
    inserts = Tk(className="插入数据")
    inserts.wm_attributes('-topmost', 1)
    user_height = inserts.winfo_screenheight()
    user_width = inserts.winfo_screenwidth()
    inserts.geometry('400x150+%d+%d' % ((user_width-400)/2, (user_height-150)/2))
    Label(inserts, text='插入数据').grid(row=0, column=0, columnspan=2)
    Label(inserts, text='请选择需要读取文件：').grid(row=1, column=0)
    path = Entry(inserts)
    path.grid(row=1, column=1)
    def huoqu():
        path.insert(0,'%s' % filedialog.askopenfilename())
    gets = Button(inserts, text='...', width=5, command=huoqu)
    gets.grid(row=1, column=2)
    Label(inserts, text='请输入文件内的数据总个数：').grid(row=2, column=0)
    num = Entry(inserts)
    num.grid(row=2, column=1)
    def tijiao():
        insert(path.get(), int(num.get()))
        inserts.destroy()
    submit = Button(inserts, text='提交', width=20, command=tijiao)
    submit.grid(row=3, column=0)
    inserts.mainloop()







def mains():
    wins = Tk(className="数据快查")  # 创建窗口类
    user_height = wins.winfo_screenheight()
    user_width = wins.winfo_screenwidth()
    wins.geometry('%dx%d' % ((user_width), (user_height)))
    Label(wins, text="数据快查").grid(row=0, column=0, columnspan=6, padx=500, pady=20)
    Label(wins,text="欢迎你！%s" % user_name,anchor="e").grid(row=1,column=0, padx=500, pady=20)
    inserts = Button(wins, text='插入数据', width=60, command=insert_input)
    inserts.grid(row=2, column=0, padx=500, pady=20)
    def data_look_form():  # 数据查看（表格）
        wins.destroy()
        global sql
        if sql.sqlite_select():
            sql.sqlite_look()
            while sqlites.is_close:
                pass
            mains()

    def data_look_pic():  # 数据查看（图）
        wins.destroy()
        new_win = Tk()
        new_win.title("请选择数据范围")
        user_height = new_win.winfo_screenheight()
        user_width = new_win.winfo_screenwidth()
        new_win.geometry('600x150+%d+%d' % ((user_width - 600) / 2, (user_height - 150) / 2))
        Label(new_win, text='反应釜编号：').grid(row=0, column=0, columnspan=2)
        code = ttk.Combobox(new_win,width=5)
        code['value'] = sqlites.codes
        code.grid(row=0, column=2)
        Label(new_win, text='开始日期（年-月-日 时:分:秒）：').grid(row=1, column=0, columnspan=2)
        begin_year = ttk.Combobox(new_win,width=5)
        begin_year['value'] = sqlites.year
        begin_year.current(8)
        begin_year.grid(row=1, column=2)
        begin_month = ttk.Combobox(new_win,width=5)
        begin_month['value'] = sqlites.date[1:12]
        begin_month.grid(row=1, column=3)
        begin_day = ttk.Combobox(new_win,width=5)
        if begin_month.get() in ('1', '3', '5', '7', '8', '10', '12'):
            begin_day['value'] = sqlites.date[1:31]
        elif begin_month.get() == '2':  # 判断是闰年还是平年
            if (int(begin_year.get()) % 4) == 0:
                if (int(begin_year.get()) % 100) == 0:
                    if (int(begin_year.get()) % 400) == 0:
                        begin_day['value'] = sqlites.date[1:29]
                    else:
                        begin_day['value'] = sqlites.date[1:28]
                else:
                    begin_day['value'] = sqlites.date[1:29]
            else:
                begin_day['value'] = sqlites.date[1:28]
        else:
            begin_day['value'] = sqlites.date[1:30]
        begin_day.grid(row=1, column=4)
        begin_hour = ttk.Combobox(new_win,width=5)
        begin_hour['value'] = sqlites.date[:24]
        begin_hour.grid(row=1, column=5)
        begin_minute = ttk.Combobox(new_win,width=5)
        begin_minute['value'] = sqlites.date[:60]
        begin_minute.grid(row=1, column=6)
        begin_second = ttk.Combobox(new_win,width=5)
        begin_second['value'] = sqlites.date[:60]
        begin_second.grid(row=1, column=7)

        Label(new_win, text='结束日期（年-月-日 时:分:秒）：').grid(row=2, column=0, columnspan=2)
        end_year = ttk.Combobox(new_win,width=5)
        end_year['value'] = sqlites.year
        end_year.current(8)
        end_year.grid(row=2, column=2)
        end_month = ttk.Combobox(new_win,width=5)
        end_month['value'] = sqlites.date[1:12]
        end_month.grid(row=2, column=3)
        end_day = ttk.Combobox(new_win,width=5)
        if end_month.get() in ('1', '3', '5', '7', '8', '10', '12'):
            end_day['value'] = sqlites.date[1:31]
        elif end_month.get() == '2':  # 判断是闰年还是平年
            if (int(end_year.get()) % 4) == 0:
                if (int(end_year.get()) % 100) == 0:
                    if (int(end_year.get()) % 400) == 0:
                        end_day['value'] = sqlites.date[1:29]
                    else:
                        end_day['value'] = sqlites.date[1:28]
                else:
                    end_day['value'] = sqlites.date[1:29]
            else:
                end_day['value'] = sqlites.date[1:28]
        else:
            end_day['value'] = sqlites.date[1:30]
        end_day.grid(row=2, column=4)
        end_hour = ttk.Combobox(new_win,width=5)
        end_hour['value'] = sqlites.date[:24]
        end_hour.grid(row=2, column=5)
        end_minute = ttk.Combobox(new_win,width=5)
        end_minute['value'] = sqlites.date[:60]
        end_minute.grid(row=2, column=6)
        end_second = ttk.Combobox(new_win,width=5)
        end_second['value'] = sqlites.date[:60]
        end_second.grid(row=2, column=7)
        Label(new_win, text='查看数据类别（温度、湿度、气压）：').grid(row=3, column=0, columnspan=2)
        types = ttk.Combobox(new_win,width=5)
        types['value'] = ('温度','湿度','气压')
        types.grid(row=3, column=2)
        def submit():   #提交函数
            begin_times = begin_year.get() + '-' + begin_month.get() + '-' + begin_day.get() + ' ' \
                          + begin_hour.get() + ':' + begin_minute.get() + ':' + begin_second.get()
            end_times = end_year.get() + '-' + end_month.get() + '-' + end_day.get() + ' ' \
                        + end_hour.get() + ':' + end_minute.get() + ':' + end_second.get()
            times = [begin_times,end_times]
            conn = sqlite3.connect('test.db')
            c = conn.cursor()
            c.execute("SELECT ID,DAY,TIME_,CODE,TEM,HUM,PRE,UID FROM ALL_DATA WHERE CODE='%s'" % code.get())
            ans = c.fetchall()
            conn.commit()
            conn.close()
            data = []  # 数据列表
            is_none = True  # 判断所选时间内是否有数据
            for j in ans:
                if time.mktime(time.strptime(j[1]+' '+j[2], '%Y-%m-%d %H:%M:%S')) >= time.mktime(
                    time.strptime(times[0], '%Y-%m-%d %H:%M:%S')) and time.mktime(
                    time.strptime(j[1]+' '+j[2], '%Y-%m-%d %H:%M:%S')) <= time.mktime(
                    time.strptime(times[1], '%Y-%m-%d %H:%M:%S')):
                    is_none = False
                temp = {'day': j[1], 'time': j[2], 'code': j[3],
                        'tem': j[4], 'hum': j[5], 'pre': j[6], 'uid': j[7]}
                data.append(temp)
            if data == []:
                messagebox.showerror(title='wrong', message='数据库内无该反应釜数据！')
            elif is_none:
                messagebox.showerror(title='wrong', message='所选时间内无数据！')
            else:
                data = sqlites.sort_data(data)  #对数据按时间进行升序排序
                coding = code.get()
                typing = types.get()
                new_win.destroy()
                sqlites.sqlites_pic(data, coding, times, typing)
                while sqlites.is_close:
                    pass
                mains()

        submits = Button(new_win, text='提交', width=20, command=submit)  # command为关联函数
        submits.grid(row=5, column=0, columnspan=2)

    look_form = Button(wins, text='数据查看（表格）', width=60, command=data_look_form)
    look_form.grid(row=3, column=0, padx=500, pady=20)
    look_pic = Button(wins, text='数据查看（图）', width=60, command=data_look_pic)
    look_pic.grid(row=4, column=0, padx=500, pady=20)
    def user_logout():  #用户注销
        global uid
        global user_name
        login_register.logout()
        uid = login_register.uid
        user_name = login_register.user_name
        wins.destroy()
        main_1()    #重新调用主函数完成回到注册登录界面
    logout = Button(wins, text='注销用户', width=60, command=user_logout)  # command为关联函数
    logout.grid(row=5, column=0, padx=500, pady=20)
    wins.mainloop()


if __name__ == '__main__':
    if not os.path.exists('.\\test.db'):
        while not sqlites.sqlite_init():    #循环进行直到初始化成功
            pass
        print('初始化成功！')
    main_1()

