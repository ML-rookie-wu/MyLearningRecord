import time

import numpy as np

try:
    import nidaqmx
    from nidaqmx.constants import *
except ImportError:
    print("nidaqmx未安装")


class NiFgen:

    def __init__(self, resource_name: str = "NI_FGEN_4463_0", channel: str = "ao0", simulated: bool = True):
        self.physical_channel = "{}/{}".format(resource_name, channel)

    @staticmethod
    def generate_sin_signal(frequency: int, sampling_rate: int, amplitude: float = 1):
        t = np.linspace(0, 1, sampling_rate, endpoint=False)
        signal = amplitude * np.sin(2 * np.pi * frequency * t)
        return signal

    def output_sin_wave(self, config: dict):
        """
        输出正弦波
        :param config:
        :return:
        """
        waveform_frequence = config.get("waveform_frequence")
        sampling_rate = config.get("sampling_rate")
        output_duration = config.get("output_duration")
        amplitude = config.get("amplitude")
        print("调用4463输出正弦波，振幅为：{}，传入的波形频率为：{}，采样率为：{}，波形输出时长为：{}".format(amplitude, waveform_frequence, sampling_rate, output_duration))
        if waveform_frequence is None or sampling_rate is None:
            return
        if output_duration is None:
            output_duration = 10
        if amplitude is None:
            amplitude = 1
        with nidaqmx.Task() as task:
            task.ao_channels.add_ao_voltage_chan(self.physical_channel)
            task.timing.cfg_samp_clk_timing(sampling_rate, sampling_mode=AcquisitionType.FINITE, samps_per_chan=int(sampling_rate * output_duration))
            signal = self.generate_sin_signal(waveform_frequence, sampling_rate, amplitude)
            start_time = time.time()
            task.write(signal, auto_start=True)
            task.wait_until_done(output_duration * 5)
            if task.is_task_done():
                end_time = time.time()
                task.stop()
            time_count = end_time - start_time

    def output_current_voltage(self, config: dict):
        """
        输出单点电压
        :param config:
        :return:
        """
        voltage = config.get("voltage")
        sampling_rate = config.get("sampling_rate")
        output_duration = config.get("output_duration")
        if voltage is None or sampling_rate is None:
            return
        if output_duration is None:
            output_duration = 10
        with nidaqmx.Task() as task:
            task.ao_channels.add_ao_voltage_chan(self.physical_channel)
            task.timing.cfg_samp_clk_timing(sampling_rate, sampling_mode=AcquisitionType.FINITE, samps_per_chan=int(sampling_rate * output_duration))
            signal = [voltage] * sampling_rate
            task.write(signal, auto_start=True)
            task.wait_until_done(output_duration * 5)
            if task.is_task_done():
                task.stop()


if __name__ == '__main__':
    wave_config = {
        "sampling_rate": 10000,   # 采样率，范围100~51200Hz
        "output_duration": 10, # 输出总时间
        "voltage": 2.8   # 电压值
    }
    nifen = NiFgen()
    nifen.output_current_voltage(wave_config)