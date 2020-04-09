import os
import socket
from os import listdir
from os.path import isfile, join
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_mode = ""
data = ""
mode = sys.argv[1]
dest_ip = sys.argv[2]
dest_port = int(sys.argv[3])
# incorrect operation. not 0 or 1
if mode != '0' and mode != '1':
    exit()
msg = sys.argv[1:]
s.connect((dest_ip, dest_port))

files_to_choose = []

# if im in server mode
if mode == "0":
    new_msg = "1 " + sys.argv[4]
    only_files = [f for f in listdir('.') if isfile(join('.', f))]
    files = ','.join(only_files)
    new_msg = new_msg + " " + files  # 0/1_ip_serverPort_clientPort_FileNames
    s.send(new_msg)
    data = s.recv(4096)
    if data == "server":
        client_mode = "server"
# client mode
if mode == "1":
    client_mode = "client"

while not msg == 'quit':

    if client_mode == "server":
        s.close()
        new_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_ip = '0.0.0.0'
        server_port = int(sys.argv[4])
        new_server.bind((server_ip, server_port))
        new_server.listen(5)

        while True:
            conn, addr = new_server.accept()
            # print 'Connection from: ', conn
            reqFile = conn.recv(1024)
            with open(reqFile, 'rb') as file_to_send:
                for data in file_to_send:
                    conn.sendall(data)
            conn.close()

    if client_mode == "client":
        msg = raw_input("Search: ")
        new_msg = "2 " + msg
        s.send(new_msg)
        data = s.recv(4096)
        if msg == 'quit':
            break
        else:
            if data != '-1':
                # data splitting into chunks by ","
                files_to_choose = []
                splited_file_list = data.split(",")

                counter = 1
                for i in range((len(splited_file_list))):
                    # dividing the chunk to 3 string to name_ip_port
                    files_info = splited_file_list[i].split(" ")
                    # input the name_ip_port into list
                    files_to_choose.extend([(files_info[0], (files_info[1], files_info[2]))])
                files_to_choose.sort()
                for j in range(0, len(files_to_choose)):
                    print (j + 1), files_to_choose[j][0]
                choose = raw_input("Choose: ")

                # client chose to quit.
                if choose == 'quit':
                    msg = 'quit'
                if not choose.isdigit():
                    continue
                # checking if client chose a number of one o the files he can choose.
                if int(choose) in range(0, (len(files_to_choose) + 1)):
                    # disconnect from server
                    s.close()
                    # connect to uval
                    s_new = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    new_dest_ip = files_to_choose[int(choose) - 1][1][0]
                    new_desk_port = files_to_choose[int(choose) - 1][1][1]
                    filename = files_to_choose[int(choose) - 1][0]
                    s_new.connect((new_dest_ip, int(new_desk_port)))
                    s_new.send(filename)
                    with open(os.path.join(filename), 'wb') as file_to_write:
                        while True:
                            data_data = s_new.recv(1024)
                            if not data_data:
                                break
                            file_to_write.write(data_data)
                        file_to_write.close()
                    s_new.close()
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.connect((dest_ip, dest_port))
                    #
            if data == '-1':
                choose = raw_input("Choose: ")


s.close()