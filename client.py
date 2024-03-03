# client



import signal

import socket

import echo_util

import threading



HOST = echo_util.HOST

PORT = echo_util.PORT



sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.connect((HOST, PORT))



def handler(signum, frame):

    echo_util.send_msg(sock, "exit")

    exit(0)



def receive():

    while True:

        try:

            msg = echo_util.recv_msg(sock)

            print(msg)

        except:

            sock.close()

            break



def write():

    while True:

        msg = input()

        if not msg:

            continue



        if msg == 'q':

            sock.close()

            break

        try:

            echo_util.send_msg(sock, msg)

        except ConnectionError:

            print('Socket error during communication')

            sock.close()

            print('Closed connection to server\n')

            break





signal.signal(signal.SIGINT, handler)







if __name__ == "__main__":



    receive_thread = threading.Thread(target=receive)

    receive_thread.start()



    write_thread = threading.Thread(target=write)

    write_thread.start()