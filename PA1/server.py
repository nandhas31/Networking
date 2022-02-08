import socket
import threading
import sys 
import argparse
import time
import traceback


#TODO: Implement a client that connects to your server to chat with other clients here
start = None
PORT = None
password = None
HOST = ''



# Use sys.stdout.flush() after print statemtents

def handle_connection(conn):
	username = 'DEFAULT_USERNAME'
	print('{} joined the chatroom'.format(username))
	sys.stdout.flush()
	while True:
		try:
			conn.sendall(b'')
			data = conn.recv(1024)
			if data: 
				print(data, conn)
				sys.stdout.flush()
			else:
				print("{} left the chatroom".format(username))
				sys.stdout.flush()
				conn.close()
				break
		except:
			traceback.print_exc()
			break 


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Start a chat server on a specified port")
	parser.add_argument('-port', dest = 'port', required=True, type=int)
	parser.add_argument('-password', dest = 'password', required=True)
	parser.add_argument('-start', action = 'store_true')
	password, PORT, start = parser.parse_args().password, parser.parse_args().port,parser.parse_args().start


if start:
	print("Server started on port {}. Accepting connections".format(PORT))

	sys.stdout.flush()

	serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	serverSocket.bind((HOST,PORT))
	while(True):
		serverSocket.listen()
		conn, addr = serverSocket.accept()
		thread = threading.Thread(target=handle_connection, args=(conn,))
		thread.start()