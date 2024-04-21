import weakref



class Device:
    def __init__(self):
        self.chip_name = None
        self.core_name = None
        self.peripheral_enum = None
        self.peripheral_typedef_dict = None
        self.peripherals = {}
        self.dal_handler = None
        self.hw_id = None

    def init(self, chip_name, core_name, peripheral_enum, peripheral_typedef_dict, dal_handler):
        pass

    def set_dal_handler(self, dal_handler):
        pass

    def get_app(self, peripheral):
        pass