#!/usr/bin/env python3
from svg_to_gcode.svg_parser import parse_file
from svg_to_gcode.compiler import Compiler, interfaces
from svg_to_gcode.formulas import linear_map

class CustomInterface(interfaces.Gcode):
    def __init__(self):
        super().__init__()
        self.fan_speed = 1
    
    # Override the laser_off method such that it also powers off the fan.
    def laser_off(self):
        return "M5;\nG4 P0.20000000298023224;\n"  # Turn off the fan + turn off the laser

    # Override the set_laser_power method
    def set_laser_power(self, power):
        if power < 0 or power > 1:
            raise ValueError(f"{power} is out of bounds. Laser power must be given between 0 and 1. "
                             f"The interface will scale it correctly.")

        #return f"M106 S255\n" + f"M3 S{linear_map(0, 255, power)};"  # Turn on the fan + change laser power
        return f"M03 S1000;\nG4 P0.20000000298023224;\n"

custom_header = [
"M5",
"G4 P0.20000000298023224"
]

custom_footer = [
"M5",
"G4 P0.20000000298023224",
"G1 F3000",
"G1 X0 Y0"
]

gcode_compiler = Compiler(CustomInterface, movement_speed=3000, cutting_speed=1000, pass_depth=1, dwell_time=0.20000000298023224, custom_header=custom_header, custom_footer=custom_footer)


import sys
input_file = sys.argv[-1]
output_file = input_file + ".gcode"

curves = parse_file(input_file)

gcode_compiler.append_curves(curves) 
gcode_compiler.compile_to_file(output_file)
