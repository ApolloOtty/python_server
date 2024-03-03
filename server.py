import echo_util

import threading

import time



HOST = echo_util.HOST

PORT = echo_util.PORT



clients = {}

clientNames={}



client_set = set()

name=""



def handle_client(client_socket, addr):

    echo_util.send_msg(client_socket, "Welcome. Current connections:")
    for i in clients.values():
            echo_util.send_msg(client_socket, i + ", ")
    echo_util.send_msg(client_socket, "\n Choose a name:")




    client_set.add(client_socket)



    while True:

        #Verifica daca numele este deja luat

        name = echo_util.recv_msg(client_socket)

        if name in clients.values():

            echo_util.send_msg(client_socket, "Numele este deja luat. Alege altul:")

        else:

            clients[client_socket] = name

            clientNames[name]=client_socket

            for client in client_set:

                if client != client_socket:

                 try:

                    echo_util.send_msg(client,  str(clients[client_socket]) + " connected")

                 except:

                    client_set.remove(client)

            break





    while True:

        try:

            msg = echo_util.recv_msg(client_socket)



            atr = msg.split(" ")
            if atr[0][1]=="l":
                print("cool")
            atr = msg.split(" ")
            if atr[0][0] == "/" and not (atr[0] in ["/l", "/n", "/w"]):
                echo_util.send_msg(client_socket, "Comanda nu exista!")


            if (msg=="/l"):
                for i in clients.values():
                    echo_util.send_msg(client_socket, i + ", ")

            if atr[0]=="/n" and len(atr) > 1:
                nume_vechi = clients[client_socket]
                if atr[1] in clients.values():
                    echo_util.send_msg(client_socket, "Numele este deja luat. Alege altul:")
                else:
                    clients[client_socket]=atr[1]
                    echo_util.send_msg(client_socket, "Numele a fost schimbat!")
                    for client in client_set:
                        echo_util.send_msg(client,  str(nume_vechi) + " Si-a schimbat numele in {}".format(atr[1]))


            if atr[0] == "/w" and len(atr) > 2:

                nume = atr[1]

                print( "recived:  " + msg)

                #print(client_set)



                for client in clientNames.keys():
                    if client == nume:
                        #print("Corect")
                        aux = atr[2:]
                        #print(aux = atr[3:])

                        mesaj = "Private message from " + str(clients[client_socket]) + ": "

                        for x in aux:

                            mesaj += x + " "

                        print(mesaj)

                        echo_util.send_msg(clientNames[nume], mesaj)

                        

            elif msg and msg != "q":

                print("Received from {}: {}".format(client_socket.getpeername(), msg))

                msg = "<" + str(clients[client_socket]) + ">: " + msg

                #print(client_set)

                for client in client_set:

                    if client != client_socket:

                        try:

                            echo_util.send_msg(client, msg)

                        except:

                            client_set.remove(client)

            else:

                print("{} disconnected.".format(addr))
                clients.pop(client_socket)


                for client in client_set:

                    if client != client_socket:

                        try:

                            echo_util.send_msg(client,  str(client_socket.getpeername()) + " disconnected")

                        except:

                            client_set.remove(client)
                            clients.pop(client_socket)


                client_set.remove(client_socket)

        except (ConnectionError, BrokenPipeError):
            print('{} disconnected.'.format(addr))
            clients.pop(client_socket)
    
            for client in client_set:
                if client != client_socket:
                    try:
                        echo_util.send_msg(client,  str(client_socket.getpeername()) + " disconnected")
                    except:
                        client_set.remove(client)
                        clients.pop(client_socket)
            
            client_set.remove(client_socket)






if __name__ == "__main__":

    listener = echo_util.create_listen_socket(HOST, PORT)

    print("Server is on...")

    while True:

        client, addr = listener.accept()

        print("{} connected.".format(addr))

        thread = threading.Thread(target=handle_client, args=[client, addr], daemon=True)

        thread.start()