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

    file = open(ino_file_path,'r', encoding='utf-8')
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
        if(fqbn_name == "arduino:avr:uno"):
            print("\033[34m" + "Found in the code: Atmega328p with hardware"+ "\033[0m")
        else:
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

        def create_bar(used, total, width=79):
            percent = used / total
            filled = int(round(width * percent))
            empty = width - filled
            return f"[{"\033[32m"}{'■' * filled}{"\033[0m"}{' ' * empty}] {percent:.0%}"

        print("\033[32m" + "=====================================SUCCESS====================================" + "\033[0m")
        
        print(f"RAM:   {dynamic_used:,} / {dynamic_max:,} bytes")
        print(create_bar(dynamic_used, dynamic_max))

        print(f"Flash: {program_used:,} / {program_max:,} bytes")
        print(create_bar(program_used, program_max))
        print()




    result = subprocess.run(command, capture_output=True, text=True)
    if(result.stderr == ""):
        print_progress_bars(result.stdout)
        checkAllOffsets(content)
        return True
    else:
        print(result.stderr)
        return False

def checkAllOffsets(content):
    countGetBits = content.count("queen.getBits(")
    countSetBits = content.count("queen.setBits(")

    pattern = r"\.setBits\((\d+),\s*(\d+)"
    matches = re.findall(pattern, content)
    setBitsArray = [{"index": int(index), "size": int(size)} for index, size in matches]

    pattern = r"\.getBits\((\d+),\s*(\d+)"
    matches = re.findall(pattern, content)
    getBitsArray = [{"index": int(index), "size": int(size)} for index, size in matches]
    # ЗАГЛУШКА
    if (content.find("queen.pwmOuts(queen.getBits(bitIndex, 10), i + 1);") != -1):
        for i in range(16):
            getBitsArray.append({"index": int(16 + 10 * i), "size": int(10)})
        countGetBits += 15

    if (content.find("queen.setBits(bitIndex, 10, adcBuffer[i]);") != -1):
        for i in range(16):
            setBitsArray.append({"index": int(16 + 10 * i), "size": int(10)})
        countSetBits += 15

    if (countGetBits != len(getBitsArray)):
        print("\033[31mНе совпадение по количеству getBits\033[0m")
    if (countSetBits != len(setBitsArray)):
        print("\033[31mНе совпадение по количеству setBits\033[0m")

    def checkBitsData(data):
        array = [0] * 256
        result = ""
        for dat in data:
            for j in range(dat['size']):
                if(array[dat['index']+j] == 0):
                    array[dat['index']+j] = 1
                else:
                    array[dat['index']+j] = 2

        j = 0
        for i in array:
            j+=1
            if(i == 0):
                result+="▎"
            elif (i == 1):
                result+="\033[34m▎\033[0m"
            else:
                result+="\033[31m▎\033[0m"

            if(j % 32 == 0):
                result+='\n'
            
        
        return result

    def joinTables(table1, table2, spacing=6):
        lines1 = table1.split('\n')
        lines2 = table2.split('\n')

        max_lines = max(len(lines1), len(lines2))

        lines1 += [''] * (max_lines - len(lines1))
        lines2 += [''] * (max_lines - len(lines2))

        joined_lines = [f"{line1}{' ' * spacing}{line2}" for line1, line2 in zip(lines1, lines2)]

        return '\n'.join(joined_lines)

    print((" " * 23)+"GetBits" + (" " * 31) + "SetBits")
    tables = (joinTables(checkBitsData(getBitsArray), checkBitsData(setBitsArray)))

    numbersTables = """[0  -32 ]:
[32 -64 ]:
[64 -96 ]:
[96 -128]:
[128-160]:
[160-192]:
[192-224]:
[224-256]:
    """
    print(joinTables(numbersTables,tables,1), end="")
    print( "╲ 0" + (" " * 5) + "╲ 8" + (" " * 4) + "╲ 16" + (" " * 4) + "╲ 24" + (" " * 4) + "╲ 32"  + (" " * 3)+"╲ 0" + (" " * 5) + "╲ 8" + (" " * 4) + "╲ 16" + (" " * 4) + "╲ 24" + (" " * 4) + "╲ 32")

