from configparser import ConfigParser
import os
import sys
from datetime import datetime

def load_ini_config(config_path="config.ini"):
    config = ConfigParser()
    config.read(config_path, encoding='utf-8')
    return config


libraries_dir = os.path.join(os.path.expanduser( '~' ), "Documents/Arduino/libraries")
queen_kit_path = os.path.join(libraries_dir, "QueenKit/examples")

files = os.listdir(queen_kit_path)
boards = []
for file in files:
    boards.append(file)
        
i = 0
result = ""
print("\n\033[32mSelect a template [number]\033[0m")
for board in boards:
    i = i + 1
    result += f"[\033[33m{i}\033[0m:{board.split(".")[0]}] "

print(result)
phrase = int(input())

if(not isinstance(phrase, int)):
    print("Not a number")
    exit()

if(phrase < 1 or phrase > len(boards)):
    print("The number must be at least 1")
    exit()

phrase = phrase - 1
path = sys.argv[1]
if(os.path.exists(os.path.join(path, boards[phrase] + ".ino"))):
    print("\033[31mIt will find a file with the same name, which will cause the file to be lost. Continue? [y/n]\033[0m")
    if (input() != "y"):
        print("Stop")
        exit()
file = open(os.path.join(queen_kit_path, boards[phrase] + "/" + boards[phrase] + ".ino"),'r', encoding='utf-8')
content = file.read()

content = content.replace("!CREATEDFLAG", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
content = content.replace("!FILENAMEFLAG",  boards[phrase])

if (content.find("!AUTHORFLAG") != -1):
    content = content.replace("!AUTHORFLAG",  load_ini_config(os.path.join(os.path.dirname(os.path.abspath(__file__)),"config.ini"))["Options"]["author"])

new_file = open(os.path.join(path, boards[phrase] + ".ino"),'w+', encoding='utf-8')
new_file.write(content)

print("\033[32m" + boards[phrase]+ ".ino" + " has been added!" + "\033[0m")
