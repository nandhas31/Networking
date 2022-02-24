# CS 3251 PA1 - Nandha and Nithik

from calendar import week
import socket
import threading
import sys 
import os
import argparse
import datetime
import traceback


#TODO: Implement a client that connects to your server to chat with other clients here
# Use sys.stdout.flush() after print statemtents
start = None
PORT = None
password = None
HOST = ''


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Start a chat server on a specified port")
	parser.add_argument('-start', action = 'store_true')
	parser.add_argument('-port', dest = 'port', required=True, type=int)
	parser.add_argument('-passcode', dest = 'passcode', required=True)
	password, PORT, start = parser.parse_args().passcode, parser.parse_args().port,parser.parse_args().start
	if len(password) > 5 or not password.isalnum():
		print("Enter a valid password")
		sys.exit(0)


def time(hours):
	t = datetime.datetime.now() + datetime.timedelta(hours=hours)
	weekday = t.isoweekday()
	month = t.month
	day = t.day
	year = t.year
	time = str(t.time()).split(".")[0]

	weekdays = {1: "Mon", 2: "Tue", 3: "Wed", 4: "Thu", 5: "Fri", 6: "Sat", 7: "Sun"}
	months = {1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun", 7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"}
	d = weekdays[weekday] + " " + months[month] + " " + str(day) + " " + str(time) + " " + str(year)
	return d


connections = {}
t = time(0)
shortcuts = {":)": "[feeling happy]", ":(": "[feeling sad]", ":mytime": str(t), ":+1hr": str(time(1))}
def handle_connection(conn):
	username, userpass = conn.recv(1024).decode().split(":")
	if password != userpass:
		conn.sendall("Incorrect passcode".encode())
		conn.close()
		return
	conn.sendall('Connected to {} on port {}'.format('127.0.0.1', PORT).encode())
	connections[username] = conn
	print('{} joined the chatroom'.format(username))
	sys.stdout.flush()
	for user in connections:
		if user != username:
			connections[user].sendall("{} joined the chatroom".format(username).encode())
	sys.stdout.flush()
	while True:
		try:
			# conn.sendall(b'')
			data = conn.recv(1024).decode()
			if not data or data == ':Exit':
				print("{} left the chatroom".format(username))
				for user in connections:
					if user != username:
						connections[user].sendall("{} left the chatroom".format(username).encode())
				sys.stdout.flush()
				del connections[username]
				conn.close()
				return
			else: 
				if data in shortcuts:
					data = shortcuts[data]
				print(username + ": " + data)
				sys.stdout.flush()
				for user in connections:
					if user != username:
						connections[user].sendall((username + ": " + data).encode())
		except:
			traceback.print_exc()
			break 


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


