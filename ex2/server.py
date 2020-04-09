import socket, threading
from os import listdir
from os.path import isfile, join
import sys

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_ip = '0.0.0.0'
server_port = int(sys.argv[1])
server.bind((server_ip, server_port))
server.listen(5)
file_name_list = []  # data structure - key:file_name, value:port (key,port)
name_ip_port = ""
client_mode = ""

while True:
    client_socket, client_address = server.accept()
    # print 'Connection from: ', client_address
    data = client_socket.recv(1024)
    data_split = data.split(" ")

    while not data == '':
        # uval wants to send files
        if data_split[0] == "1":
            client_mode = "server"
            file_names = data_split[2].split(",")
            for name in file_names:
                file_name_list.extend([(name, (client_address[0], data_split[1]))])
            # ACK
            client_socket.send(client_mode)
        # uval wants to search for files
        elif data_split[0] == "2":
            # flag to know if there is nothing to send to client.
            empty_list = 0
            for key in file_name_list:
                is_sub = key[0].find(data_split[1])
                if is_sub != -1:
                    if name_ip_port == "":
                        name_ip_port = key[0] + " " + key[1][0] + " " + str(key[1][1])
                    else:
                        name_ip_port = name_ip_port + "," + key[0] + " " + key[1][0] + " " + str(key[1][1])
                else:
                    empty_list = empty_list + 1
            if data_split[1] == "":
                client_socket.send('-1')
            # checking if there is nothing to send to client.
            if empty_list != len(file_name_list):
                client_socket.send(name_ip_port)
            else:
                # flag nothing to send.
                client_socket.send('-1')
        # any other input just continue - it's not a valid input
        else:
            print "Bad Input"
        name_ip_port = ""
        # getting message from client.
        data = client_socket.recv(1024)
        data_split = data.split(" ")

    client_mode = ""
    # print 'Client disconnected'
    client_socket.close()