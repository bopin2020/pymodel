import os
from core.header import *
from core.express import *
from core.datamodel import*

FILTERSHELL = 'filtershell>'

class FilterShell(ConsoleLogable):
    def __init__(self):
        self.re = RootExpress()
        self._init_context()

    def _init_context(self):
        self.report2(f"FilterShell init context",2)
        self.re.register_context("process",ProcessModel())
        self.re.register_context("memory",MemoryModel())
        self.re.register_context("thread",ThreadModel())
        register_envs()
        self.report2('register environment variables')

    def _help(self):
        self.report('''
                    FilterShell  v0.1  by bopin

                    process.get_name() == "cmd"
                    process->get_name() in $COMSPEC

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
                print("bye bye!")
                break
                
            if user_input:
                result = self.eval(user_input)
            else:
                pass
