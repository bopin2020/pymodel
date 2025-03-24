import os
import random
import hexdump
import json

from enum import IntEnum
__VERSION__ = "v0.1"
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
        if DEBUG or debug > 0:
            print(data)