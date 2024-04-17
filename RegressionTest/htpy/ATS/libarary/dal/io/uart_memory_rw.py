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

