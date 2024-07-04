import logging
from socket import *
import socket
import threading
import time
import sys
import json
import base64

logging.basicConfig(level=logging.WARNING)

class Chat:
    def proses(self, data):
        data = json.loads(data)
        if data['type'] == 'login':
            logging.warning(f"{data['user']} logged in")
        elif data['type'] == 'signup':
            logging.warning(f"{data['user']} signed up")
        elif data['type'] == 'message':
            logging.warning(f"Message from {data['user']}: {data['message']}")
        elif data['type'] == 'file':
            logging.warning(f"File upload from {data['user']}: {data['filename']}")
        return {"status": "ok"}

chatserver = Chat()

class ProcessTheClient(threading.Thread):
    def __init__(self, connection, address):
        self.connection = connection
        self.address = address
        threading.Thread.__init__(self)

    def run(self):
        rcv = ""
        while True:
            data = self.connection.recv(32)
            if data:
                d = data.decode()
                rcv = rcv + d
                if rcv[-2:] == '\r\n':
                    logging.warning(f"data dari client: {rcv}")
                    hasil = json.dumps(chatserver.proses(rcv))
                    hasil = hasil + "\r\n\r\n"
                    logging.warning(f"balas ke client: {hasil}")
                    self.connection.sendall(hasil.encode())
                    rcv = ""
            else:
                break
        self.connection.close()

class Server(threading.Thread):
    def __init__(self):
        self.the_clients = []
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        threading.Thread.__init__(self)

    def run(self):
        self.my_socket.bind(('0.0.0.0', 8889))
        self.my_socket.listen(1)
        while True:
            self.connection, self.client_address = self.my_socket.accept()
            logging.warning(f"connection from {self.client_address}")
            clt = ProcessTheClient(self.connection, self.client_address)
            clt.start()
            self.the_clients.append(clt)

def main():
    svr = Server()
    svr.start()

if __name__ == "__main__":
    main()