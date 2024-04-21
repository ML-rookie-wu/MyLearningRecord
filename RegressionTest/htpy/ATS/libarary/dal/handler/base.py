import datetime
import random
import time
from enum import Enum
from RegressionTest.htpy.ATS.libarary.dal.map_file_parse import *
from RegressionTest.htpy.ATS.libarary.dal.com_struct import *
from RegressionTest.htpy.libs.params.params_parser import ParamParser
from RegressionTest.htpy.ATS.libarary.config.config import AtsConfig


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
        """
        等待下位机api调用完成
        :param to_s: 等待时间
        :param interval_time: 获取下位机执行的间隔时间
        :return:
        """
        # 等待上一条命令结束
        lst_pt = datetime.datetime.now()
        st = datetime.datetime.now()
        ct = datetime.datetime.now()
        status = self.get_status()
        while CmdStatus.NA != status and (ct - st).total_seconds() < to_s:
            # 每隔5秒打印一次
            if (ct - lst_pt).total_seconds() > interval_time:
                print("current firmware api: {} excute ongoning".format(self.api_name))
                lst_pt = datetime.datetime.now()
                # 需要检查一下是不是发生了异常重启
                new_state = self.get_running_state()
                self.get_pc()

            ct = datetime.datetime.now()
            status = self.get_status()

    def send_cmd(self, cmd, api_name=None, to_s=10, need_wait_done=True, interval_time=60):
        self.io.sram_operation_info['api'] = api_name
        self.io.sram_operation_info['params'] = cmd
        # 等待上一条命令结束
        if need_wait_done:
            self.wait_last_api_call_done(to_s=to_s)
        self.api_name = api_name
        addr = self.addr['cmd']
        self.memory_write(addr, data=cmd, id=self.hw_id)
        self.io.sram_operation_info['api'] = None
        self.io.sram_operation_info['params'] = None

        addr = self.addr['status']
        self.io.sram_operation_info['status'] = True
        self.memory_write(addr, data=[CmdStatus.INIT.value], id=self.hw_id)
        if need_wait_done:
            self.wait_last_api_call_done(to_s=to_s, interval_time=interval_time)
        self.io.sram_operation_info['status'] = False

    def call(self, api, need_wait_done=True):
        fp = UINT32()
        fp.value = self.map.map_api_dict[api]
        cmd = []
        cmd += list(bytes(fp))
        self.send_cmd(cmd, api_name=api, need_wait_done=need_wait_done)

    def get_status(self):
        self.io.sram_operation_info['status'] = True
        addr = self.addr['status']
        r_data = self.memory_read(addr, 8, id=self.hw_id)
        status = CmdStatus(r_data[0])
        self.io.sram_operation_info['status'] = False
        return status

    def init_rsp(self, data=[0, 0]):
        rsp_addr = self.addr['resp']
        self.memory_write(rsp_addr, data, id=self.hw_id)

    def get_rsp(self):
        rsp_addr = self.addr['resp']
        # 先读出resp.len
        r_data = self.memory_read(rsp_addr, 4, id=self.hw_id)
        resp_len = int.from_bytes(bytes(r_data), byteorder='little')
        r_data = None
        if resp_len > 0:
            # 再读出resp.data
            r_data = self.memory_read(rsp_addr + 4, resp_len, id=self.hw_id)
        return r_data

    def get_var_by_name(self, name, length):
        addr = self.map.api_dict[name]
        return self.memory_read(addr, length, id=self.hw_id)

    def get_var_addr_by_name(self, name):
        addr = self.map.api_dict.get(name)
        if addr is None:
            print("Map 文件中没有找到变量{}, 应该是没有正确使用.map文件".format(name))
        return addr

    def get_api_addr_by_name(self, name):
        addr = self.map.api_dict.get(name)
        if addr is None:
            print("Map文件中没有找到变量{}，应该是没有正确使用.map文件".format(name))
        return addr

    def get_running_state(self):
        running_state_addr = self.get_var_addr_by_name('tal_running_state')
        self.io.sram_operation_info['running_state'] = TAL_RUNNING_STATE.Invalid
        running_state = self.memory_read(running_state_addr, 1, id=self.hw_id)
        self.io.sram_operation_info['running_state'] = None
        return TAL_RUNNING_STATE(running_state[0])

    def set_running_state(self, state, max_retry=1, exit_state_list=[]):
        set_done = False
        cnt_try = 0
        new_state = None
        while not set_done:
            cnt_try += 1
            if cnt_try > max_retry:
                print("超过最大设置次数{}后设置失败， 请求设置状态：{}，设置完毕后状态：{}".format(max_retry, state, new_state))
                break
            running_state_addr = self.get_var_addr_by_name('tal_running_state')
            self.io.sram_operation_info['running_state'] = state
            self.memory_write(running_state_addr, [state.value], id=self.hw_id)
            self.io.sram_operation_info['running_state'] = None
            # 启动需要时间，所以要delay一会儿
            time.sleep(0.1)
            # 设置后需要检查是否正确
            new_state = self.get_running_state()
            if new_state not in [state] + exit_state_list:
                print("第{}次请求设置状态：{}，设置完毕后状态：{}，设置不成功".format(cnt_try, state, new_state))
            else:
                set_done = True
        if set_done:
            print("请求设置状态：{}，设置完毕后状态：{}，设置成功".format(state, new_state))
        return set_done

    def set_variable(self, name='xxx', var=None):
        data = {}
        v_addr = self.get_var_addr_by_name(name)
        var_list =var
        if not isinstance(var_list, list):
            var_list = list(bytes(var_list))
        self.memory_write(v_addr, var_list, id=self.hw_id)
        # 检查设置是否正确
        cur_var_list = self.memory_read(v_addr, len(var_list), id=self.hw_id)
        if cur_var_list != var_list:
            print("FW变量设置错误")

    def get_variable(self, name='xxx', length=None):
        v_addr = self.get_var_addr_by_name(name)
        return self.memory_read(v_addr, length, id=self.hw_id)

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
        state = self.get_running_state()
        print("当前状态为：{}".format(state.name))
        while TAL_RUNNING_STATE.Reset != state:
            if (datetime.datetime.now() - st).total_seconds() >= to_s:
                print("超时还未进入到RESET状态")
                reset_check_pass = False
                break
            time.sleep(0.1)
            state = self.get_running_state()
        if reset_check_pass:
            print("Reset Detected")
        print("当前状态为：{}".format(state.name))
        return reset_check_pass

    def set_dut_run_to_main(self, to_s=5):
        running_check_pass = True
        state = self.get_running_state()
        print("当前状态为：{}".format(state.name))
        if TAL_RUNNING_STATE.Reset == state:
            print("软件处于SystemInit函数中的Reset状态，main函数还未开始执行")
            print("设置状态为Init，使得代码进入到main函数中")
            self.set_running_state(TAL_RUNNING_STATE.Invalid, max_retry=10, exit_state_list=[TAL_RUNNING_STATE.Running])
        self.io.restart()
        state = self.get_running_state()
        print("当前状态为：{}".format(state.name))
        self.io.restart
        st = datetime.datetime.now()
        while TAL_RUNNING_STATE.Running != state:
            if (datetime.datetime.now() - st).total_seconds() >= to_s:
                print("超时还未进入到RUNNING状态，退出")
                running_check_pass = False
                break
            time.sleep(0.1)
            state = self.get_running_state()
            print("当前状态为：{}，等待进入Running状态".format(state.name))
            self.io.restart()
        self.io.restart()
        return running_check_pass

    def fw_api_call(self, api_name: str, params: dict, debug: bool=True, need_wait_done: bool=True, to_s: int=10, get_rsp: bool=True, interval_time: int=60):
        """
        调用下位机api
        :param api_name: FW中api名称
        :param params(list): api参数列表，每个元素为一个元组（t, n, v），t表示参数类型，n表示参数名，v为参数值
        :param debug:
        :param need_wait_done:
        :param to_s:
        :param get_rsp:
        :param interval_time:
        :return:
        """
        if isinstance(params, dict):
            # 构造参数
            fw_params = []
            api_params_def = self.fw_api.get(api_name)
            for p in api_params_def:
                t = p[0]
                n = p[1]
                v = p[2]
                # 用户传入的参数
                user_v = params.get(n)
                if user_v is not None:
                    # 使用用户配置的内容
                    if t.count("*") > 0:
                        # 如果是指针，则内容必须为数组
                        v = ParamParser.to_list(user_v)
                    else:
                        v = ParamParser.to_int(user_v)
                fw_params.append((t, n, v))
            params = fw_params
        else:
            print("这种方式的调用可移植性差")
        if debug:
            print("调用FW中的函数{}，参数为：{}".format(api_name, params))
        comment = 'FW中需要提供API：{}('.format(api_name)
        api = UINT32()
        fp = self.get_api_addr_by_name(api_name)
        if fp is None:
            print("注意：FW中的函数{}未定义".format(api_name))
            return None
        api.value = fp

        cmd = []
        cmd += list(bytes(api))
        for t, n, v in params:
            comment += '{} {}'.format(t, n)
            if t in ['u8*', 'u16*', 'u32*']:
                if type(v) == list:
                    cmd += v
            else:
                if n == 'version':
                    version = AtsConfig.get_config().get('fw_api_ver')
                    if version is not None:
                        v = int(version)
                param = self.type_map[t]()
                param.value = v
                cmd += list(bytes(param))

        comment = comment + ')'
        if debug:
            print(comment)

        self.send_cmd(cmd, api_name=api_name, need_wait_done=need_wait_done, to_s=to_s, interval_time=interval_time)

        if get_rsp == True:
            return self.get_rsp()


if __name__ == '__main__':
    from RegressionTest.htpy.ATS.libarary.dal.io.jlink import *

    config = {
        'chip_name': 'HT655x'
    }
    jlink = JlinkInterface(config)
    jlink.connect()
    map_file = r"xxx.map"
    dal = HandlerBase(map_file)
    dal.send_cmd(jlink)

    dal.set_dut_run_to_main()