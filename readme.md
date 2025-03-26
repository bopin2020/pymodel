# filter expression

**filter expression parse engine**

eval `process->get_pid() == 0`  True or False in order to filter and query data results

I expect this script can eval compound expressions such as `thread->get_tid(1,2) == 1 || thread->get_tid(1,2) == 0 || thread->get_tid(12,2) == 0x10` 

design thoughts from [wireshark  display filter](https://www.wireshark.org/docs/wsug_html_chunked/ChWorkBuildDisplayFilterSection.html)



## Features

* support to register the global context obj, access object fields and methods



## todo

- [ ] const parse  =>  1 == 1, "bopin" in "bopin2020" and so on
- [ ] compound expressions eval