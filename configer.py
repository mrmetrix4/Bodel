import configparser

BLACK_CORE_SETTINGS_SECTION = "BlackCoreSettings"
RED_CORE_SETTINGS_SECTION = "RedCoreSettings"
GLOBAL_SETTINGS_SECTION = "GlobalSettings"

UDP_BLACK_RECEIVER_PORT = 4444
UDP_RED_SENDER_PORT = 4445
PACKET_SIZE = 1500
DEST_IP = "127.0.0.1"

config_file = configparser.ConfigParser()

config_file.add_section(GLOBAL_SETTINGS_SECTION)
config_file.add_section(BLACK_CORE_SETTINGS_SECTION)
config_file.add_section(RED_CORE_SETTINGS_SECTION)

config_file.set(GLOBAL_SETTINGS_SECTION, "PACKET_SIZE", str(PACKET_SIZE))
config_file.set(BLACK_CORE_SETTINGS_SECTION, "UDP_PORT", str(UDP_BLACK_RECEIVER_PORT))
config_file.set(RED_CORE_SETTINGS_SECTION, "UDP_PORT", str(UDP_RED_SENDER_PORT))
config_file.set(RED_CORE_SETTINGS_SECTION, "DEST_IP", DEST_IP)

with open(r"conf.ini", "w") as configFile:
    config_file.write(configFile)
