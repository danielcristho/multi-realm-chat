import json
import uuid
import logging
import sys
from queue import Queue

class Chat:
    def __init__(self):
        self.sessions = {}
        self.users = {}
        self.groups = {}
        self.setup_users()
    def proses(self, data):
        j = data.split(" ")
        try:
            command = j[0].strip()
            if command == 'register':
                username = j[1].strip()
                nama = j[2].strip()
                negara = j[3].strip()
                realm = j[4].strip()
                password = j[5].strip()
                logging.warning(f"REGISTER: register {username} {password}")
                return self.register_user(username, nama, negara, password, realm)
            elif command == 'auth':
                username = j[1].strip()
                password = j[2].strip()
                return self.autentikasi_user(username, password)
            else:
                return {'status': 'ERROR', 'message': '**Protocol Tidak Benar'}
        except KeyError:
            return {'status': 'ERROR', 'message': 'Informasi tidak ditemukan'}
        except IndexError:
            return {'status': 'ERROR', 'message': '--Protocol Tidak Benar'}

    def autentikasi_user(self, username, password):
        if username not in self.users:
            return {'status': 'ERROR', 'message': 'User Tidak Ada'}

        if self.users[username]['password'] != password:
            return {'status': 'ERROR', 'message': 'Password Salah'}

        tokenid = str(uuid.uuid4())
        self.sessions[tokenid] = {'username': username, 'userdetail': self.users[username]}

        return {'status': 'OK', 'tokenid': tokenid}

    def register_user(self, username, nama, negara, password, realm):
        if username in self.users:
            return {'status': 'ERROR', 'message': 'User Sudah Ada'}

        self.users[username] = {
            "nama": nama,
            "negara": negara,
            "password": password,
            "realm": realm,
            "incoming": {},
            "outgoing": {},
        }

        return {'status': 'OK', 'message': 'User Berhasil Ditambahkan'}

if __name__ == "__main__":
    j = Chat()
    while True:
        data = input("Command : ")
        hasil = j.proses(data)
        print(json.dumps(hasil))
