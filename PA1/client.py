# CS 3251 PA1 - Nandha and Nithik

import socket
import threading
import sys 
import os
import argparse
import atexit
import time

# TODO: Implement all code for your server here
# Use sys.stdout.flush() after print statemtents
PORT = None
HOST = '127.0.0.1'
s_global = None
username = "DEFAULT_USERNAME"

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Join a chat server on a specified port")
	parser.add_argument('-join', action = 'store_true')
	parser.add_argument('-host', dest = 'host', required=True)
	parser.add_argument('-port', dest = 'port', required=True, type=int)
	parser.add_argument('-username', dest = 'username', required=True)
	parser.add_argument('-passcode', dest = 'passcode', required=True)

	username, HOST = parser.parse_args().username, parser.parse_args().host
	password, PORT, join = parser.parse_args().passcode, parser.parse_args().port,parser.parse_args().join
	if len(username) > 8:
		print("Enter a valid username")
		os._exit(0)

def recieve_messages(s):
	while(True):
		data = s.recv(1024).decode()
		if not data:
			# print("You are no longer in the chatroom")
			os._exit(0)
		print(data)		
		sys.stdout.flush()

def write_messages(s):
	while(True):
		message = input()
		s.sendall(message.encode())		

def close_socket():
	s_global.close()

atexit.register(close_socket)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s_global = s
s.connect((HOST, PORT))


s.sendall((username + ":" + password).encode())

reader = threading.Thread(target=recieve_messages, args=(s,))
reader.start()
writer = threading.Thread(target=write_messages, args=(s,))
writer.start()