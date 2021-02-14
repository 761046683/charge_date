# -*- coding:utf-8 -*-
from tkinter import *
from tkinter import messagebox
import sqlite3

init = False
uid = -1
user_name = ''

def win_init():
    #messagebox.showinfo( "题目", "提示") 显示提示框
    win = Tk()
    win.title('用户登录')
    user_height = win.winfo_screenheight()
    user_width = win.winfo_screenwidth()
    win.geometry('350x150+%d+%d' % ((user_width-350)/2, (user_height-150)/2))
    win.resizable(False, False)    #禁止改变大小
    win.maxsize(user_width, user_height)
    Label(win,text='用户登录').grid(row=0,column=0,columnspan=2)
    Label(win,text='用户名：').grid(row=1,column=0)
    name = Entry(win)
    name.grid(row=1,column=1)
    Label(win,text='密码：').grid(row=2,column=0)
    passwd = Entry(win,show='*')
    passwd.grid(row=2,column=1)
    def user_login():   #用户登录函数
        global uid
        global user_name
        global init
        try:
            conn = sqlite3.connect('test.db')
            c = conn.cursor()
            ans = c.execute("SELECT * FROM user WHERE NAME='%s'" % name.get())
            ans = ans.fetchall()
            count = 0
            for i in ans:
                count = count + 1
            if count == 0:
                messagebox.showerror(title='wrong', message='登录失败，用户名不存在')
            elif name.get() == ans[0][1] and passwd.get() == ans[0][2]:
                if ans[0][0] >= 0:
                    messagebox.showinfo(title='successful', message='登录成功')
                    uid = ans[0][0]
                    user_name = ans[0][3]
                    init = True
                    win.destroy()
                else:
                    messagebox.showerror(title='wrong', message='登录失败，用户id获取失败，请重试')
            else:
                messagebox.showerror(title='wrong', message='登录失败，用户名或密码错误')
            conn.commit()
            c.close()
            conn.close()
        except Exception as err:
            messagebox.showerror(title='wrong', message=err)
        else:
            pass

    def user_register():
        registered = Tk()
        registered.title('用户注册')
        registered.geometry('230x180+%d+%d' % ((user_width-230)/2, (user_height-180)/2))
        registered.resizable(False, False)    #禁止改变大小
        Label(registered, text='用户注册').grid(row=0, column=0, columnspan=2)
        Label(registered, text='用户名：').grid(row=1, column=0, sticky=E)
        names = Entry(registered)
        names.grid(row=1, column=1)
        Label(registered, text='密码：').grid(row=2, column=0, sticky=E)
        passwds = Entry(registered, show='*')
        passwds.grid(row=2, column=1)
        Label(registered, text='确认密码：').grid(row=3, column=0)
        repasswd = Entry(registered, show='*')
        repasswd.grid(row=3, column=1)
        Label(registered, text='真实姓名：').grid(row=4, column=0, sticky=E)
        real_names = Entry(registered)
        real_names.grid(row=4, column=1)

        def registeredes():
            conn = sqlite3.connect('test.db')
            c = conn.cursor()
            c.execute("SELECT * FROM USER WHERE NAME='%s'" % names.get())
            ans = c.fetchall()
            count1 = 0
            conn.commit()
            c.close()
            conn.close()
            for i in ans:
                count1 = count1 + 1
            if count1 != 0:
                messagebox.showerror(title='wrong', message='注册失败，用户名已存在')
            elif not (any([x.isdigit() for x in names.get()]) and any([x.isalpha() for x in names.get()])):
                messagebox.showerror(title='wrong', message='注册失败，用户名格式错误，必须包括字母和数字')
            elif len(passwds.get()) < 6:
                messagebox.showerror(title='wrong', message='注册失败，密码不应少于6位')
            elif passwds.get() != repasswd.get():
                messagebox.showerror(title='wrong', message='注册失败，两次密码不相同')
            elif real_names.get() == '':
                messagebox.showerror(title='wrong', message='真实姓名不能为空！')
            else:
                try:
                    conn = sqlite3.connect('test.db')
                    c = conn.cursor()
                    uid = c.execute("SELECT MAX(UID) FROM  USER")
                    uid = uid.fetchall()
                    c.execute("INSERT INTO USER (UID,NAME,PASSWORD,REALNAME) \
                            VALUES (%d, '%s', '%s', '%s');" % (uid[0][0]+1, names.get(), passwds.get(), real_names.get()))
                    messagebox.showinfo(title='successful', message='注册成功！欢迎您,新会员')
                    conn.commit()
                    conn.close()
                except Exception as err:
                    messagebox.showerror(title='wrong', message=err)
                else:
                    registered.destroy()

        Button(registered, text='注册', command=registeredes).grid(row=6, column=0, columnspan=2)
        registered.mainloop()

    login = Button(win, text='登录', width=20, command=user_login)    #command为关联函数
    login.grid(row=3, column=0)
    register = Button(win, text='注册', width=20, command=user_register)
    register.grid(row=3,column=1)
    win.mainloop()

def logout():
    global init
    global uid
    global user_name
    init = False
    uid = -1
    user_name = ''



