import socket
import time
from wheels_manager import WheelsManager

if __name__ == '__main__':
    # HOST = '192.168.1.104'
    HOST = '172.18.22.12'
    PORT = 1919
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, PORT))
    sock.listen(1)
    wheels_manager = WheelsManager()
    while True:
        connection, address = sock.accept()
        while True:
            try:
                connection.settimeout(10)
                buf = connection.recv(1024)
                if buf:
                    opt = buf.decode('ASCII')
                    print(opt)
                    if opt == 'accel':
                        wheels_manager.accelerate()
                    elif opt == 'decel':
                        wheels_manager.decelerate()
                    elif opt == 'left':
                        wheels_manager.left()
                    elif opt == 'right':
                        wheels_manager.right()
            except socket.timeout:
                print('time out')
            except ConnectionResetError:
                print('disconnected')
                connection.close()
        connection.close()
