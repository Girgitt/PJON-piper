#! /bin/bash

g++ -DLINUX -I. -I PJON//src -std=gnu++11 pjon_piper_main.cpp -o PJON-piper.exe -lpthread -lcrypt -lm -lrt
