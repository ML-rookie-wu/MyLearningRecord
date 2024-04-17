"""
JLINK操作的接口类：通过jlink进行memory地址的写入与读取
"""

import pylink

from RegressionTest.htpy.ATS.libarary.dal.io.io import *
# from RegressionTest.htpy.common.common_log import Debug


class JlinkInterface(InOutInterface):

    def __init__(self, config: dict=None):
        InOutInterface.__init__(self, config)
        self.chip_name = config.get("chip_name")
        self.simulated = config.get("simulated")
        if self.simulated is None:
            self.simulated = True
            print('JlinkInterface simulated call __init__(config={})'.format(config))

        self.jlink = None
        if not self.simulated:
            self.jlink = pylink.JLink(use_tmpcpy=False)
            self.jlink.open()
            self.jlink.set_tif(pylink.enums.JLinkInterfaces.SWD)
        else:
            self.simulator_init()

    def __del__(self):
        if not self.simulated:
            self.jlink.close()

    def set_chip_name(self, chip_name):
        self.chip_name = chip_name

    def reset(self, halt=False):
        if not self.simulated:
            self.jlink.reset(halt=halt)
        else:
            print('JlinkInterface simulated call reset({})'.format(halt))

    def connect(self):
        if not self.simulated:
            if not self.jlink.open():
                self.jlink = pylink.JLink()
                self.jlink.open()
                self.jlink.set_tif(pylink.enums.JLinkInterfaces.SWD)
                print("open jlink")
            print('connect jlink')
            self.jlink.connect(self.chip_name)
            self.jlink.set_speed(speed=50000)

    def disconnect(self):
        if not self.simulated:
            self.jlink.close()
        else:
            print('JlinkInterface simulated call disconnect()')

    def halt(self):
        pass

    def restart(self):
        if not self.simulated:
            if self.jlink.halted():
                print("CPU处于halted状态，需要restart")
                self.jlink.halt()
                pc = self.jlink.register_read('R15 (PC)')
                print("pc = ", pc)
                x = self.jlink.restart(skip_breakpoints=True)
                print("x = ", x)
        else:
            print("simulated CPU restart")

    def memory_read(self, address: int, num: int, hw_id: int=None):
        if not self.simulated:
            return self.jlink.memory_read(address, num)
        else:
            return self.simulator.memory_read(address, num)

    def memory_write(self, address: int, data: list, hw_id: int = None):
        if not self.simulated:
            return self.jlink.memory_write(address, data)
        else:
            return self.simulator.memory_write(address, data)

    def flash_file(self, addr: int, data: list):
        if not self.simulated:
            return self.jlink.flash_file(data, addr)
        else:
            return self.simulator.flash_file(data, addr)





