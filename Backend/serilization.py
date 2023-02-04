import os
import pickle
import sqlite3
import hashlib


FILE = 'Users/users.pickle'
ENDL = '\n'.encode()


def str_find(string, char):
    indexes = []
    index = 0

    for i in string:
        index += 1
        if i == char:
            indexes.append(index)

    return indexes


def save_hostname(address):
    with open(FILE, 'rb') as f:
        try:
            data = pickle.load(f)
        except EOFError:
            data = []

    with open(FILE, 'wb') as f:
        pickle.dump(data + [address], f)


def get_all_users():
    with open(FILE, 'rb') as f:
        data = pickle.load(f)

    return data


def is_registered(address):
    if os.path.getsize(FILE) > 0:
        with open(FILE, 'rb') as f:
            data = pickle.load(f)
            return True if address in data else False
    else:
        return False


def check_dir(address):
    return os.path.exists(os.getcwd().join('Users/' + address))


def create_user_dir(address):
    if not check_dir(address):
        os.chdir('Users/')
        os.mkdir(address)

        os.chdir('../Logs')
        open(f'{address}.log', 'w').close()

        os.chdir('../')


def translate(request, address, client):

    # reg
    if request.__contains__('< reg >'):
        username = request[7:str_find(request, '|')[0] - 1]
        email = request[str_find(request, '|')[0]:str_find(request, '|')[1] - 1]
        password = hashlib.sha256(request[str_find(request, '|')[1]:].encode()).hexdigest()

        db_conn = sqlite3.connect('bin/userdata.db')
        cursor = db_conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS userdata (
            id INTEGER PRIMARY KEY,
            username VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            password VARCHAR(255) NOT NULL,
            address VARCHAR(255) NOT NULL
        )
        """)

        cursor.execute('INSERT INTO userdata (username, email, password, address) VALUES (?, ?, ?, ?)',
                       (username, email, password, address))

        db_conn.commit()

        return '< success >'.encode()

    # log
    elif request.__contains__('< log >'):
        username = request[7:str_find(request, '|')[0] - 1]
        email = request[str_find(request, '|')[0]:str_find(request, '|')[1] - 1]
        password = hashlib.sha256(request[str_find(request, '|')[1]:].encode()).hexdigest()

        db_conn = sqlite3.connect('bin/userdata.db')
        cursor = db_conn.cursor()

        cursor.execute("SELECT * FROM userdata WHERE username = ? AND email = ? AND password = ?", (username, email,
                                                                                                    password))

        return '< success >'.encode() if cursor.fetchall() else '< failed >'.encode()

    # upload
    elif request.__contains__('< upload >'):
        try:
            client.send('SIZE'.encode())
            size = client.recv(1024).decode()
            client.send('FILENAME'.encode())
            filename = client.recv(1024).decode()
            client.send('DATA'.encode())
            data = client.recv(int(size))

            with open(f'Users/{address}/{filename}', 'wb') as f:
                f.write(data)

            return '< success >'.encode()
        except OSError as exc:
            print(repr(exc))
            return '< failed >'.encode()

    # download
    elif request.__contains__('< download >'):
        client.send('FILENAME'.encode())
        filename = client.recv(1024).decode()

        try:
            size = os.path.getsize(f'Users/{address}/{filename}')
            with open(f'Users/{address}/{filename}', 'rb') as f:
                data = f.read()
        except FileNotFoundError as exc:
            return repr(exc).encode()

        client.send(bytes(size))
        client.send(data)

        return '< success >'.encode()


def remove_client(client, client_log, clients, client_logs):
    client.close()
    clients.remove(client)
    client_logs.remove(client_log)


def main():
    save_hostname('pass')
    is_registered('pass')
    create_user_dir('pass')
    get_all_users()
    check_dir('pass')
    str_find('pass', 'pass')
    remove_client('pass', 'pass', 'pass2', 'pass')


if __name__ == '__main__':
    main()