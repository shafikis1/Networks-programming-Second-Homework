import socket

host = '127.0.0.1'
port = 4040
encoding = 'utf-8'
message_end = "!!!111!!!"

def create_listen_socket(host, port):

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))
    sock.listen(100)

    return sock

def recv_msg(sock):
    #print("in receive waiting")

    data = bytearray()
    message = ''

    while not message:
        received_data = sock.recv(4096)


        if not received_data:
            raise ConnectionError()

        data = data + received_data

        if b'\0' in received_data:
            message = data.rstrip(b'\0')

    message = message.decode(encoding)
    message = message.strip(message_end)

    return message

def recv_multi_msg(sock):
    #print("in receive multiiiiii")

    data = bytearray()
    message = ''

    while not message:
        received_data = sock.recv(4096)


        if not received_data:
            raise ConnectionError()

        data = data + received_data

        if b'\0' in received_data:
            message = data.rstrip(b'\0')

    message = message.decode(encoding)
    messages = message.split(message_end)

    return list(filter(None, messages))

def prep_msg(message):

    message += '\0'
    return message.encode(encoding)

def send_msg(sock, message):
    #print("in sending a message", message)
    sock.sendall(prep_msg(message+message_end))
