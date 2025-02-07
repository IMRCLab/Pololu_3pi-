from machine import Timer, UART, Pin
from pololu_3pi_2040_robot import robot
import time


class StateDisplay():
    def __init__(self) -> None:
        self.display = robot.Display()
    

    def waiting_for_trajectory(self) -> None:
        self.display.fill(0)
        self.display.text("   WAITING FOR ", 0, 0+8)
        self.display.text("   ______", 0, 0+8+8)
        self.display.text("  /|_||_\`.__", 0, 8+8+8)
        self.display.text(" (   _    _ _\ ", 0,16+8+8)
        self.display.text(" =`-(_)--(_)-'",0,24+8+8)
        self.display.text("-- --- --- --- -",0,32+8+8)
        self.display.text("   TRAJECTORY", 0, 32+8+8+8)
        self.display.show()

    def received_trajectory(self,trajectory:str) -> None:
        self.display.fill(0)
        self.display.text("    TRAJECTOY: ", 0, 0+8)
        self.display.text("   ______", 0, 0+8+8)
        self.display.text("  /|_||_\`.__", 0, 8+8+8)
        self.display.text(" (   _    _ _\ ", 0,16+8+8)
        self.display.text(" =`-(_)--(_)-'",0,24+8+8)
        self.display.text("-- --- --- --- -",0,32+8+8)
        self.display.text(f"{trajectory[:-5]}", 0, 32+8+8+8)
        self.display.show()

    def ready(self) -> None:
        self.display.fill(0)
        self.display.text("     READY", 0, 0+8)
        self.display.text("   ______", 0, 0+8+8)
        self.display.text("  /|_||_\`.__", 0, 8+8+8)
        self.display.text(" (   _    _ _\ ", 0,16+8+8)
        self.display.text(" =`-(_)--(_)-'",0,24+8+8)
        self.display.text("-- --- --- --- -",0,32+8+8)
        self.display.text("     READY", 0, 32+8+8+8)
        self.display.show()

    def driving(self) -> None:
        self.display.fill(0)
        self.display.text("    DRIVING...", 0, 0+8)
        self.display.text("   ______", 0, 0+8+8)
        self.display.text("  /|_||_\`.__", 0, 8+8+8)
        self.display.text(" (   _    _ _\ ", 0,16+8+8)
        self.display.text(" =`-(_)--(_)-'",0,24+8+8)
        self.display.text("-- --- --- --- -",0,32+8+8)
        self.display.text("    DRIVING...", 0, 32+8+8+8)
        self.display.show()

    def driving_continously(self) -> None:
        def shift_left(s:str)-> str:
            if not s:  # Handle empty strings
                return ""
            return s[1:] + s[0]
        road = "-- --- --- --- -"
        for _ in range(20):
            self.display.fill(0)
            self.display.text("    DRIVING...", 0, 0+8)
            self.display.text("   ______", 0, 0+8+8)
            self.display.text("  /|_||_\`.__", 0, 8+8+8)
            self.display.text(" (   _    _ _\ ", 0,16+8+8)
            self.display.text(" =`-(_)--(_)-'",0,24+8+8)
            road = shift_left(road)
            self.display.text(road,0,32+8+8)
            self.display.text("    DRIVING...", 0,32+8+8+8)
            self.display.show()
            time.sleep(0.1)

    def finish_driving(self) ->None:
        self.display.fill(0)
        self.display.text("----------------",0,8)
        self.display.text("|  ______      |", 0, 0+8+8)
        self.display.text("| /|_||_\`.__  |", 0, 8+8+8)
        self.display.text("|(   _    _ _\ |", 0,16+8+8)
        self.display.text("|=`-(_)--(_)-' |",0,24+8+8)
        self.display.text("----------------",0,32+8+8)
        self.display.text("  DONE DRIVING", 0, 32+8+8+8)
        self.display.show()

    def finish_saving(self) -> None:
        self.display.fill(0)
        self.display.text("----------------",0,8)
        self.display.text("|  ______      |", 0, 0+8+8)
        self.display.text("| /|_||_\`.__  |", 0, 8+8+8)
        self.display.text("|(   _    _ _\ |", 0,16+8+8)
        self.display.text("|=`-(_)--(_)-' |",0,24+8+8)
        self.display.text("----------------",0,32+8+8)
        self.display.text("  DONE SAVING", 0, 32+8+8+8)
        self.display.show()

