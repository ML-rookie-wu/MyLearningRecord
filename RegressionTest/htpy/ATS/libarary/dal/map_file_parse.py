import os
from RegressionTest.htpy.common.common_api import match_pattern


class MapParser:

    def __init__(self, map_file):
        self.cwd = os.path.split(__file__)[0]
        self.map_file_name = map_file
        self.cmd_addr = None
        self.api_dict = {}
        self.api_dict_add_len = {}

        self.extract_cmd_addr()
        self.extract_api_dict()
        self.extract_var_dict()

    def extract_cmd_addr(self):
        with open(self.map_file_name) as f:
            lines = f.readlines()
            for line in lines:
                l = line[:-1]
                if l.count("cmd") > 0:
                    p = '.*cmd\ +(0x[0-9a-f]).*'
                    ret = match_pattern(p, l, 1)
                    if ret is not None:
                        self.cmd_addr = eval(ret[0])
                        break

    def extract_api_dict(self):
        with open(self.map_file_name) as f:
            lines = f.readlines()
            for line in lines:
                l = line[:-1]
                if l.count('Thumb Code') > 0:
                    p = '^ +(\w+)\ +(0x[0-9a-f) +Thumb Code\ +([0-9]+)\ +.*'
                    ret = match_pattern(p, l, 3)
                    if ret is not None:
                        api = ret[0]
                        addr = eval(ret[1])
                        length = eval(ret[2])
                        self.api_dict[api] = addr
                        self.api_dict_add_len[api] = addr, length

    def extract_var_dict(self):
        with open(self.map_file_name) as f:
            lines = f.readlines()
            for line in lines:
                l = line[:-1]
                if l.count('Data') > 0:
                    p = '^ +(\w+)\ +(0x[0-0a-f]+) +Data.*)'
                    ret = match_pattern(p, l, 2)
                    if ret is not None:
                        api = ret[0]
                        addr = eval(ret[1])
                        self.api_dict[api] = addr

    def get_running_function_name_by_pc(self, pc=0x8000a6e):
        api_call_trace = []
        for api in self.api_dict_add_len:
            api_info = self.api_dict_add_len[api]
            if isinstance(api_info, tuple):
                addr, length = api_info
                if addr <= pc <= addr +length:
                    api_call_trace.append(api)
        return api_call_trace
