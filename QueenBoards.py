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
print("\n\033[32mВыбери шаблон: \033[0m")
for board in boards:
    i = i + 1
    result += f"[{i}]: {board.split(".")[0]} "

print(result)
phrase = int(input())

if(not isinstance(phrase, int)):
    print("Не число")
    exit()

if(phrase < 1 or phrase > len(boards)):
    print("Выход за пределы")
    exit()

phrase = phrase - 1
path = sys.argv[1]
if(os.path.exists(os.path.join(path, boards[phrase]))):
    print("\033[31mНайдет файл с таким же названием, создание приведет к потере файла. Продолжить? [y/n]\033[0m")
    if (input() != "y"):
        print("Отмена")
        exit()
file = open(os.path.join(queen_kit_path, boards[phrase] + "/" + boards[phrase] + ".ino"),'r', encoding='utf-8')
content = file.read()

content = content.replace("!CREATEDFLAG", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
content = content.replace("!FILENAMEFLAG",  boards[phrase])

new_file = open(os.path.join(path, boards[phrase] + ".ino"),'w+', encoding='utf-8')
new_file.write(content)

print("Готово")