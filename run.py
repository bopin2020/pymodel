import pytest
from core.express import *
from core.datamodel import *
from core.lexer import *
from shell import FilterShell

def test_sub():
    register_envs()
    ce = ChildExpress()
    ce.parse("$true -eq $true")
    print(ce.tokens)
    ce.parse("$COMSPEC != $OS")
    print(ce.tokens)
    ce.parse("obj.name -eq \"bopin\"")
    print(ce.tokens)
    ce.parse("obj.subobj.pro -eq \"bopin\"")
    print(ce.tokens)
    ce.parse("obj.get_obj().pro -eq \"bopin\"")
    print(ce.tokens)
    ce.parse("obj->name >= \"bopin\"")
    print(ce.tokens)
    ce.parse("obj->get_test(v1,v2,v3) -le \"bopin\"")
    print(ce.tokens)
    ce.parse("obj->get_test() == obj2.getname(obj)")
    print(ce.tokens)

def test_rootexpress():
    re = RootExpress()
    register_envs()
    #
    # 1. tokenizer lexer
    # 2. use ast to execute expression eval and map the built-in and env variables to the real vars
    # 3. execute method dynamically with reflection
    #
    re.parse("obj->get_test() == obj2.getname(obj) && obj->get_test(v1,v2,v3) -le \"bopin\" || obj->name == bopin && $COMSPEC != $OS")
    #re.parse("obj->get_test() == obj2.getname(obj) or obj->get_test(v1,v2,v3) -le \"bopin\" and obj->name == bopin or $COMSPEC != $OS")

def test_context_inject_manager():
    re = RootExpress()
    re.register_context("process",ProcessModel())
    re.register_context("memory",MemoryModel())
    re.register_context("thread",ThreadModel())
    register_envs()
    print(re.format_objmodel())
    # todo
    print(re.invoke("process.get_modules()"))
    print(re.invoke("process.modules"))
    #re.unregister_context("process")
    print(re.invoke("process->get_pid()"))

    hexdump.hexdump(re.invoke("memory->get_bytes(None,0x40)"))
    print(re.invoke("memory->test(0x10)"))

    print(re.invoke("process->get_pid() == 0"))
    print(re.invoke("process->get_pid() > 0"))
    print(re.invoke("process->get_pid() < 0"))
    print(re.invoke("process->get_pid() != 0"))
    print(re.invoke("process->get_pid() >= 0"))
    print(re.invoke("process->get_pid() <= 0"))

    print(re.invoke("0x10 == 16"))
    print(re.invoke("\"bo\" in \"bopin2020\""))
    print(re.invoke("\"bo\" in \"bopin2020\""))

    print(re.invoke("process->get_name() in $COMSPEC"))
    print(re.invoke("$COMSPEC ct process->get_name()"))
    print(re.invoke("\"cmd\" ct process->get_name()"))
    return

    print(re.invoke("process->get_name() == \"bopin\""))
    print(re.invoke("process->get_name() == $COMSPEC"))

    print(re.invoke("$COMSPEC == process->get_name()"))
    print(re.invoke("thread->get_tid(1,2) == 0"))
    print(re.invoke("thread->get_tid(1,2) != 0"))

    print(re.invoke("thread->get_tid(1,2) == 1 || thread->get_tid(1,2) == 0 || thread->get_tid(12,2) == 0x10"))

def test_method_args():
    me = MethodExpress()
    print(me.parse('get_name(v1,v2,v3)'))
    print(me.parse('get_name(1, "test", "this is a test")'))

if __name__ == '__main__':
    #test_sub()
    #test_rootexpress()
    #test_method_args()
    #test_context_inject_manager()
    FilterShell().entry()
    pass