# Author: Jehu Alejandro Nunez
# Date: 10/03/2020
# CS4375 Theory of Operating Systems
# Eric Freudenthal
# File Transfer Lab

import os
import socket, sys

PATH_DIRECTORY = "./lib"
sys.path.append(PATH_DIRECTORY)  # for params
import params

HOST = "127.0.0.1"
filePath = "./receiveFiles"

def write_file(filename, byte, conn):

    file_writer = open(filename, 'wb')  # create file to write

    # send and get data
    i = 0
    data = ''
    while i < byte:
        data = conn.recv(1024)
        if not data:
            break
        i += len(data)

    file_writer.write(data)
    file_writer.close()
    print("file %s received" % filename)


def get_byte_size(conn):
    data_byte = conn.recv(1024)
    return data_byte.decode()


def server():
    switchesVarDefaults = (
        (('-l', '--listenPort'), 'listenPort', 50001),
        (('-d', '--debug'), "debug", False),  # boolean (set if present)
        (('-?', '--usage'), "usage", False),  # boolean (set if present)
    )

    paramMap = params.parseParams(switchesVarDefaults)
    debug, listenPort = paramMap['debug'], paramMap['listenPort']

    if paramMap['usage']:
        params.usage()

    bind_addr = (HOST, listenPort)

    # Socket listener
    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # associating socket with host and port number
    listen_socket.bind(bind_addr)
    listen_socket.listen(5)
    print("listening on: ", bind_addr)

    # connection and tuple for client address (host, port)
    conn, addr = listen_socket.accept()
    print("connection rec'd from", addr)

    # move to directory to receive files
    os.chdir(filePath)

    while True:
        # receive file name first
        data = conn.recv(1024)
        d = data.decode()

        # file byte size
        data_byte = get_byte_size(conn)

        # if filename was provided, write it
        if d:
            write_file(d, int(data_byte), conn)

        if not data:
            break
        conn.sendall(data)


if __name__ == "__main__":
    server()