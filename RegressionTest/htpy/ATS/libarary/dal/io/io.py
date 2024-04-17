
import abc


class InOutInterface(metaclass=abc.ABCMeta):

    def __init__(self, config):
        self.simulated = None
        self.simulator = None
        self.sram_operation_info = {
            'api': None,
            'params': None,
            'status': None,
            'running_state': False,
        }

    def simulator_init(self):
        pass

    def connect(self):
        """
        功能：连接硬件的io
        :arg:
            None
        :return:
             None
        """
        pass

    def disconnect(self):
        """
        功能：关闭所连接的io
        :arg:
            None
        :return:
             None
        """
        pass

    def halt(self):
        pass

    def restart(self):
        pass

    def memory_read(self, address: int, num: int, hw_id: int=None):
        """
        功能：读取指定内存地址的内容
        :param address: 地址
        :param num: 字节大小
        :param hw_id: 硬件id
        :return:
        """
        pass

    def memory_write(self, address: int, data: list, hw_id: int = None):
        """
        功能：往指定内存地址写入指定数目的字节
        :param address: 地址
        :param data: 写入的数据
        :param hw_id: 硬件id
        :return:
        """
        pass


if __name__ == '__main__':
    pass