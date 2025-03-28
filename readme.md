# filter expression

**filter expression parse engine**

eval `process->get_pid() == 0`  True or False in order to filter and query data results

I expect this script can eval compound expressions such as `thread->get_tid(1,2) == 1 || thread->get_tid(1,2) == 0 || thread->get_tid(12,2) == 0x10` 

design thoughts from [wireshark  display filter](https://www.wireshark.org/docs/wsug_html_chunked/ChWorkBuildDisplayFilterSection.html)

## shell
```
[**] FilterShell init context
[*] register process into context bag
[*] register memory into context bag
[*] register thread into context bag
filtershell>help
[*]
                    FilterShell  v0.1  by bopin

                    process.get_name() == "cmd"
                    process->get_name() in $COMSPEC

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
filtershell>quit
bye bye!
```


## Features

* support to register the global context obj, access object fields and methods



## todo

- [ ] const parse  =>  1 == 1, "bopin" in "bopin2020" and so on
- [ ] compound expressions eval
- [ ] tokenizer error report