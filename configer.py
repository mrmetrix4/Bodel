import configparser

UDP_BLACK_SOURCE_PORT = 4444
UDP_RED_DEST_PORT = 4444
BLACK_SRC_INTERFACE = "eth01"
RED_DEST_INTERFACE = "eth02"

BLACK_CORE_SETTINGS_SECTION = "BlackCoreSettings"
RED_CORE_SETTINGS_SECTION = "RedCoreSettings"

config_file = configparser.ConfigParser()

config_file.add_section(BLACK_CORE_SETTINGS_SECTION)
config_file.add_section(RED_CORE_SETTINGS_SECTION)

config_file.set(BLACK_CORE_SETTINGS_SECTION, "UDP_PORT", UDP_BLACK_SOURCE_PORT)
config_file.set(RED_CORE_SETTINGS_SECTION, "UDP_PORT", UDP_RED_DEST_PORT)

config_file.set(BLACK_CORE_SETTINGS_SECTION, "INTERFACE", BLACK_SRC_INTERFACE)
config_file.set(RED_CORE_SETTINGS_SECTION, "INTERFACE", RED_DEST_INTERFACE)

with open(r"conf.ini", "w") as configFile:
    config_file.write(configFile)
