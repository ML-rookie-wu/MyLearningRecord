"""
ULINK操作的接口类：通过ulink进行memory地址的写入与读取
"""

from RegressionTest.htpy.ATS.libarary.dal.io.io import *
from pyocd.core.helpers import ConnectHelper
from pyocd.flash.loader import FlashLoader
from pyocd.core.memory_map import MemoryType


class OcdInterface(InOutInterface):
    def __init__(self, config=None):
        InOutInterface.__init__(self, config)
        self.chip_name = config.get('chip_name')
        self.simulated = config.get('simulated')
        self.unique_id = config.get('unique_id')
        self.target = config.get('target')
        self.connect_mode = config.get('connect_mode')
        self.pack = config.get('pack')
        if self.simulated is None:
            self.simulated = True
            print('OcdInterface simulated call __init__(config={})'.format(config))
        self.session = None
        if not self.simulated:
            print(self.unique_id, self.target, self.connect_mode)
            self.session = ConnectHelper.session_with_chosen_probe(unique_id=self.unique_id,
                                                                   options={"frequency": 10000000,
                                                                            "target_override": self.target,
                                                                            "connect_mode": self.connect_mode,
                                                                            "pack": self.pack})
        else:
            self.simulator_init()

    def __del__(self):
        if not self.simulated:
            pass

    def set_chip_name(self, chip_name: str):
        self.chip_name = chip_name

    def reset(self, halt=False):
        if not self.simulated:
            self.session.board.target.reset()
            if halt:
                self.session.board.target.halt()
        else:
            print("OcdInterface simulated call reset!")

    def connect(self):
        pass

    def disconnect(self):
        pass

    def halt(self):
        if not self.simulated:
            with self.session:
                if not self.session.board.target.is_halted():
                    print("CPU处于running状态，需要halt！")
                    self.session.board.target.halt()

        else:
            print("simulated CPU halt")

    def restart(self):
        if not self.simulated:
            with self.session:
                if self.session.board.target.is_halted():
                    print("CPU处于halted状态，需要restart！")
                    self.session.board.target.resume()
        else:
            print("simulated CPU restart!")

    def memory_read(self, address: int, num: int, hw_id: int=None):
        if not self.simulated:
            with self.session:
                return self.session.board.target.read_memory_block8(address, num)

        else:
            return self.simulator.memory_read(address, num)

    def memory_write(self, address: int, data: list, hw_id: int = None):
        if not self.simulated:
            with self.session:
                memory_map = self.session.board.target.get_memory_map()
                for rom_region in memory_map.iter_matching_regions(type=MemoryType.RAM, is_testable=True):
                    rom_start = rom_region.start
                    rom_size = rom_region.length
                    if rom_start <= address <= rom_start + rom_size:
                        return self.session.board.target.write_memory_block8(address, data)

                return self.flash_write(data, address, hw_id)

    def flash_write(self, data: list, addr: int, id: int=None):
        if not self.simulated:
            with self.session:
                memory_map = self.session.board.target.get_memory_map()
                for rom_region in memory_map.iter_matching_regions(type=MemoryType.FLASH, is_testable=True):
                    rom_start = rom_region.start
                    rom_size = rom_region.length
                    if rom_start <= addr <= rom_start + rom_size:
                        flash = rom_region.flash
                        sector_info = flash.get_sector_info(addr)
                        if sector_info is not None:
                            # 假设一次flash操作不会超过一个sector
                            # 1. 读取这个sector中的原始内容
                            # 2. 根据addr和data修改对应的内容
                            # 3. 将修改后的内容写入sector
                            org_data = self.session.board.target.read_memory_block8(sector_info.base_addr, sector_info.size)
                            offset = addr - sector_info.base_addr
                            data_len = len(data)
                            new_data = org_data[0: offset] + data + org_data[offset + data_len:]
                            loader = FlashLoader(self.session, chip_erase="sector")
                            loader.add_data(sector_info.base_addr, new_data)
                            loader.commit()
                            break
        else:
            return self.simulator.flash_file(data, addr)

    def flash_file(self, filename, addr, id=None):
        if not self.simulated:
            with open(filename, 'rb') as f:
                data = list(f.read())
            self.flash_write(data, addr, id)
        else:
            return self.simulator.flash_file(filename, addr)


if __name__ == '__main__':
    config = {
        'chip_name': 'STM32H743IGT',
        'unique_id': 'V0010M9E',
        'target': 'stm32h743xx',
        'connect_mode': 'attach',
        'simulated': False
    }
    ocd = OcdInterface(config)
    ocd.connect()
    addr = 0x08100000 + 0x80000 - 1024
    size = 1
    x = ocd.memory_read(addr, size)




