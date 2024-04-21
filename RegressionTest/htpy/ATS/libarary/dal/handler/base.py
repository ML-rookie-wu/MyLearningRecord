import datetime
import random
from enum import Enum
from RegressionTest.htpy.ATS.libarary.dal.map_file_parse import *
from RegressionTest.htpy.ATS.libarary.dal.com_struct import *


MAX_BUF_SIZE = 1024


class TAL_RUNNING_STATE(Enum):
    Reset = 0
    CallbackSet = 1
    Hardfault = 2
    Running = 3
    Done = 4
    Init = 5
    Invalid = 0xFF

class TalCmdRsp(LittleEndianStructure):
    _pack_ = 1
    _field_ = [
        ('len', c_uint16),
        ('data', MAX_BUF_SIZE * c_uint8)
    ]


class TalCmd(LittleEndianStructure):
    _pack_ = 1
    _field_ = [
        ('api', c_uint32),
        ('params', MAX_BUF_SIZE * c_uint8),
        ('status', c_uint8),
        ('rsv', c_uint8),
        ('st', c_uint32),
        ('et', c_uint32),
        ('resp', TalCmdRsp)
    ]


class CmdStatus(Enum):
    INIT = 0
    EXEC = 1
    NA = 2


class HandlerBase:

    def __init__(self, map_file):
        self.debug = False
        self.map = MapParser(map_file)
        self.share_mem_addr = self.map.cmd_addr

        self.addr = {
            'cmd': self.share_mem_addr,
            'params': self.share_mem_addr + 4,
            'status': self.share_mem_addr + 4 + MAX_BUF_SIZE,
            'resp': self.share_mem_addr + 4 + MAX_BUF_SIZE + 10 + 2
        }

        self.api_name = None
        self.fp_map = {}
        self.simulated_data = {}
        self.io = None
        self.hw_id = None
        self.fw_api = None
        self.type_map = {
            'UINT32': UINT32,
            'UINT16': UINT16,
            'UINT8': UINT8,
            'u32': UINT32,
            'u16': UINT16,
            'u8': UINT8,
            'U32': UINT32,
            'U16': UINT16,
            'U8': UINT8,
            'u32*': UINT32_T_PRT,
            'u16*': UINT16_T_PRT,
            'u8*': UINT8_T_PRT,
        }

    def set_io(self, io):
        self.io = io

    def get_pc(self):
        print("如果是Jlink连接的需要实现这个API")

    def memory_read(self, addr, length, id=None):
        if self.debug:
            if addr not in self.simulated_data:
                print("读取地址 = {}, 返回随机数据".format(hex(addr)))
                data = []
                for i in range(0, length):
                    data.append(random.randint(0, 0xFF))
                self.simulated_data[addr] = data
            else:
                print("读取地址 = {}, 返回已有的数据".format(hex(addr)))
            return self.simulated_data[addr]
        else:
            data = self.io.memory_read(addr, length, id)
            if data is None:
                data = []
            return data

    def memory_write(self, addr, data, id=None):
        if self.debug:
            self.simulated_data[addr] = data
            return len(data)
        else:
            return self.io.memory_write(addr, data, id)

    def wait_last_api_call_done(self, to_s=3600, interval_time=60):
        pass

    def send_cmd(self, cmd, api_name=None, to_s=10, need_wait_done=True, interval_time=60):
        pass

    def call(self, api, need_wait_done=True):
        pass

    def get_status(self):
        pass

    def init_rsp(self, data=[0, 0]):
        pass

    def get_rsp(self):
        pass

    def get_var_by_name(self, name, length):
        pass

    def get_var_addr_by_name(self, name):
        pass

    def get_api_addr_by_name(self, name):
        pass

    def get_running_state(self):
        pass

    def set_running_state(self, state, max_retry=1, exit_state_list=[]):
        pass

    def recovery_callback(self):
        for fp in self.fp_map:
            f = self.fp_map[fp]["回调函数名称"]
            fp_addr = self.fp_map[fp]["函数指针地址"]
            f_addr_list = self.fp_map[fp]["回调函数地址"]
            self.memory_write(fp_addr, f_addr_list, id=self.hw_id)
            print("将函数指针{}恢复成指向函数{}".format(fp, f))

    def clean_fp(self):
        self.fp_map = {}

    def wait_for_reset(self, to_s=5):
        reset_check_pass = True
        st = datetime.datetime.now()

