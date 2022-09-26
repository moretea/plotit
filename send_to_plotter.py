#!/usr/bin/env python3

import serial
import sys
import time


class PlotterInterface():
    def __init__(self, port="/dev/ttyUSB0"):
        self.ser = serial.Serial(port=port, baudrate=115200)
        self.writeline("G90")
        self.hello_prompt=self.writeline("G90")
        print(self.hello_prompt);

    def readline(self):
        return self.ser.readline().decode("utf-8")

    def writeline(self, line, and_read_line=True):
        self.ser.write(bytes((line + "\n").encode("UTF-8")))
        if and_read_line:
            return self.readline()

pi = PlotterInterface()
lines = open(sys.argv[-1]).read().split("\n")
cnt = len(lines)


ACCEPTED_CMDS=["G90", "G4", "G1", "M5"]
for (idx, line) in enumerate(lines):
    if line == "":
        continue

    percentage = f"{float(int(float(idx)/float(cnt) * 100_00))/ 100}%"

    if line[-1] == ";":
        line = line[:-1]

    cmd = line.split(" ")[0]
    print("> ", idx, line, "OK", percentage);
    response = idx, pi.writeline(line).strip()
    print("<", response)
