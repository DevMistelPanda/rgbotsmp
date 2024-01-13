import logging
from typing import Literal
import json

logging.basicConfig(level=logging.INFO, filename="bot.log", filemode="a", format="[%(asctime)s] %(levelname)s : %(message)s")


def logthis(severity: Literal['info', 'debug', 'warning', 'error', 'critical'], message: str):
    if severity == "info":
        logging.info(message)
    elif severity == "debug":
        logging.debug(message)
    elif severity == "warning":
        logging.debug(message)
    elif severity == "error":
        logging.error(message)
    elif severity == "crtitcal":
        logging.critical(message)
    else:
        raise Exception

def open_json(file: str):
    json_file = open(file)
    loaded_file = json.load(json_file)
    json_file.close()
    return loaded_file

def checkpassword(password):
    loaded_file = open_json("Variables.json")
    if password == loaded_file[["general_variables"[0]]]:
        return True
    else:
        return False

def parse_server_info(string: str):
    server_info = string.split('<br/>')

    server1_info = server_info[:7]
    server2_info = server_info[7:-1]

    server1_dict = {}
    server2_dict = {}

    for i in range(1, len(server1_info)):
        key_value = server1_info[i].split(': ')
        if len(key_value) >= 2:
            key = key_value[0].strip()
            value = key_value[1].strip()
            server1_dict[key] = value

    for i in range(1, len(server2_info)):
        key_value = server2_info[i].split(': ')
        if len(key_value) >= 2:
            key = key_value[0].strip()
            value = key_value[1].strip()
            server2_dict[key] = value

    return server1_dict, server2_dict




