# Fleet Info
This document contains info regarding the status, issues etc. of our ground robot fleet. The fleet consists of 10 [Pololu 3pi+ Hyper Edition](https://www.pololu.com/category/280/3pi-plus-32u4-oled-robot).

## 001
- Motors are solderdered in inverted, therefore motor direction has been flipped in the config (motors.py)
- Firmware version: MicroPython v1.22.1-g9b8c64c9c build 240117-9512cf9; with ulab 6.5.0-9a1d03d; Pololu 3pi+ 2040 Robot

## 002
- Firmware version: MicroPython v1.22.1-g9b8c64c9c build 240117-9512cf9; with ulab 6.5.0-9a1d03d; Pololu 3pi+ 2040 Robot
- 2024/07/10: gyro_turn.py shows weird behavior. The robot turns in the wrong direction and therefore never stops (as target angle is never reached). The motors are mounted and configured correctly though. Needs further investigation.

## 003


## 004
- 2024/07/24: seems to turn slightly to the right when trying to run a straight line in the sample code

## 005
- 2024/08/01: seems to turn slightly to the right when trying to run a straight line in the sample code

## 006
