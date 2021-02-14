# -*- coding:utf-8 -*-
import sqlite3
from tkinter import messagebox
from tkinter import *
from tkinter import ttk
import matplotlib
from matplotlib import pyplot
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time

pages = 1  # 页数
is_close = True
date = []   #下拉框日期列表
year = []   #下拉框年份
for i in range(61):
    if 0<=i<=9:
        date.append('0'+str(i))
    year.append(str(2030-i))
date = tuple(date)
year = tuple(year)
codes = []  #下拉框编号
conn = sqlite3.connect('test.db')
c = conn.cursor()
c.execute("SELECT CODE FROM ALL_DATA")
anses = c.fetchall()[1:]
conn.commit()
conn.close()
for j in anses:
    codes.append(j[0])
codes = list(set(codes))
codes.sort()
codes = tuple(codes)

def sqlite_init():  #数据库初始化
    try:
        conn = sqlite3.connect('test.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE ALL_DATA
                   (ID           INT     NOT NULL,
                   DAY           TEXT    NOT NULL,
                   TIME_           TEXT    NOT NULL,
                   CODE           TEXT    NOT NULL,
                   TEM           TEXT    NOT NULL,
                   HUM            TEXT     NOT NULL,
                   PRE            TEXT     NOT NULL,
                   UID           INT        NOT NULL);''')
        c.execute("INSERT INTO ALL_DATA (ID,DAY,TIME_,CODE,TEM,HUM,PRE,UID) \
                      VALUES ( 0, '0', '0', '0', '0', '0', '0', 0);")
        c.execute('''CREATE TABLE USER
                   (UID         INT     NOT NULL ,
                   NAME         TEXT     NOT NULL,
                   PASSWORD           TEXT    NOT NULL,
                   REALNAME     TEXT    NOT NULL );''')
        c.execute("INSERT INTO USER (UID,NAME,PASSWORD,REALNAME) \
                    VALUES ( 0, 'admin', 'admin', 'controller');")
        conn.commit()
        conn.close()
    except Exception as err:
        messagebox.showerror(title='数据库初始化失败', message=err)
        return False
    else:
        messagebox.showinfo(title='successful', message='数据库初始化成功！')
        return True

def sort_data(data,type='time',sort_type='up'):
    '''
    排序函数
    :param data: 需要排序的数据
    :param type: 判断需要排序的种类: 'time' 'hum' 'tem' 'pre' 'code'
    :param sort_type: 判断需要升序（'up'）还是降序('down')
    :return: 排序后的数据
    '''
    sort_list = []
    if type == 'time':
        for i in range(len(data)):
            temp = [i, time.mktime(time.strptime(data[i]['day'] + ' ' + data[i]['time'], '%Y-%m-%d %H:%M:%S'))]    #将时间戳和序号放入
            sort_list.append(temp)
    else:
        for i in range(len(data)):
            temp = [i, float(data[i][type])]
            sort_list.append(temp)
    if sort_type == 'up':
        sort_list.sort(key=(lambda x: x[1]))
    elif sort_type == 'down':
        sort_list.sort(key=(lambda x:x[1]),reverse=True)
    else:
        return False
    new_data = []
    for i in range(len(data)):
        temp = data[sort_list[i][0]]    #用序号确定排序后的数据与原数组的对应关系
        new_data.append(temp)
    return new_data

def sqlites_pic(data, code, times, types):
    '''
        显示数据图
    :param times: ['(开始日期的)年-月-日 时:分:秒','(结束日期的)年-月-日 时:分:秒']
    :param code: 反应釜编号(字符类型)
    :param types: 温度、湿度、气压中的一个(字符类型)
    :return:
    '''
    global is_close
    is_close = False
    root = Tk()
    root.title("数据显示（图）")
    user_height = root.winfo_screenheight()
    user_width = root.winfo_screenwidth()
    root.geometry('1100x700+%d+%d' % ((user_width - 1100) / 2, (user_height -700) / 2))
    Label(root, text=' ').grid(row=0, column=0, columnspan=2)
    Label(root, text=' ').grid(row=0, column=2, columnspan=2)
    Label(root, text='数据显示（图）').grid(row=0, column=4, columnspan=2)

    def customized_function():  # 窗口关闭绑定函数
        root.destroy()
        is_close = True
    def print_pic(data_, code_, times_, types_):
        x = []
        y = []
        day = ''
        for i in data_:
            # 将原始数据的时间转化为输入数据同类型的列表对象便于做比对
            this_time = i['day'] + ' ' + i['time']
            if time.mktime(time.strptime(this_time, '%Y-%m-%d %H:%M:%S')) >= time.mktime(
                    time.strptime(times_[0], '%Y-%m-%d %H:%M:%S')):
                if time.mktime(time.strptime(this_time, '%Y-%m-%d %H:%M:%S')) > time.mktime(
                        time.strptime(times_[1], '%Y-%m-%d %H:%M:%S')):
                    # 直到时间戳大于截止日期，退出循环
                    break
                if types_ == '温度':
                    y.append(float(i['tem']))
                elif types_ == '湿度':
                    y.append(float(i['hum']))
                elif types_ == '气压':
                    y.append(float(i['pre']))
                if i['day'] != day:  # 如果日期不再是上一天的日期
                    x.append(i['day'] + ' ' + i['time'])
                else:
                    x.append(i['time'])
                day = i['day']
        x_ = range(1, len(y)+1, 1)
        # 设置图形尺寸与质量
        fig = pyplot.figure(figsize=(10, 5), dpi=100)
        a = fig.add_subplot(111)
        # 把绘制的图形显示到tkinter窗口上
        canvas_spice = FigureCanvasTkAgg(fig, root)
        canvas_spice.get_tk_widget().grid(row=1, column=0, columnspan=9)  # 放置位置
        a.clear()  # 刷新
        pyplot.xlabel('时间', size=20, fontproperties="SimSun")
        pyplot.ylabel(types_, size=20, fontproperties="SimSun")
        pyplot.title('%s反应釜的%s曲线图' % (code_, types_), size=20, fontproperties="SimSun")
        pyplot.plot(x_,y)
        pyplot.xticks(x_ ,tuple(x))
        pyplot.grid(True)  # 网格
        canvas_spice.draw()
    Label(root, text=' ').grid(row=2, column=0, columnspan=2)
    Label(root, text='当前显示的反应釜编号：%s' % code).grid(row=2, column=2, columnspan=2)
    new_code = ttk.Combobox(root,width=10)
    new_code['value'] = codes
    new_code.grid(row=2, column=4, columnspan=2)

    print_pic(data, code, times, types)

    def set_codes():  # 改变反应釜编号函数
        if new_code.get() != '':
            conn = sqlite3.connect('test.db')
            c = conn.cursor()
            c.execute("SELECT ID,DAY,TIME_,CODE,TEM,HUM,PRE,UID FROM ALL_DATA WHERE CODE='%s'" % new_code.get())
            ans = c.fetchall()
            conn.commit()
            conn.close()
            data = []  # 数据列表
            for j in ans:
                temp = {'day': j[1], 'time': j[2], 'code': j[3],
                        'tem': j[4], 'hum': j[5], 'pre': j[6], 'uid': j[7]}
                data.append(temp)
            code =  new_code.get()
            print_pic(data, new_code.get(), times, types)

    def turn_into_hum():
        print_pic(data, code, times, '湿度')

    def turn_into_tem():
        print_pic(data, code, times, '温度')

    def turn_into_pre():
        print_pic(data, code, times, '气压')

    Button(master=root, text='修改', command=set_codes, width=20).grid(row=2, column=6, columnspan=2)
    Label(root, text=' ').grid(row=3, column=0, columnspan=2)
    Button(master=root, text='湿度', command=turn_into_hum, width=20).grid(row=3, column=2, columnspan=2)
    Button(master=root, text='温度', command=turn_into_tem, width=20).grid(row=3, column=4, columnspan=2)
    Button(master=root, text='气压', command=turn_into_pre, width=20).grid(row=3, column=6, columnspan=2)
    Label(root, text='开始日期（年-月-日 时:分:秒）：').grid(row=4, column=0, columnspan=2)
    begin_year = ttk.Combobox(root,width=5)
    begin_year['value'] = year
    begin_year.current(8)
    begin_year.grid(row=4, column=2)
    begin_month = ttk.Combobox(root,width=5)
    begin_month['value'] = date[1:12]
    begin_month.grid(row=4, column=3)
    begin_day = ttk.Combobox(root,width=5)
    if begin_month.get() in ('1','3','5','7','8','10','12'):
        begin_day['value'] = date[1:31]
    elif begin_month.get() == '2':      #判断是闰年还是平年
        if (int(begin_year.get()) % 4) == 0:
            if (int(begin_year.get()) % 100) == 0:
                if (int(begin_year.get()) % 400) == 0:
                    begin_day['value'] = date[1:29]
                else:
                    begin_day['value'] = date[1:28]
            else:
                begin_day['value'] = date[1:29]
        else:
            begin_day['value'] = date[1:28]
    else:
        begin_day['value'] = date[1:30]
    begin_day.grid(row=4, column=4)
    begin_hour = ttk.Combobox(root,width=5)
    begin_hour['value'] = date[:24]
    begin_hour.grid(row=4, column=5)
    begin_minute = ttk.Combobox(root,width=5)
    begin_minute['value'] = date[:60]
    begin_minute.grid(row=4, column=6)
    begin_second = ttk.Combobox(root,width=5)
    begin_second['value'] = date[:60]
    begin_second.grid(row=4, column=7)

    Label(root, text='结束日期（年-月-日 时:分:秒）：').grid(row=5, column=0, columnspan=2)
    end_year = ttk.Combobox(root,width=5)
    end_year['value'] = year
    end_year.current(8)
    end_year.grid(row=5, column=2)
    end_month = ttk.Combobox(root,width=5)
    end_month['value'] = date[1:12]
    end_month.grid(row=5, column=3)
    end_day = ttk.Combobox(root,width=5)
    if end_month.get() in ('1', '3', '5', '7', '8', '10', '12'):
        end_day['value'] = date[1:31]
    elif end_month.get() == '2':  # 判断是闰年还是平年
        if (int(end_year.get()) % 4) == 0:
            if (int(end_year.get()) % 100) == 0:
                if (int(end_year.get()) % 400) == 0:
                    end_day['value'] = date[1:29]
                else:
                    end_day['value'] = date[1:28]
            else:
                end_day['value'] = date[1:29]
        else:
            end_day['value'] = date[1:28]
    else:
        end_day['value'] = date[1:30]
    end_day.grid(row=5, column=4)
    end_hour = ttk.Combobox(root,width=5)
    end_hour['value'] = date[:24]
    end_hour.grid(row=5, column=5)
    end_minute = ttk.Combobox(root,width=5)
    end_minute['value'] = date[:60]
    end_minute.grid(row=5, column=6)
    end_second = ttk.Combobox(root,width=5)
    end_second['value'] = date[:60]
    end_second.grid(row=5, column=7)
    def change_time():
        begin_times = begin_year.get() + '-' + begin_month.get() + '-' + begin_day.get() + ' ' \
                      + begin_hour.get() + ':' + begin_minute.get() + ':' + begin_second.get()
        end_times = end_year.get() + '-' + end_month.get() + '-' + end_day.get() + ' ' \
                    + end_hour.get() + ':' + end_minute.get() + ':' + end_second.get()
        new_times = [begin_times, end_times]
        conn = sqlite3.connect('test.db')
        c = conn.cursor()
        c.execute("SELECT ID,DAY,TIME_,CODE,TEM,HUM,PRE,UID FROM ALL_DATA WHERE CODE='%s'" % code)
        ans = c.fetchall()
        conn.commit()
        conn.close()
        new_data = []  # 数据列表
        is_none = True  # 判断所选时间内是否有数据
        for j in ans:
            if time.mktime(time.strptime(j[1] + ' ' + j[2], '%Y-%m-%d %H:%M:%S')) >= time.mktime(
                    time.strptime(new_times[0], '%Y-%m-%d %H:%M:%S')) and time.mktime(
                time.strptime(j[1] + ' ' + j[2], '%Y-%m-%d %H:%M:%S')) <= time.mktime(
                    time.strptime(new_times[1], '%Y-%m-%d %H:%M:%S')):
                is_none = False
            temp = {'day': j[1], 'time': j[2], 'code': j[3],
                    'tem': j[4], 'hum': j[5], 'pre': j[6], 'uid': j[7]}
            new_data.append(temp)
        if is_none:
            messagebox.showerror(title='wrong', message='所选时间内无数据！')
        else:
            data = new_data
            times = new_times
            print_pic(data, code, times, types)

    change_times = Button(master=root, text='修改', command=change_time, width=20)
    change_times.grid(row=5, column=8, columnspan=2)
    root.mainloop()

class sqlite:   #数据库类
    def __init__(self, uid=0, num=0, data=[]):
        #self.data = [{'day':'','time':'','code':'','tem':'','hum':'','pre':'','uid':0}]
        self.data = []
        if num != 0:
            for i in range(num):
                temp = {'day': data[i][0],'time':data[i][1],'code':data[i][2],
                         'tem':data[i][3],'hum':data[i][4],'pre':data[i][5],'uid':uid}
                self.data.append(temp)
            self.num = num
        else:
            self.num = 0
            self.data = []
        try:
            conn = sqlite3.connect('test.db')
            c = conn.cursor()
            anser = c.execute("SELECT MAX(ID) FROM  ALL_DATA").fetchall()
            self.id = anser[0][0]
            conn.commit()
            conn.close()
        except Exception as err:
            messagebox.showerror(title='数据库类初始化错误', message=err)


    def insert_class(self, uid, data, num):  # 插入数据到sqlite对象中
        for i in range(num-1):
            temp = {'day': data[i][0], 'time': data[i][1], 'code': data[i][2],
                     'tem': data[i][3], 'hum': data[i][4], 'pre': data[i][5], 'uid': uid}
            self.data.append(temp)
        self.num = num

    def sqlite_insert(self):  # 插入数据到数据库
        if self.num == 0:
            messagebox.showerror(title='数据为空', message='请先插入数据！')
            return False
        else:
            try:
                for i in self.data:
                    self.id += 1
                    conn = sqlite3.connect('test.db')
                    c = conn.cursor()
                    #print((self.id, i['day'], i['time'], i['code'], i['tem'], i['hum'], i['pre'], i['uid']))
                    c.execute("INSERT INTO ALL_DATA (ID,DAY,TIME_,CODE,TEM,HUM,PRE,UID) \
                    VALUES (%d, '%s', '%s', '%s', '%s', '%s', '%s', %d);"
                              % (self.id, i['day'], i['time'], i['code'], i['tem'], i['hum'], i['pre'], i['uid']))
                    self.data = self.data[1:]  # 利用切片删除插入后的数据
                    conn.commit()
                    conn.close()
                    self.num = 0
                    self.data = []
            except Exception as err:
                messagebox.showerror(title='插入数据错误', message=err)
                return False
            else:
                messagebox.showinfo(title='successful', message='插入数据操作完成！')
                return True

    def sqlite_select(self):  # 将数据库中的数据存入对象内
        self.num = 0
        self.data = []  # 清空对象原始数据
        try:
            conn = sqlite3.connect('test.db')
            c = conn.cursor()
            ans = c.execute("SELECT ID,DAY,TIME_,CODE,TEM,HUM,PRE,UID FROM ALL_DATA")
            ans = ans.fetchall()
            conn.commit()
            conn.close()
        except Exception as err:
            print(err)
            messagebox.showerror(title='载入数据错误', message=err)
            return False
        else:
            for j in ans:
                self.id = j[0]
                temp = {'day': j[1], 'time': j[2], 'code': j[3],
                        'tem': j[4], 'hum': j[5], 'pre': j[6], 'uid': j[7]}
                self.data.append(temp)
            self.num = self.id
            self.data = self.data[1:] #通过切片去除初始项(0, '0', '0', '0', '0', '0', '0', 0)
            self.data.reverse()
            return True

    def sqlite_look(self):    #显示数据表
        global is_close
        is_close = False
        win = Tk(className="所有数据（表）")
        user_height = win.winfo_screenheight()
        user_width = win.winfo_screenwidth()
        win.geometry('1000x700+%d+%d' % ((user_width-1000)/2, (user_height-700)/2))
        def customized_function():  #窗口关闭绑定函数
            win.destroy()
            is_close = True
        win.protocol('WM_DELETE_WINDOW', customized_function)
        if self.id != self.num:
            messagebox.showerror(title='wrong', message='原有数据未插入或未获取数据库数据，请先插入并获取数据库数据！')
            win.destroy()
        else:
            Label(win, text="日期").grid(row=0, column=0, padx=20, pady=20)
            Label(win, text="时间").grid(row=0, column=1, padx=20, pady=20)
            Label(win, text="反应釜编号").grid(row=0, column=2, padx=20, pady=20)
            Label(win, text="温度").grid(row=0, column=3, padx=20, pady=20)
            Label(win, text="湿度").grid(row=0, column=4, padx=20, pady=20)
            Label(win, text="气压").grid(row=0, column=5, padx=20, pady=20)
            Label(win, text="用户名").grid(row=0, column=6, padx=20, pady=20)
            def print_form(data,num):
                for i in range(5):
                    Label(win, text=data[i + (pages - 1) * 5]['day']).grid(row=i + 1, column=0, padx=20, pady=20)
                    Label(win, text=data[i + (pages - 1) * 5]['time']).grid(row=i + 1, column=1, padx=20, pady=20)
                    Label(win, text=data[i + (pages - 1) * 5]['code']).grid(row=i + 1, column=2, padx=20, pady=20)
                    Label(win, text=data[i + (pages - 1) * 5]['tem']).grid(row=i + 1, column=3, padx=20, pady=20)
                    Label(win, text=data[i + (pages - 1) * 5]['hum']).grid(row=i + 1, column=4, padx=20, pady=20)
                    Label(win, text=data[i + (pages - 1) * 5]['pre']).grid(row=i + 1, column=5, padx=20, pady=20)
                    conn = sqlite3.connect('test.db')
                    c = conn.cursor()
                    ans = c.execute(
                        "SELECT REALNAME FROM USER WHERE UID=%d" % data[i + (pages - 1) * 5]['uid'])
                    ans = ans.fetchall()
                    conn.commit()
                    conn.close()
                    Label(win, text=ans[0][0]).grid(row=i + 1, column=6, padx=20, pady=20)
                    if pages == int((num - 1) / 5) + 1:
                        if i == (num - 1) % 5:
                            break

            print_form(self.data, self.num) #初始化显示第一页默认数据

            def previous_page():
                global pages
                if pages == 1:
                    messagebox.showerror(title='wrong', message='当前已经是第一页了！')
                else:
                    pages -= 1
                    print_form(self.data,self.num)

            def next_page():
                global pages
                if pages == int((self.num-1)/5)+1:
                    messagebox.showerror(title='wrong', message='当前已经是最后一页了！')
                else:
                    pages += 1
                    print_form(self.data, self.num)


            '''scorllbar = Scrollbar(orient="vertical",command=win.yview)
            win.config(yscrollcommand=scorllbar.set)
            scorllbar.grid(row=3, column=2, sticky=S + W + E + N)'''
            pre_page = Button(win, text='上一页', width=15, command=previous_page)
            pre_page.grid(row=6, column=0, padx=20, pady=20)
            Label(win, text="%d/%d" % (pages,int((self.num-1)/5)+1)).grid(row=6, column=1, padx=20, pady=20)
            nex_page = Button(win, text='下一页', width=15, command=next_page)
            nex_page.grid(row=6, column=2, padx=20, pady=20)
            back = Button(win, text='返回', width=15, command=customized_function)
            back.grid(row=6, column=3, padx=20, pady=20)

            def code_sort_up():
                self.data = sort_data(self.data, 'code')
                print_form(self.data, self.num)
            def tem_sort_up():
                self.data = sort_data(self.data, 'tem')
                print_form(self.data, self.num)
            def hum_sort_up():
                self.data = sort_data(self.data, 'hum')
                print_form(self.data, self.num)
            def pre_sort_up():
                self.data = sort_data(self.data, 'pre')
                print_form(self.data, self.num)
            def code_sort_down():
                self.data = sort_data(self.data, 'code', 'down')
                print_form(self.data, self.num)
            def tem_sort_down():
                self.data = sort_data(self.data, 'tem', 'down')
                print_form(self.data, self.num)
            def hum_sort_down():
                self.data = sort_data(self.data, 'hum', 'down')
                print_form(self.data, self.num)
            def pre_sort_down():
                self.data = sort_data(self.data, 'pre', 'down')
                print_form(self.data, self.num)


            Label(win, text="排序方式：").grid(row=7, column=0, padx=20, pady=20)
            Button(master=win, text='反应釜编号（升序）', command=code_sort_up, width=20).grid(row=7, column=2)
            Button(master=win, text='温度（升序）', command=tem_sort_up, width=20).grid(row=7, column=3)
            Button(master=win, text='湿度（升序）', command=hum_sort_up, width=20).grid(row=7, column=4)
            Button(master=win, text='气压（升序）', command=pre_sort_up, width=20).grid(row=7, column=5)
            Label(win, text=" ").grid(row=8, column=0, padx=20, pady=20)
            Button(master=win, text='反应釜编号（降序）', command=code_sort_down, width=20).grid(row=8, column=2)
            Button(master=win, text='温度（降序）', command=tem_sort_down, width=20).grid(row=8, column=3)
            Button(master=win, text='湿度（降序）', command=hum_sort_down, width=20).grid(row=8, column=4)
            Button(master=win, text='气压（降序）', command=pre_sort_down, width=20).grid(row=8, column=5)
        win.mainloop()




