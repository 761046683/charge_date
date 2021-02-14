import os
from tkinter import messagebox

def readfile(filename, num):
    '''
    读取文件函数
    :param filename: 文件路径
    :param num: txt文件内的数据量个数
    :return: 文件数据二维列表  行：第几个数据  列：0-5分别是六个数据类
    '''
    try:
        fd = os.open(filename, os.O_RDONLY)
        fd_read = os.read(fd, 35 * num) #根据格式，文件数据每行占34个字符
        datas = str(fd_read)[2:].split(',')
        data = []  # 返回的列表
        for i in range(len(datas)):
            if i % 6 == 0:  # 每组数据重新定义data1数组防止append覆盖
                data1 = [0, 0, 0, 0, 0, 0]  # 每个数据的列表
            data1[i % 6] = datas[i]
            if i % 6 == 5:
                data.append(data1)
        os.close(fd)
    except Exception as err:
        messagebox.showerror(title='获取文件错误', message=err)
        return False
    else:

        return data
