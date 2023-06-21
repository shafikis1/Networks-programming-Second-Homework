import tincanchat
import threading
from quiz import start

host = tincanchat.host
port = tincanchat.port


if __name__ == '__main__':
    listen_socket = tincanchat.create_listen_socket(host, port)
    address = listen_socket.getsockname()
    print('listening on {}'.format(address))

    while True:
        client_socket, address = listen_socket.accept()

        thread = threading.Thread(target=start
                                  , args=[client_socket]
                                  , daemon=True)

        thread.start()
        print('connection from {}'.format(address))