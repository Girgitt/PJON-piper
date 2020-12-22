```                                                                                                                                     

                      -yho:                                                                                                  
                      `sdhs                ____     _____   _____    __  __                                                  
                        +oo.    ..:`      /\  _`\  /\___ \ /\  __`\ /\ \/\ \                      __                         
                   `   .yyo:+:/+++/+/-    \ \ \L\ \\/__/\ \\ \ \/\ \\ \ `\\ \             _____  /\_\   _____      __   _ __ 
                   .//-/os++//::::::::/.   \ \ ,__/   _\ \ \\ \ \ \ \\ \ , ` \   _______ /\ '__`\\/\ \ /\ '__`\  /'__`\/\`'_\
                 `.::ssoo+/:::----------:.  \ \ \/   /\ \_\ \\ \ \_\ \\ \ \`\ \ /\______\\ \ \L\ \\ \ \\ \ \L\ \/\  __/\ \ \/
                 `-oyso+/::---------..---:-  \ \_\   \ \____/ \ \_____\\ \_\ \_\\/______/ \ \ ,__/ \ \_\\ \ ,__/\ \____\\ \_\
                  osso/:::::---------------   \/_/    \/___/   \/_____/ \/_/\/_/           \ \ \/   \/_/ \ \ \/  \/____/ \/_/
                 +yso+/+sys+:-------...--+s-                                                     \ \_\         \ \_\         
               .+s++//+yhdhd/:-------..--hyo-                                                     \/_/          \/_/     v0.1
               :o+//+oyhdmmmo:----:+ooo--smh+/                                                                               
               :so/::/oyyhds:::-+yhhddy/-:ss+:`                                                                    PJON-piper
               /s/:::-:/++:----::/oyyo/:----:-:`                                 Little command-line client for the PJON™ bus
               :+/:::::::::::::://+oo+/:::----:-                                 --------------------------------------------
              `oo+////:///::::////++++//::::::/`                                         unnamed pipes are the user interface
              ooo++++++/+////////////////::::/:                                      PJON® bus is accessed over a serial port
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
   -+sssooossoooo+++++++/////:/:////////++++.../.........................../..../  ....................................\.....
       ossssssooos+++++////:///++++++++++....................................................................................
...................... o++/++++++++ ...............oy........................................................................
............... dmo .hmo+++++++++o  ............. dd  dd.....................................................................
............... oms./dh/+ ... +++s ............ /dhy my .....................................................................
............ do . hdssm/ ....... +/++o ....... /ddddsoyhh ...................................................................
............. dhyhddddo ............ ++yy .. /odddmdd .......................................................................
................ ddmdho .............. oohysydmmmd ..........................................................................
................. mmmy .................. ddmmm ................................. [ Based on a solid ground of PJON® ] ......
.............................................................................................................................
```
PJON™ is a self-funded, no-profit open-source project created and mantained by Giovanni Blu Mitolo gioscarab@gmail.com
https://github.com/gioblu/PJON

PJON-piper is a contribution to PJON™ by Zbigniew Zasieczny z.zasieczny@gmail.com

The purpose of PJON-piper is to provide an easy to use PJON client available for various OS platforms (Windows, Linux*).
------------------------------------------------------------------------------------------------------------------------
* currently Rasbian for Raspberry PI is supproted in all branches; branches dev_0_12 and newer also support Linux x86
 
PJON-piper can be used to develop PJON connectivity from many programming languages by wrapping the stdin/out of the PJON-piper
e.g. running as a subprocess. PJON-piper is also an abstraction layer for maintaining compatibility with PJON for multiple 
ports in different languages without re-implementing any new PJON features in these languages.

An example of a PJON port utilizing PJON-piper is PJON-python - a python module providing programmatic interface to PJON bus from
the python programming language (https://github.com/Girgitt/PJON-python)


PJON-piper uses a branched development approach as follows: 
-----------------------------------------------------------------
 
1. There are no direct commits to the master branch which purpose is to accept PRs and be a base to create development branches or forks 
2. Master is neither the unstable of newest code. It should have the latest stable tag merged from the latest development branch.
3. Development is done in dev_X_Y branches where:
- X defines compatibility within PJON-piper (stdin/out interface should not change for a given X number)
- Y defines compatibility with PJON version 

Example: dev_0_12 is a branch with PJON v12 library and has tags rel_0_12_1_0, rel_0_12_1_1.. where the last digit indicates bugfix release. Each release tag from dev_0_12 should work with any code using PJON-piper version "0" API and PJON devices built with PJON v12 library - in this example v12.1 thus there are four release tag digits. 

Please checkout the branch compatible with the PJON version being used or use tags to get the tested code. 
