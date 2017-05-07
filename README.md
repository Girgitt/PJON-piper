```                                                                                                                                     
                         -yho:                                                                                                       
                         `sdhs                     ____     _____   _____    __  __                                                  
                          +oo.    ..:`            /\  _`\  /\___ \ /\  __`\ /\ \/\ \                      __                         
                      `   .yyo:+:/+++/+/-         \ \ \L\ \\/__/\ \\ \ \/\ \\ \ `\\ \             _____  /\_\   _____      __   _ __ 
                      .//-/os++//::::::::/.        \ \ ,__/   _\ \ \\ \ \ \ \\ \ , ` \   _______ /\ '__`\\/\ \ /\ '__`\  /'__`\/\`'_\
                    `.::ssoo+/:::----------:.       \ \ \/   /\ \_\ \\ \ \_\ \\ \ \`\ \ /\______\\ \ \L\ \\ \ \\ \ \L\ \/\  __/\ \ \/
                    `-oyso+/::---------..---:-       \ \_\   \ \____/ \ \_____\\ \_\ \_\\/______/ \ \ ,__/ \ \_\\ \ ,__/\ \____\\ \_\
                     osso/:::::---------------        \/_/    \/___/   \/_____/ \/_/\/_/           \ \ \/   \/_/ \ \ \/  \/____/ \/_/
                    +yso+/+sys+:-------...--+s-                                                     \ \_\         \ \_\              
                  .+s++//+yhdhd/:-------..--hyo-                                                     \/_/          \/_/          v0.1
                  :o+//+oyhdmmmo:----:+ooo--smh+/                                                                                    
                  :so/::/oyyhds:::-+yhhddy/-:ss+:`                                                                         PJON-piper
                  /s/:::-:/++:----::/oyyo/:----:-:`                                       little commandline client for the PJON™ bus
                  :+/:::::::::::::://+oo+/:::----:-                                       -------------------------------------------
                 `oo+////:///::::////++++//::::::/`                                              unnamed pipes are the user interface
                 ooo++++++/+////////////////::::/:                                           PJON™ bus is accessed over a serial port
                `+oo++++++////////////////////://-                                                                                   
              `oys++++++////://///////////////://:                                                                                   
     ```    `/hyys+/////////:/:://///////:////////                                                                                   
   -shhho+/+yhhyo+//:::::::/:::://:////::::::////+                                                                                   
   `/yhyosyhhhy++////:::://///:/://:::/::::://////:                                                                                  
    :yysssdddy+/////////////////////:::://:::/::///-                                                                                 
    -sysyhdhs////////::/:///:////::::::/::::::::::/-                                                                                 
     -+yhhyo////////:::::::/://://:::::::::::::::///                                                                                 
      `/hhyo++++/////://////::::::::::::::::::::///.                                                                                 
       .shssoooo+++++++////////::/::::::/://:::///+`     .../....\                          .....//........\                         
       `oysoooooooo++++++///////://////:///////+/   ./../.........\....\..           ...../..................\..........\            
       -+sssooossoooo+++++++/////:/:////////++++.../.........................../..../  ....................................\.........
           ossssssooos+++++////:///++++++++++........................................................................................
............................. o++/++++++++ ...............oy.........................................................................
...................... dmo .hmo+++++++++o  ............. dd  dd......................................................................
...................... oms./dh/+ ... +++s ............ /dhy my ......................................................................
................... do . hdssm/ ....... +/++o ....... /ddddsoyhh ....................................................................
.................... dhyhddddo ............ ++yy .. /odddmdd ........................................................................
....................... ddmdho .............. oohysydmmmd ...........................................................................
........................ mmmy .................. ddmmm ................................. [ based on a solid ground of PJON™ ] .......
.....................................................................................................................................
```
PJON™ is a self-funded, no-profit open-source project created and mantained by Giovanni Blu Mitolo gioscarab@gmail.com
https://github.com/gioblu/PJON

PJON-piper is a contribution to PJON™ by Zbigniew Zasieczny z.zasieczny@gmail.com

The purpose of PJON-piper is to provide an easy to use PJON client available for various OS platforms (Windows, Linux*).
------------------------------------------------------------------------------------------------------------------------
* currently only Rasbian for Raspberry PI will be supported (work in progress)
 
PJON-piper can be used to develop PJON connectivity from many programming languages by wrapping the stdin/out of the PJON-piper
e.g. running as a subprocess. PJON-piper is also an abstraction layer for maintaining compatibility with PJON for multiple 
ports in different languages without re-implementing any new PJON features in these languages.

An example of a PJON port utilizing PJON-piper is PJON-python - a python module providing programmatic interface to PJON bus from
the python programming language (https://github.com/Girgitt/PJON-python)
