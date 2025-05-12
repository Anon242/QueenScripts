import os
from configparser import ConfigParser
import subprocess
import re;
from GetSignature import getSignature

def load_ini_config(config_path="config.ini"):
    config = ConfigParser()
    config.read(config_path, encoding='utf-8')
    return config


def compile(ino_file_path):

    script_dir = os.path.dirname(os.path.abspath(__file__))
    cache_dir = os.path.join(script_dir, "cache")
    cache_ino_file_path = os.path.join(script_dir, "inofile/inofile.ino")
    arduino_dir = load_ini_config(os.path.join(script_dir,"config.ini"))["Paths"]["arduino_dir"]
    hardware_dir = os.path.join(arduino_dir, "hardware")
    tools_avr_dir = os.path.join(hardware_dir, "tools/avr")
    arduino_builder_path = os.path.join(arduino_dir, "arduino-builder.exe")
    built_in_libraries_path = os.path.join(arduino_dir,"libraries")
    tools_builder_path = os.path.join(arduino_dir, "tools-builder")
    libraries_dir = os.path.join(os.path.expanduser( '~' ), "Documents/Arduino/libraries")

    file = open(ino_file_path,'r')
    content = file.read()

    cache_file = open(cache_ino_file_path,'w+')
    cache_file.write(content)
    cache_file.close()

    ino_file_path = cache_ino_file_path
    
    if (content.find("#include <R4") >= 0):
        fqbn_name = "arduino:avr:uno"
        print("\033[34m" + "Found in the code: Atmega328p"+ "\033[0m")
    elif (content.find("#include <QueenUnisense") >= 0):
        fqbn_name = "arduino:avr:mega:cpu=atmega2560"
        print("\033[34m" + "Found in the code: Atmega2560"+ "\033[0m")
    else:
        fqbn_name = getSignature()
        print("\033[34m" + "Found in the code: Atmega2560 with hardware"+ "\033[0m")
        if(fqbn_name == "" or fqbn_name == "Error"):
            print("\033[31m" + "Сигнатура не определена..." + "\033[0m")
            fqbn_name = "arduino:avr:uno"


    command = [
        arduino_builder_path,
        "-compile", 
        "-hardware", hardware_dir,
        "-tools", tools_avr_dir,
        "-tools", tools_builder_path,
        "-tools", tools_avr_dir,
        "-libraries", libraries_dir,
        "-built-in-libraries", built_in_libraries_path,
        "-fqbn", fqbn_name,
        "-build-path",cache_dir,
         ino_file_path,
    ]

    def print_progress_bars(data):
        lines = data.split('\n') 
        memory_info = lines[-3:len(lines)-1]  

        program_pattern = r'uses (\d+) bytes.*Maximum is (\d+) bytes'
        dynamic_pattern = r'use (\d+) bytes.*Maximum is (\d+) bytes'

        program_match = re.search(program_pattern, memory_info[0])
        dynamic_match = re.search(dynamic_pattern, memory_info[1])

        program_used = int(program_match.group(1))
        program_max = int(program_match.group(2))

        dynamic_used = int(dynamic_match.group(1))
        dynamic_max = int(dynamic_match.group(2))

        def create_bar(used, total, width=60):
            percent = used / total
            filled = int(round(width * percent))
            empty = width - filled
            return f"[{"\033[32m"}{'■' * filled}{"\033[0m"}{' ' * empty}] {percent:.0%}"

        print("\033[32m" + "===========================SUCCESS===========================" + "\033[0m")
        
        print(f"RAM:   {dynamic_used:,} / {dynamic_max:,} bytes")
        print(create_bar(dynamic_used, dynamic_max))

        print(f"Flash: {program_used:,} / {program_max:,} bytes")
        print(create_bar(program_used, program_max))
        print()




    result = subprocess.run(command, capture_output=True, text=True)
    if(result.stderr == ""):
        print_progress_bars(result.stdout)
        return True
    else:
        print(result.stderr)
        return False

