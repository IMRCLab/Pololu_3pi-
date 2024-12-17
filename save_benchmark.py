from machine import Timer, UART, Pin
from pololu_3pi_2040_robot import robot
import time

def write_binaryappend(buffer:bytearray):
    time_start = time.time_ns()
    with open('save_benchmark', 'ab') as file:
        file.write(buffer)
    print(f"binary save time {(time.time_ns()-time_start)*1e-9}")

def write_csv(save_list:list):
    time_start = time.time_ns()
    with open('save_benchmark', "a") as file :
        #file.write(str([",".join(map(str, line)) + '\n' for line in save_list]))
        for row in save_list:
            file.write(','.join(map(str, row)) + '\n')
    print(f"csv save time {(time.time_ns()-time_start)*1e-9}")

def write_string(save_string:str):
    time_start = time.time_ns()
    with open('save_benchmark', "a") as file :
        file.write(save_string)
    print(f"string save time {(time.time_ns()-time_start)*1e-9}")

def write_stromg_csv(save_list:list):
    time_start = time.time_ns()
    with open('save_benchmark', "a") as file :
        #file.write(str([",".join(map(str, line)) + '\n' for line in save_list]))
        file.write(str(save_list))
    print(f"csv_string save time {(time.time_ns()-time_start)*1e-9}")


buffer = bytearray()
save_list = []
string_buffer = str()
for i in range(10):
    save_list.append([0x1,0x1,0x1,0x1,0x1,0x1,0x1,0x1,0x15])
    
for i in range(10):
    buffer+= b'/x01/x01/x01/x01/x01/x01/x01/x01/x15'

for i in range(10):
    string_buffer += "/x01/x01/x01/x01/x01/x01/x01/x01/x15"
    pass
write_binaryappend(buffer)
write_csv(save_list)
write_string(string_buffer)
write_stromg_csv(save_list)