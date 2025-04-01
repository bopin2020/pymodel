import os
import random
import hexdump
import json

from enum import IntEnum
__VERSION__ = "v2.3"
__AUTHOR__ = "bopin"
#
# reference Wireshark   filter section
# https://www.wireshark.org/docs/wsug_html_chunked/ChWorkBuildDisplayFilterSection.html
# 
# searching filter expression
# context
# primitive type
# examples:
#       context object  obj   obj has some fields and methods
#       $true  $false  $custom   built-in variables
#       obj.name == "bopin" && obj.sex == 1;
#
DEBUG = 0
log1 = []
log2 = []
log3 = []

class ConsoleLogable:
    _loglevel = 0
    @property
    def loglevel(self):
        return ConsoleLogable._loglevel

    @loglevel.setter
    def loglevel(self,loglevel):
        ConsoleLogable._loglevel = loglevel

    def report(self,data, debug = 0):
        if DEBUG or (debug > 0 and debug < 4):
            tmp = f'[*] {data}'
            log1.append(tmp)
            if self.loglevel >= 1:
                print(tmp)

    def report2(self,data,debug = 0):
        if DEBUG or (debug > 0 and debug < 4):
            tmp = f'[**] {data}'
            log2.append(tmp)
            if self.loglevel >= 2:
                print(tmp)

    def report3(self,data,debug = 0):
        if DEBUG or (debug > 0 and debug < 4):
            tmp = f'[***] {data}'
            log3.append(tmp)
            if self.loglevel >= 3:
                print(tmp)

class OperateResult(IntEnum):
    Success = 0x0000,
    UnknownError = 0x00fe,
    Failed = 0x00ff,