"""
UART操作的接口类：通过串口进行memory地址的写入与读取
"""

import serial
from RegressionTest.htpy.ATS.libarary.dal.io.io import *


class UartMemoryRwInterface(InOutInterface):

    def __init__(self, config):
        InOutInterface.__init__(self, config)
        self.config = config
        self.simulated = False
        port = self.config['port']
        br = self.config['波特率']
        pr = self.config['校验方式']
        st = self.config['停等位']
        timeout = 0.5
        self.serial = None
        if port is not None:
            self.serial = serial.Serial(port, br, timeout=timeout, parity=pr, stopbit=st)
        else:
            # 模拟芯片情况下
            self.simulated = True
            self.simulator_init()

    def __list_item_replace(self, input_list, item=0x7D, sub_list=[0x7D, 0x5D]):
        new_list = []
        for x in input_list:
            if x == item:
                new_list += sub_list
            else:
                new_list.append(x)
        return new_list

    def connect(self):
        pass

    def disconnect(self):
        pass

    def halt(self):
        pass

    def restart(self):
        pass

    def memory_read(self, address: int, num: int, hw_id: int=None):
        if not self.simulated:
            # [0:4] 表示操作的地址
            frame = list(address.to_bytes(4, byteorder='little'))
            # [4:5] 表示读写操作
            frame += [0]
            # [5:6] 表示代操作hw地址，考虑通过485发送的情况
            frame += [hw_id]
            # [6:8] 表示待写入的内容的长度，用2个byte表示
            frame += list(num.to_bytes(2, byteorder='little'))

            # 向将frame中的7E和7D进行替换
            frame = self.__list_item_replace(frame, 0x7D, [0x7D, 0x5D])
            frame = self.__list_item_replace(frame, 0x7E, [0x7D, 0x5E])
            frame = [0x7E] + frame + [0x7E]

            self.serial.write(frame)
            self.serial.flush()
            r_data = self.serial.read(num)
            return list(r_data)
        else:
            return self.simulator.memory_read(address, num)

    def memory_write(self, address: int, data: list, hw_id: int = None):
        if not self.simulated:
            # [0:4] 表示操作的地址
            frame = list(address.to_bytes(4, byteorder='little'))
            # [4:5] 表示读写操作
            frame += [1]
            # [5:6] 表示代操作hw地址，考虑通过485发送的情况
            frame += [hw_id]
            # [6:8] 表示待写入的内容的长度，用2个byte表示
            frame += list(len(data).to_bytes(2, byteorder='little'))
            frame += data

            # 向将frame中的7E和7D进行替换
            frame = self.__list_item_replace(frame, 0x7D, [0x7D, 0x5D])
            frame = self.__list_item_replace(frame, 0x7E, [0x7D, 0x5E])
            frame = [0x7E] + frame + [0x7E]

            self.serial.write(frame)
            self.serial.flush()


