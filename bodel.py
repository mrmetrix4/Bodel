import configparser
import socket
from json import loads, dumps, JSONDecodeError

CONFIG_FILE_PATH = "conf.ini"
BLACK_CORE_SETTINGS_SECTION = "BlackCoreSettings"
RED_CORE_SETTINGS_SECTION = "RedCoreSettings"
GLOBAL_SETTINGS_SECTION = "GlobalSettings"
OVERFLOW_SOCKET_ERRORNO = 10040


def safe_recv_json(receiver_socket, packet_size):
    try:
        data, client = receiver_socket.recvfrom(packet_size)
    except OSError as e:
        if e.winerror != OVERFLOW_SOCKET_ERRORNO:
            raise e
        print(f"[*] Overflow message sent to the black core.")
        print(f"[*] The message size was >{packet_size}.")
        return None
    print(f"[*] Black core received message:")
    print(data.decode())
    try:
        recv_json = loads(data.decode())
    except JSONDecodeError:
        print(f"[*] JSON schema mismatch from {client}.")
        return None

    return recv_json


def send_json(sender_socket, dest_ip, dest_port, data):
    data_size = sender_socket.sendto(data.encode(), (dest_ip, dest_port))
    print(f"[*] Red core sent {data_size} bytes sized message:")
    print(data)


def exec_from_dict(d):
    if "onError" not in d:
        return
    try:
        exec(d["onError"])
    except Exception as e:
        print(f"[*] Could not execute \"{d['onError']}\"")
        print(f"[*] Exception {e}")
    else:
        print(f"[*] Executed \"{d['onError']}\"")


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

    print(f"[*] Opened the black core receiver on {receiver_port}/UDP.")

    while True:
        if not (recv_json := safe_recv_json(receiver_socket, packet_size)):
            continue
        exec_from_dict(recv_json)
        filtered_json = filter_json(recv_json)
        send_json(sender_socket, dest_ip, dest_port, dumps(filtered_json))


if __name__ == "__main__":
    main()
