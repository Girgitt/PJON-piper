#!/bin/sh

gcc pjon_piper_main.cpp -o ./build/rpi/pjon_piper -std=c++11 -lwiringPi -lpthread -lstdc++