from ctypes import *



class UINT32(LittleEndianStructure):
    _pack_ = 1
    _field_ = [
        ('value', c_uint32)
    ]


class UINT16(LittleEndianStructure):
    _pack_ = 1
    _field_ = [
        ('value', c_uint16)
    ]


class UINT8(LittleEndianStructure):
    _pack_ = 1
    _field_ = [
        ('value', c_uint8)
    ]


class UINT32_T_PRT(LittleEndianStructure):
    _pack_ = 1
    _field_ = [
        ('value', POINTER(c_uint32))
    ]


class UINT16_T_PRT(LittleEndianStructure):
    _pack_ = 1
    _field_ = [
        ('value', POINTER(c_uint16))
    ]


class UINT8_T_PRT(LittleEndianStructure):
    _pack_ = 1
    _field_ = [
        ('value', POINTER(c_uint8))
    ]
