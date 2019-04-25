# !/usr/bin/env python3
# -*- coding: utf-8 -*-

# simple.py

import socket


def fibonacci(i):
    # print(i)
    if i == 0:
        return 0
    elif i == 1:
        return 1
    else:
        return fibonacci(i - 1) + fibonacci(i - 2)


# Create a server socket

serverSocket = socket.socket()

print("Server socket created.")

# Associate the server socket with the IP and Port

ip = "127.0.0.1"

port = 35491

serverSocket.bind((ip, port))

print("Server socket bound with with ip {} port {}.".format(ip, port))

# Make the server listen for incoming connections

serverSocket.listen()

# Server incoming connections "one by one"

count = 0

while (True):

    (clientConnection, clientAddress) = serverSocket.accept()

    count = count + 1

    print("Accepted {} connections so far".format(count))

    # read from client connection

    data = clientConnection.recv(1024)

    print("Dato puro: {} .".format(data))
    # print(data)

    n = data.decode()

    print("Dato codificato: " + n + ".")

    res = fibonacci(int(n))

    toByte = str.encode(str(res))

    clientConnection.send(toByte)

    print("Dato inviato.")

    clientConnection.close()

    print("Connection closed.\n\n")
