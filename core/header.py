import os
import random
import hexdump
import json

from enum import IntEnum
__VERSION__ = "v2.2"
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

class ConsoleLogable:
    def report(self,data, debug = 0):
        if DEBUG or (debug > 0 and debug < 4):
            print(f'[*] {data}')

    def report2(self,data,debug = 0):
        if DEBUG or (debug > 0 and debug < 4):
            print(f'[**] {data}')

    def report3(self,data,debug = 0):
        if DEBUG or (debug > 0 and debug < 4):
            print(f'[***] {data}')

class OperateResult(IntEnum):
    Success = 0x0000,
    UnknownError = 0x00fe,
    Failed = 0x00ff,