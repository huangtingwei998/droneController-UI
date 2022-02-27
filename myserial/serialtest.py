#



# TODO 串口读取数据
# Auther wjw
import numpy as np
import serial  # 导入串口包
import time  # 导入时间包

from matplotlib import pyplot as plt

ser = serial.Serial("COM4",115200,timeout = 0)  # 开启com3口，波特率115200，超时5
ser.flushInput()  # 清空缓冲区

def main():
    plt.grid(True)  # 添加网格
    plt.ion()  # interactive mode
    plt.figure(1)
    plt.xlabel('times')
    plt.ylabel('data')
    plt.title('Diagram of UART data by Python')

    t = [0]
    m = [0]
    i = 0
    intdata = 0

    while True:
        if i>200:
            t = [0]
            m = [0]
            i = 0
            plt.cla()
        else:
            count = ser.inWaiting()  # 获取串口缓冲区数据
            if count != 0:
                recv = ser.read(ser.in_waiting).decode("gbk")  # 读出串口数据，数据采用gbk编码
                if recv[6].isdigit()&recv[8:12].isdigit():
                    str1 = ''.join(recv[6:12])
                    num2 = float(str1)
                    print(num2)
                    i = i + 1
                    t.append(i)
                    m.append(num2)
                    # plt.ion()
                    plt.clf()
                    plt.plot(t, m, '-r')
                    # plt.scatter(i, intdata)
                    # plt.draw()
                    # plt.ioff()
                    plt.show()
                    time.sleep(0.1)  # 延时0.1秒，免得CPU出问题


if __name__ == '__main__':
    main()
