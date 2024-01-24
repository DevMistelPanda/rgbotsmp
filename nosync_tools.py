import logging
from typing import Literal
import json
from interactions import Embed, Color
import datetime




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

def create_embed(server_info1:dict, server_info2:dict):
    info_embed = Embed() #implement Embed for both Servers
    if "Statusmessage" in  server_info1.keys() or server_info1.keys(): #check for offline Server
        #Set Statusmessage to something printable
        if "Statusmessage" in server_info1.keys():
            server_info1 = "Server Offline"
        else:
            server_info2 = "Server Offline"


    info_embed.footer = "Powered by Mistel_Panda"
    info_embed.title = "Server Information"
    info_embed.description = "For more information use '@MinecraftServerBot info'"
    info_embed.timestamp = datetime.datetime.now()
    try:
        info_embed.add_field("Server 1   ✅", server_info1["MOTD"], inline=False)
        info_embed.add_field("Version", server_info1["Version"], inline=True)
        info_embed.add_field("Online Players", server_info1["Players"], inline=True)
        info_embed.add_field("IP- Address", server_info1["IP-Address"], inline=True)

    except:
        info_embed.add_field("Server 1   ⚠️", server_info1, inline=False)

    info_embed.add_field(" ", " ", inline=False) #Create Blank space between server Informations

    try:
        info_embed.add_field("Server 2   ✅", server_info2["MOTD"], inline=False)
        info_embed.add_field("Version", server_info2["Version"], inline=True)
        info_embed.add_field("Online Players", server_info2["Players"], inline=True)
        info_embed.add_field("IP- Address", server_info2["IP-Address"], inline=True)

    except:
        info_embed.add_field("Server 2   ⚠️", server_info2, inline=False)

    return info_embed


