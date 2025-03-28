import os
from core.header import (
    __VERSION__,
    __AUTHOR__
)
from core.express import *
from core.datamodel import*

FILTERSHELL = 'filtershell>'

class DataModelInternal():
    def __init__(self,rootexpress : RootExpress):
        self.re = rootexpress
        
    def _format(self):
        pass

network_protocols = [
    # 应用层协议
    "http", "https", "ftp", "sftp", "tftp",
    "smtp", "pop3", "imap", "dns", "dhcp",
    "snmp", "telnet", "ssh", "ntp", "rdp",
    "sip", "ldap", "irc", "mqtt", "coap",
    
    # 传输层协议
    "tcp", "udp", "sctp", "dccp", "quic",
    
    # 网络层协议
    "ip", "ipv4", "ipv6", "icmp", "igmp",
    "bgp", "ospf", "rip", "is-is", "ipsec",
    "arp", "rarp", "nat", "gre", "ip-in-ip",
    
    # 数据链路层协议
    "ethernet", "ppp", "pppoe", "l2tp", "mac",
    "vlan", "stp", "cdp", "lldp", "hdlc",
    
    # 物理层协议/技术
    "dsl", "isdn", "docsis", "usb", "bluetooth",
    "zigbee", "wi-fi", "nfc", "lte", "5g",
    
    # 其他专用协议
    "tor", "i2p", "bittorrent", "websocket", "grpc",
    "webrtc", "rtsp", "rtmp", "smb", "nfs",
    "afp", "iscsi", "fcoe", "openflow", "vxlan"
]
class TestDataModel:
    def __init__(self):
        self._pid = random.randint(0x100,10000)
        self._ppid = random.randint(0x100,10000)
        self._name = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(5))
        self._protocol = random.choice(network_protocols)
        
    @property
    def pid(self):
        return self._pid
    
    @property
    def ppid(self):
        return self._ppid
    
    @property
    def name(self):
        return self._name
    
    @property
    def protocol(self):
        return self._protocol

class FilterShell(ConsoleLogable):
    def __init__(self):
        self.re = RootExpress()
        self._init_context()

    def _init_context(self):
        self.report2(f"FilterShell init context",2)
        self.re.register_context("process",ProcessModel())
        self.re.register_context("memory",MemoryModel())
        self.re.register_context("thread",ThreadModel())
        self.re.register_context("modelobj",TestDataModel())
        register_envs()
        self.report2('register environment variables')

    def _uninit_context(self):
        self.report2(f"FilterShell uninit context",2)
        self.re.unregister_contexts()
        unregister_envs()
        self.report2('unregister environment variables')

    def _help(self):
        self.report(f'''
                    FilterShell  {__VERSION__}  by {__AUTHOR__}

                    process.get_name() == "cmd"
                    process.get_name() ct "cmd"
                    process->get_name() in $COMSPEC
                    modelobj.name
                    modelobj.pid < 0x10000 && modelobj.ppid < 0x10000
                    modelobj.pid < 0x10000 && (modelobj.ppid < 0x10000 || modelobj.protocol == tcp)

                    help        :  print usage information
                    quit/exit   :  exit filtershell
                    ''',1)

    def eval(self,expression):
        try:
            result = self.re.invoke(expression)
            self.report3(result,1)
            return result
        except Exception as e:
            self.report3(str(e))

    def entry(self):
        while True:
            user_input = input(FILTERSHELL).strip()
            if user_input.lower() in ('cls','.cls','clear'):
                os.system("cls")
                continue

            if user_input.lower() in ('-h','help'):
                self._help()
                continue

            if user_input.lower() in ('q','quit', 'exit'):
                self._uninit_context()
                print("bye bye!")
                break
                
            if user_input:
                self.eval(user_input)
            else:
                pass