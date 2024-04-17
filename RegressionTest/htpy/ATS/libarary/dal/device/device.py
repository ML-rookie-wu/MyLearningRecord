from ctypes import *

class Peripheral:
    def __init__(self):
        self.debug = False
        self.check = True
        self.chip_name = None
        self.core_name = None
        self.name = None
        self.peripheral = None
        self.addr = None
        self.instance = None
        self.register_map = {}
        self.register_inforamtion = None
        self.register_access_by_fw = None
        self.dal_handler = None
        self.hw_id = None

    def init(self, chip_name, core_name, name, peripheral_enum, instance_class):
        self.chip_name = chip_name.lower()
        self.core_name = core_name.lower()
        self.name = name.upper()
        self.peripheral_enum = peripheral_enum
        self.instance = instance_class()
        self.addr = self.get_addr()

    def set_dal_handler(self, handler):
        self.dal_handler = handler

    def get_addr(self):
        for name, member in self.peripheral_enum.__members__.items():
            if name == self.name or (name == 'PMU' and self.name in ['Reset', 'RESET']):
                return member.value

    def get_register_map(self):
        for reg, *others in self.instance._fields_:
            if len(others) == 1 and others[0] == c_uint32:
                pass
            else:
                self.register_map[reg] = self.get_register_addr_and_length_by_name(reg)
