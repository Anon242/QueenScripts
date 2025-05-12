from GetSignature import *
from Compile import compile
import os
import sys
import subprocess
from datetime import datetime

res = compile(sys.argv[1])

if(not res):
    print("\033[31mFailed!\033[0m")
    exit()
if (len(sys.argv) > 2 and sys.argv[2] == "-C"):
    print("\033[32mCompleted!\033[0m")
    exit()

script_dir = os.path.dirname(os.path.abspath(__file__))
cache_dir = os.path.join(script_dir, "cache")
avrdude_conf_path = os.path.join(script_dir, "tool-avrdude/avrdude.conf")
avrdude_path = os.path.join(script_dir, "tool-avrdude/avrdude.exe")

hex_path = ""
files = os.listdir(cache_dir)
for file in files:
    if(file.find(".ino.hex")!= -1):
        hex_path = os.path.join(script_dir, "cache/" + file)
        break

if(hex_path == ""):
    print("Hex not found")
    exit()

if (len(sys.argv) > 2 and sys.argv[2] == "-H"):
    time_str = datetime.now().strftime("%H-%M")
    my_file = open(os.path.dirname(sys.argv[1]) + "/" +os.path.basename(sys.argv[1]).split(".ino")[0] + ".hex", "w+")
    hex_file = open(hex_path)
    data = hex_file.read()
    my_file.write(data)
    print("\033[35mHex loaded!\033[0m")
    exit()

fqbn_name = getSignature()

mcu = "atmega328p"
if(fqbn_name == "arduino:avr:uno"):
    mcu = "atmega328p"

    result = subprocess.run(f"{avrdude_path} -c usbasp -p m328p -P usb -b 19200 -B 125kHz -U hfuse:r:-:h -U lfuse:r:-:h -U efuse:r:-:h", capture_output=True, text=True)
    if(result.stdout.find("0xde\n0xff\n0xfd") == -1):
        print("\033[35mNew microcontroller detected, write FUSE...\033[0m")
        subprocess.run(f"{avrdude_path} -c usbasp -p m328p -P usb -b 19200 -B 125kHz -U lfuse:w:0xFF:m -U hfuse:w:0xDE:m -U efuse:w:0xFD:m", capture_output=True, text=True)
else:
    mcu = "atmega2560"


command = [
    avrdude_path,
    "-C", avrdude_conf_path, 
    "-p", mcu,
    "-c", "usbasp",
    "-U", f"flash:w:{hex_path}:i"
]

subprocess.run(command, stdout=None, stderr=None)
