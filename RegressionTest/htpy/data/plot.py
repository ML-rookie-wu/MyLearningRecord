
import numpy as np
# import plotly.graph_objects as go
from nptdms import TdmsFile, TdmsWriter, ChannelObject

def save_voltage(path, voltage_data={}, properties={}):
    with TdmsWriter(path) as tdms_writer:
        channel_list = []
        data_list = voltage_data["电压值"]
        data_list_1 = voltage_data["电压精度"]
        channel = ChannelObject("持续测量", "电压值", data_list, properties=properties)
        channel2 = ChannelObject("持续测量", "电压精度", data_list_1, properties=properties)
        channel_list.append(channel)
        channel_list.append(channel2)
        tdms_writer.write_segment(channel_list)

