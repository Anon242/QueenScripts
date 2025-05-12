import os
import subprocess
import re;

def getSignature():
    script_dir = os.path.dirname(os.path.abspath(__file__))

    tool_dir = os.path.join(script_dir, "tool-avrdude")
    avrdude_path = os.path.join(tool_dir, "avrdude.exe")
    avrdude_conf = os.path.join(tool_dir, "avrdude.conf")

    # Проверяем, существуют ли файлы
    if not os.path.exists(avrdude_path):
        raise FileNotFoundError(f"avrdude.exe не найден по пути: {avrdude_path}")
    if not os.path.exists(avrdude_conf):
        raise FileNotFoundError(f"avrdude.conf не найден по пути: {avrdude_conf}")

    command = [
        avrdude_path,
        "-C", avrdude_conf,
        "-p", "m328p",
        "-c", "usbasp",
        "-U", "signature:r:-:h"
    ]
    result = subprocess.run(command, capture_output=True, text=True)

    result_text = result.stdout +'\n'+ result.stderr

    if re.search(r'\b0x1e,0x95,0xf\b', result_text):
        return("arduino:avr:uno")
    elif re.search(r'\bATmega2560\b', result_text):
        return("arduino:avr:mega:cpu=atmega2560")
    else:
        return("Error")