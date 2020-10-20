# Author: Jehu Alejandro Nunez
# Date: 10/017/2020
# CS4375 Theory of Operating Systems
# Eric Freudenthal
# File Transfer Lab - Threads

import os
import re
import socket
import sys

import os
import re
import socket
import sys

DIRECTORY_PATH = "./lib"
sys.path.append(DIRECTORY_PATH)  # for params
import params
from EncapFramedSock import EncapFramedSock

PATH_FILES = "sendFiles/"
CONFIRM_MSG = "File %s received by the server"
REJECT_MSG = "File %s could not be received by the server. Try again"
EMPTY_MSG = "File %s was empty. Try again"


def client():
    switchesVarDefaults = (
        (('-s', '--server'), 'server', "127.0.0.1:50001"),
        (('-d', '--debug'), "debug", False),  # boolean (set if present)
        (('-?', '--usage'), "usage", False),  # boolean (set if present)
    )

    paramMap = params.parseParams(switchesVarDefaults)

    server, usage, debug = paramMap["server"], paramMap["usage"], paramMap["debug"]

    if usage:
        params.usage()

    try:
        serverHost, serverPort = re.split(":", server)
        serverPort = int(serverPort)
    except:
        print("can't parse server:port from '%s'" % server)
        sys.exit(1)

    addr_port = (serverHost, serverPort)

    # create socket object
    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_socket.connect(addr_port)

    # create encapsulated socket
    encap_socket = EncapFramedSock((listen_socket, addr_port))

    while True:
        filename = input("Enter the file to be sent: ")
        filename.strip()

        if filename == "exit":
            sys.exit(0)
        else:
            if not filename:
                continue
            elif os.path.exists(PATH_FILES + filename):
                # open file and read
                file = open(PATH_FILES + filename, "rb")
                file_content = file.read()

                # verify file is not empty before sending
                if len(file_content) < 1:
                    print(EMPTY_MSG % filename)
                    continue

                # send file contents to server
                encap_socket.send(filename, file_content, debug)

                # check if server received file
                status = encap_socket.get_status()
                status = int(status.decode())

                # successful transfer
                if status:
                    print(CONFIRM_MSG % filename)
                    #sys.exit(0)
                # failed transfer
                else:
                    print(REJECT_MSG % filename)
                    sys.exit(1)

            # file not found
            else:
                print("ERROR: file %s not found. Try again" % filename)


if __name__ == "__main__":
    client()