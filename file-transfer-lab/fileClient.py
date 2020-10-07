# Author: Jehu Alejandro Nunez
# Date: 10/03/2020
# CS4375 Theory of Operating Systems
# Eric Freudenthal
# File Transfer Lab

import os
import re
import socket
import sys

DIRECTORY_PATH = "./lib"
sys.path.append(DIRECTORY_PATH)  # for params
import params

filePath = "sendFiles/"


def client():
    switchesVarDefaults = (
        (('-s', '--server'), 'server', "127.0.0.1:50001"),
        (('-d', '--debug'), "debug", False),  # boolean (set if present)
        (('-?', '--usage'), "usage", False),  # boolean (set if present)
    )

    progname = "framedClient"
    paramMap = params.parseParams(switchesVarDefaults)

    server, usage, debug = paramMap["server"], paramMap["usage"], paramMap["debug"]

    if usage:
        params.usage()

    try:
        serverHost, serverPort = re.split(":", server)
        serverPort = int(serverPort)
    except:
        print("Can't parse server:port from '%s'" % server)
        sys.exit(1)

    addr_port = (serverHost, serverPort)

    # create socket object
    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_socket.connect(addr_port)

    while True:
        filename = input("> ")
        filename.strip()

        if filename == "exit":
            sys.exit(0)
        else:
            if not filename:
                continue
            elif os.path.exists(filePath + filename):
                # send file name
                listen_socket.sendall(filename.encode())
                file_content = open(filePath + filename, "rb")

                # send file size
                listen_socket.sendall(str(os.stat(filePath + filename).st_size).encode())

                # send file content
                while True:
                    data = file_content.read(1024)
                    listen_socket.sendall(data)
                    if not data:
                        break
                file_content.close()
            else:
                print("File %s not found" % filename)


if __name__ == "__main__":
    client()