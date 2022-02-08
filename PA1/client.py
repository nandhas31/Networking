import socket
import threading
import sys 
import argparse
import atexit
import time

#TODO: Implement all code for your server here
PORT = None
HOST = '127.0.0.1'
s_global = None
# Use sys.stdout.flush() after print statemtents

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Join a chat server on a specified port")
	parser.add_argument('-port', dest = 'port', required=True, type=int)
	parser.add_argument('-username', dest = 'username', required=True)
	parser.add_argument('-password', dest = 'password', required=True)
	parser.add_argument('-join', action = 'store_true')
	password, PORT, join = parser.parse_args().password, parser.parse_args().port,parser.parse_args().join

def recieve_messages(s):
	while(True):
		time.sleep(5)
		print(s)		

def write_messages(s):
	while(True):
		time.sleep(5)
		s.sendall(b'hello')		

def close_socket():
	s_global.close()

atexit.register(close_socket)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s_global = s
s.connect((HOST, PORT))
print(s)
reader = threading.Thread(target=recieve_messages, args=(s,))
reader.start()
writer= threading.Thread(target=write_messages, args=(s,))
writer.start()

