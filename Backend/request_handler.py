import socket
import threading

from log import *
import serilization as files


class RequestHandler:

    def __init__(self, addr):

        self.sys_logs = Log('Logs/sys_logs.log')
        self.client_logs = []

        self.clients = []

        self.addr = addr
        self.hostname, self.port = addr[0], addr[1]

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(self.addr)

        self.sys_logs.logger.info('Server is now listening ...')
        self.socket.listen()

    @staticmethod
    def send_to_all(clients, message):
        for client in clients:
            client.send(message.encode())

    def handle_client(self, client, address):
        connected = True
        if not files.is_registered(address[0]):
            files.save_hostname(address[0])
            files.create_user_dir(address[0])

        client_log = Log(f'Logs/{address[0]}.log')
        self.client_logs.append(client_log)
        client_log.clear_logs()

        client_log.logger.info(f'{address} connected to the server')

        while connected:
            try:
                request = client.recv(1024).decode()

                if request == '<< !DISCONNECT! >>':
                    files.remove_client(client, client_log, self.clients, self.client_logs)
                    client.close()
                    connected = False
                    break
                else:
                    data = files.translate(request, address[0], client)
                    if data is not None:
                        client.send(data)

                client_log.logger.info(f'REQUEST: {request}')

            except ConnectionResetError or ConnectionAbortedError or ConnectionError as exc:

                client_log.logger.exception(f'{exc} Exception raised with client {address[0]}')
                files.remove_client(client, client_log, self.clients, self.client_logs)

                break

    def receive(self):
        while True:
            client, address = self.socket.accept()

            self.clients.append(client)
            self.sys_logs.logger.info(f'{address[0]} connected to the server on port {address[1]}')

            client.send('CONNECTED'.encode())

            t = threading.Thread(target=self.handle_client, args=(client, address))
            t.start()

            self.sys_logs.logger.info(f'Thread for client {address[0]} started')

    def stop(self):
        self.sys_logs.logger.critical('  <! SYSTEM STOPS !>  ')
        self.send_to_all(self.clients, '<! SYSTEM STOPS !>')
        del self.sys_logs
        for log_client in self.client_logs:
            log_client.handler.close()
        self.socket.shutdown(0)
        exit(0)


if __name__ == '__main__':
    re_handler = RequestHandler(('192.168.2.100', 525))
    re_handler.receive()