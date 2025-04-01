# filter expression

**filter expression parse engine**

eval `process->get_pid() == 0`  True or False in order to filter and query data results

I expect this script can eval compound expressions such as `thread->get_tid(1,2) == 1 || thread->get_tid(1,2) == 0 || thread->get_tid(12,2) == 0x10` 

design thoughts from [wireshark  display filter](https://www.wireshark.org/docs/wsug_html_chunked/ChWorkBuildDisplayFilterSection.html)



note:  Ugly code!



## shell
```
[**] FilterShell init context
[*] register process into context bag
[*] register memory into context bag
[*] register thread into context bag
[*] register modelobj into context bag
[*] register setting into context bag
[*] register aa.component into context bag
filtershell>help
[*] 
                    FilterShell  v2.3  by bopin

                    process.get_name() == "cmd"
                    process.get_name() ct "cmd"
                    process->get_name() in $COMSPEC
                    modelobj.name
                    modelobj.pid < 0x10000 && modelobj.ppid < 0x10000
                    modelobj.pid < 0x10000 && (modelobj.ppid < 0x10000 || modelobj.protocol == tcp)
                    modelobj.pid < 1000 && modelobj.ppid < 1000 || modelobj.protocol != "tcp"

                    (1 == 1) and ('aa' != 'aabc' or 1 == 2) and 1 < 2

                    "whoami" in "whoami222" || 212 != 234

                    help        :  print usage information
                    quit/exit   :  exit filtershell

filtershell>process.get_name() == "cmd"
[*] [LeftObjMethod  process.get_name(), Operation  ==, Const  "cmd"]
[**] parse finished
[***] False
filtershell>process->get_name() in $COMSPEC
[*] [LeftObjMethod  process->get_name(), Operation  in, BuiltInVar  $COMSPEC]
[**] parse finished
[***] True
filtershell>"whoami" in "whoami222" || 212 != 234
[**] childexpress [LeftConst  "whoami", Operation  in, RightConst  "whoami222"]
[**] childexpress [LeftConst  212, Operation  !=, RightConst  234]
[**] parse finished
[*] "whoami"
[*] 212
"whoami" in "whoami222" || 212 != 234  [True, True]
[***] [True, True]
count: 1
filtershell>q
[**] FilterShell uninit context
[*] unregister process from context bag
[*] unregister memory from context bag
[*] unregister thread from context bag
[*] unregister modelobj from context bag
[*] unregister setting from context bag
[*] unregister aa.component from context bag
bye bye!
```


## Features

* support to register the global context obj, access object fields and methods



## todo

- [x] const parse  =>  1 == 1, "bopin" in "bopin2020" and so on
- [ ] compound expressions eval
- [ ] tokenizer error report
- [ ] support () => (1 == 1) and ('aa' != 'aabc' or 1 == 2) and 1 < 2