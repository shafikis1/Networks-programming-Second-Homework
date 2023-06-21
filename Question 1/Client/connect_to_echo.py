import socket, sys
import traceback

import tincanchat

host = sys.argv[-1] if len(sys.argv) > 1 else '127.0.0.1'
port = tincanchat.port

if __name__ == '__main__':

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))

        print('connected to {}:{}'.format(host, port), end="\n")

        break_first_loop = False
        while True:
            try:
                messages = tincanchat.recv_multi_msg(sock)
                #print("messages received", messages)

                for message in messages:
                    #print("current message is ", message)
                    if message.__contains__("!!!END!!!"):
                        message = message.split("!!!END!!!")[1]
                        print(message, end="\n")
                        break_first_loop = True
                        break

                    elif message.__contains__("!!!NO_INPUT!!!"):
                        print(message.split("!!!NO_INPUT!!!")[1], end="\n")
                    else:
                        question = input(message.strip("\x00"))

                        if message == 'q':
                            break_first_loop = True
                            break

                        tincanchat.send_msg(sock, question)
                        #print("sent message: {}".format(question), end="\n")

                if break_first_loop:
                    break
            except Exception:
                print("error", traceback.format_exc())
                break

    except ConnectionError:
        print("socket error")

    finally:
        print("closed connection")
