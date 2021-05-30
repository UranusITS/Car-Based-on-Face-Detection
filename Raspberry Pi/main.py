import socket

if __name__ == '__main__':
    HOST = '192.168.1.104'
    PORT = 1919
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, PORT))
    sock.listen(1)
    while True:
        connection, address = sock.accept()
        while True:
            try:
                connection.settimeout(10)
                buf = connection.recv(1024)
                if buf:
                    print(buf.decode('ASCII'))
            except socket.timeout:
                print('time out')
        connection.close()
