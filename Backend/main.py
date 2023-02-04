import request_handler as re


def main(addr):
    server = re.RequestHandler(addr)
    server.receive()


if __name__ == '__main__':
    main(('192.168.2.100', 525))
