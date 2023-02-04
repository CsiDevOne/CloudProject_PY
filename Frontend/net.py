import os.path
import socket


class Net:

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.addr = (socket.gethostname(), 525)

        try:
            self.socket.connect(self.addr)

        except ConnectionRefusedError:
            print('Verbindung mit server nicht möglich')
            exit(0)

        if not self.socket.recv(1024).decode() == 'CONNECTED':
            exit(0)

    def __del__(self):
        del self

    def __str__(self):
        return self.addr

    def send_credentials(self, logs):
        data = f'< log >{logs[0]}|{logs[1]}|{logs[2]}'
        self.socket.send(data.encode())

    def send_reg(self, logs):
        data = f'< reg >{logs[0]}|{logs[1]}|{logs[2]}'
        self.socket.send(data.encode())

    def send_upload(self, filename, data):
        self.socket.send('< upload >'.encode())
        if self.socket.recv(1024) == b'SIZE':
            self.socket.send(str(os.path.getsize(filename)).encode())
        if self.socket.recv(1024) == b'FILENAME':
            self.socket.send(filename.encode())
        if self.socket.recv(1024) == b'DATA':
            self.socket.send(data.encode())

    def send_download(self, filename):
        self.socket.send('< download >'.encode())
        if self.socket.recv(1024) == b'FILENAME':
            self.socket.send(filename.encode())
        file_size = int(self.socket.recv(1024))
        data = self.socket.recv(file_size)

        with open(filename, 'wb') as f:
            f.write(data)
