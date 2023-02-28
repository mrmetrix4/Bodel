import configparser
import socket

CONFIG_FILE_PATH = "conf.ini"
BLACK_CORE_SETTINGS_SECTION = "BlackCoreSettings"
RED_CORE_SETTINGS_SECTION = "RedCoreSettings"
GLOBAL_SETTINGS_SECTION = "GlobalSettings"

config_file = configparser.ConfigParser()
config_file.read(CONFIG_FILE_PATH)

receiver_port = int(config_file[BLACK_CORE_SETTINGS_SECTION]["UDP_PORT"])
packet_size = int(config_file[GLOBAL_SETTINGS_SECTION]["PACKET_SIZE"])

receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
receiver_socket.bind(("", receiver_port))

while True:
    data, client = receiver_socket.recvfrom(packet_size)
