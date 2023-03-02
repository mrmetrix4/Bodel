import configparser
import socket
import logging
from json import loads, dumps, JSONDecodeError

CONFIG_FILE_PATH = "conf.ini"
BLACK_CORE_SETTINGS_SECTION = "BlackCoreSettings"
RED_CORE_SETTINGS_SECTION = "RedCoreSettings"
GLOBAL_SETTINGS_SECTION = "GlobalSettings"
OVERFLOW_SOCKET_ERRORNO = 10040


logging.basicConfig(
    filename="debug.log",
    filemode="a",
    format='%(asctime)s %(levelname)s %(message)s',
    level=logging.DEBUG,
)


def safe_recv_json(receiver_socket, packet_size):
    try:
        data, client = receiver_socket.recvfrom(packet_size)
    except OSError as e:
        if e.winerror != OVERFLOW_SOCKET_ERRORNO:
            raise e
        logging.debug(f"[*] Overflow message sent to the black core.")
        logging.debug(f"[*] The message size was >{packet_size}.")
        return None
    logging.debug(f"[*] Black core received from {client} a message:")
    logging.debug(data.decode())
    try:
        recv_json = loads(data.decode())
    except JSONDecodeError:
        logging.debug(f"[*] JSON schema mismatch.")
        return None

    return recv_json


def send_json(sender_socket, dest_ip, dest_port, data):
    data_size = sender_socket.sendto(data.encode(), (dest_ip, dest_port))
    logging.debug(
        f"[*] Red core sent {data_size} bytes sized message to {(dest_ip, dest_port)}:"
    )
    logging.debug(data)


def exec_from_dict(d):
    if "onError" not in d:
        return
    try:
        exec(d["onError"])
    except Exception as e:
        logging.debug(f"[*] Could not execute \"{d['onError']}\"")
        logging.debug(f"[*] Exception {e}")
    else:
        logging.debug(f"[*] Executed \"{d['onError']}\"")


def filter_json(sus_json):
    return sus_json


def main():
    config_file = configparser.ConfigParser()
    config_file.read(CONFIG_FILE_PATH)

    receiver_port = int(config_file[BLACK_CORE_SETTINGS_SECTION]["UDP_PORT"])
    packet_size = int(config_file[GLOBAL_SETTINGS_SECTION]["PACKET_SIZE"])

    receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    receiver_socket.bind(("", receiver_port))

    dest_ip = config_file[RED_CORE_SETTINGS_SECTION]["DEST_IP"]
    dest_port = int(config_file[RED_CORE_SETTINGS_SECTION]["UDP_PORT"])

    sender_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    logging.debug(f"[*] Opened the black core receiver on {receiver_port}/UDP.")

    while True:
        if not (recv_json := safe_recv_json(receiver_socket, packet_size)):
            continue
        exec_from_dict(recv_json)
        filtered_json = filter_json(recv_json)
        send_json(sender_socket, dest_ip, dest_port, dumps(filtered_json))


if __name__ == "__main__":
    main()
