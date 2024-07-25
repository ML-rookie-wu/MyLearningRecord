import datetime
import os
import random

try:
    import nidcpower
    import hightime, time
    from RegressionTest.htpy.data.plot import DataProcess, save_current, save_voltage
except ImportError:
    print("nidcpower未安装")

import copy
from threading import Thread
from RegressionTest.htpy.common.common_api import *


class NiSmuChannel:
    def __init__(self, resource_name="NI_SMU_4147_0", channel=None, simulated=True):
        self.resource_name = resource_name
        self.channel = channel
        self.session = None
        self.config = None
        self.simulated = simulated

        self.accuracy_info = \
        load_dict_from_file(os.path.join(os.path.split(__file__)[0], 'ni_spec_info.json'))[self.resource_name][
            '精度信息']['精度信息']
        if not self.simulated:
            self.session = nidcpower.Session(resource_name=self.resource_name, channels=self.channel)
            self.session.reset()
        self.properties = {}
        self.current_gear = 0.05

    def __del__(self):
        if not self.simulated:
            self.session.close()
        print("NiSmuChannel.__del__")

    def cal_measured_voltage_accuracy(self, v):
        pass

    def cal_measured_current_accuracy(self, v):
        pass

    def send_sw_trigger_start(self):
        pass

    def run_in_thread(self, func):
        pass

    def output_disable(self):
        pass

    def measure_voltage(self, config={}):
        print("测量电压配置为：{}".format(config))
        reset = config.get("reset")
        current_level = config.get("current_level")
        if current_level is None:
            current_level = 0.0

        num = config.get("测量次数")
        if num is None:
            num = 1

        info = {
            "电压值": [],
            "电压精度": []
        }
        if self.simulated:
            for i in range(0, num):
                # 随机产生0~3.3v电压
                voltage = random.randint(0, 33) * 1.0 / 10
                # 精度为所产生电压的1/100~1/1000
                accuracy = voltage / random.randint(100, 1000)
                info["电压值"].append(voltage)
                info["电压精度"].append(accuracy)
            return info

        if reset:
            print(datetime.datetime.now(), '需要先关闭输出，否则之前的输出会影响测量结果')
            self.session.reset()
        aperture_time = config.get('测量间隔')
        if aperture_time is None:
            aperture_time = 0.1

        self.session.source_mode = nidcpower.SourceMode.SINGLE_POINT
        self.session.output_function = nidcpower.OutputFunction.DC_CURRENT
        self.session.output_enable = True
        self.session.current_level = current_level
        self.session.current_level_range = 0.000001
        self.session.voltage_level_range = 8

        if config.get("测量方式") is not None and config.get("测量方式") == "持续测量":
            self.session.configure_aperture_time(aperture_time, nidcpower.ApertureTimeUnits.SECONDS)
            # 发送测量命令
            self.session.measure_when = nidcpower.MeasureWhen.AUTOMATICALLY_AFTER_SOURCE_COMPLETE
            # 配置立即测量方式
            self.session.measure_record_length = 1
            self.session.measure_record_length_is_finite = False

        else:
            self.session.measure_when = nidcpower.MeasureWhen.ON_DEMAND

        self.session.commit()
        with self.session.initiate():
            if config.get("测量方式") is None or config.get("测量方式") == '立即测量':
                self.session.wait_for_event(nidcpower.Event.SOURCE_COMPLETE)
                for i in range(0, num):
                    voltage = self.session.channels[self.channel].measure(nidcpower.MeasurementTypes.VOLTAGE)
                    accuracy = self.cal_measured_voltage_accuracy(voltage)
                    info['电压值'].append(voltage)
                    info['电压精度'].append(accuracy)
            else:
                measurements = self.session.channels[self.channel].fetch_multiple(count=num, timeout=10)
                for measurement in measurements:
                    accuracy = self.cal_measured_voltage_accuracy(measurement.voltage)
                    info["电压值"].append(measurement.voltage)
                    info["电压精度"].append(accuracy)
                file_path = config.get("文件名称")
                if file_path is None:
                    file_path = "电压信息.tdms"
                save_voltage(file_path, info, properties=self.properties)
                print("file_path", file_path, len(info["电压值"]))

        # 测量完毕之后需要关闭输出
        self.session.reset

        return info

    def measure_current(self, config={}):
        """
        测量电流
        :param config:
        :return:
        """
        current_data = {
            self.channel: {
                '时间': [],
                '电流': [],
                '电压': [],
                '电流精度': [],
                '电流档位': [],

            }
        }
        measure_func = config.get("测量方式")
        if measure_func is None or measure_func == '立即测量':
            num = config.get('测量次数')
            if num is None:
                num = 1
            for i in range(0, num):
                if self.simulated:
                    # 随机产生0~10安培的电流
                    current = random.randint(0, 10) * 1.0 / 10
                    accuracy = current / random.randint(100, 1000)
                else:
                    current = self.session.channels[self.channel].measure(nidcpower.MeasurementTypes.CURRENT)
                    accuracy = self.cal_measured_current_accuracy(current)
                current_data[self.channel]['电流'].append(current)
                current_data[self.channel]['电流精度'].append(accuracy)
                current_data[self.channel]['电流档位'].append(self.current_gear)
            return current_data
        else:
            if not self.simulated:
                measurements = self.session.channels[self.channel].fetch_multiple(count=self.session.fetch_backlog)
                time.sleep(1)
                measurements = self.session.channels[self.channel].fetch_multiple(count=self.session.fetch_backlog)
                for i in range(len(measurements)):
                    current_data[self.channel]['时间'].append(i)
                    current_data[self.channel]['电流'].append(round(measurements[i].current, 9))
                    current_data[self.channel]['电压'].append(round(measurements[i].voltage, 9))
                    current_data[self.channel]['电流精度'].append(round(self.cal_measured_current_accuracy(measurements[i].current), 9))
                current_data[self.channel]['电流档位'].append(self.current_gear)
                file_path = config.get('文件名称')
                if file_path is None:
                    file_path = '电流信息.tdms'
                save_current(file_path, current_data, properties=self.properties)
            else:
                for i in range(0, 100):
                    current = random.randint(0, 10) * 1.0 / 10
                    accuracy = current / random.randint(100, 1000)
                    current_data[self.channel]['电流'].append(current)
                    current_data[self.channel]['电流精度'].append(accuracy)
                current_data[self.channel]['电流档位'].append(self.current_gear)
            return current_data


    def find_the_most_suitable_current_gear(self, voltage):
        pass

    def source_single_voltage(self, input_config={}):
        pass

    def sour_single_current(self, input_config={}):
        pass

    def sink_single_current(self, input_config={}):
        pass

    def wait_source_done(self):
        pass

    def __source_voltage_sequence(self, config={}):
        pass

    def source_voltage_by_speed(self, config={}):
        pass

    def source_voltage_different_stage_power_on_off(self, config={}):
        pass

    def source_voltage_waveform(self, channels="1", config={}):
        pass

    def source_voltage_sequence(self, channels="0", voltage_max=3.3, points_per_output_function=10,
                                aperture_time=0.0167, input_config={}):
        pass

    def sink_current_sequence(self, channels="3", current_max=0.06, points_per_output_function=10):
        pass

    def source_current_sequence(self, channels="3", current_max=0.06, points_per_output_function=10,
                                delay_in_seconds=0.05):
        pass

    def unit_conver(self, p):
        pass

    def get_time_seconds(self, p):
        pass


if __name__ == '__main__':
    pass
