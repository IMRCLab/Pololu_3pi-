from machine import Timer, UART, Pin
from pololu_3pi_2040_robot import robot
import time


class Display():
    def __init__(self) -> None:
        self.display = robot.Display()

def display_ready():
    display = robot.Display()
    display.fill(0)
    display.text("", 0, 0)
    display.text("", 0, 8)
    display.text("", 0,16)
    display.text(" ※\(^o^)/※",0,24)
    display.text("",0,32)
    display.text("", 24,40)
    display.text("",0,48)
    display.text("",0,56)
    display.show()
# (－‸ლ) exception doesnt work
# (•_•) ( •_•)>⌐■-■ (⌐■_■) csi
# ⛟ doenst work
# \ō͡≡o˞̶ doesnt work
"""
  ______
 /|_||_\`.__
(   _    _ _\
=`-(_)--(_)-'

"""
def display_car():
    display = robot.Display()
    
    display.fill(0)
    display.text("     READY", 0, 0+8)
    display.text("   ______", 0, 0+8+8)
    display.text("  /|_||_\`.__", 0, 8+8+8)
    display.text(" (   _    _ _\ ", 0,16+8+8)
    display.text(" =`-(_)--(_)-'",0,24+8+8)
    display.text("-- --- --- --- -",0,32+8+8)
    #display.text("", 0,40)
    #display.text("",0,48)
    #display.text("",0,56)
    time_start = time.time_ns()
    display.show()
    print(f"string save time {(time.time_ns()-time_start)*1e-9}")
    time.sleep(2)
    road = "-- --- --- --- -"
    for _ in range(50):
        display.fill(0)
        display.text("    DRIVING...", 0, 0+8)
        display.text("   ______", 0, 0+8+8)
        display.text("  /|_||_\`.__", 0, 8+8+8)
        display.text(" (   _    _ _\ ", 0,16+8+8)
        display.text(" =`-(_)--(_)-'",0,24+8+8)
        road = shift_left(road)
        display.text(road,0,32+8+8)
        display.show()
        time.sleep(0.1)
    display_car_stop()
    
def display():
    display = robot.Display()
    display.fill(0)
    display.text("     _  _", 0, 0+8)
    display.text("  __//  |___. ", 0, 8+8)
    display.text(" |'_ '--' _ | ", 0,16+8)
    display.text(" `(_)----(_)'=",0,24+8)
    display.text("-- --- --- --- -",0,32+8)
    #display.text("", 0,40)
    #display.text("",0,48)
    #display.text("",0,56)
    display.show()
   
def display_car_stop():
    display = robot.Display()
    
    display.fill(0)
    display.text("      DONE", 0, 0+8)
    display.text("----------------",0,8+8)
    display.text("|   ______     |", 0, 0+8+8+8)
    display.text("|  /|_||_\`.__ |", 0, 8+8+8+8)
    display.text("| (   _    _ _\|", 0,16+8+8+8)
    display.text("| =`-(_)--(_)-'|",0,24+8+8+8)
    display.text("----------------",0,32+8+8+8)
    #display.text("", 0,40)
    #display.text("",0,48)
    #display.text("",0,56)
    time_start = time.time_ns()
    display.show()
    print(f"string save time {(time.time_ns()-time_start)*1e-9}")

def shift_left(s):
    if not s:  # Handle empty strings
        return ""
    return s[1:] + s[0]
display_car()

while True:
    pass