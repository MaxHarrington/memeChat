import socket
import threading
import socketserver
import queue
import client
import time
import re

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
	def __init__(self, server_address, RequestHandlerClass, bind_and_activate=True, 
		queue=None):

		# initiates the queue shared across threads
		self.queue = queue

		socketserver.TCPServer.__init__(self, server_address, RequestHandlerClass, 
		bind_and_activate=bind_and_activate)

class threadedMessagingServer(socketserver.BaseRequestHandler):

	def serveMessages(self):

		while not server.queue.empty():
			try:

				topMessage = server.queue.get()

				sender = topMessage[0]
				destination = topMessage[1]
				message = topMessage[2]

				print("{} {} {}".format(sender, destination, message))


			except OSError:
				print("Disconnected")
		return

	def handle(self):
		fullMessage = ""
		message = False
		address = self.request.getpeername()

		# recieves data until end of message string recieved
		while True:
			incoming = ""

			incoming = str(self.request.recv(1024), 'ascii')
			fullMessage += incoming

			if incoming[-5:] == "!#E#!":
				message = True
				break

			if fullMessage[-10:] == "!#N#!!#E#!":
				print("succ")
				message = False
				messaging_serve = threading.Thread(target = self.serveMessages)
				messaging_serve.start()
				messaging_serve.join()

		if message:

			# gathers the username from the incoming data
			# splits up the address into IP and port for ease of use
			username = fullMessage.split("!#U#!")
			username = username[0]
			user = (username, address[0], str(address[1]))

			# splits the headers up into the list
			# each message has username of sender, destination, and ending
			message = re.split('[!#|U|D|E]', fullMessage)
			message = list(filter(None, message))

			print("test2")

			server.queue.put(message)

if __name__ == "__main__":

	q = queue.Queue()
	host, port = "localhost", 0
	active = True

	server = ThreadedTCPServer((host, port), threadedMessagingServer, queue = q)
	ip, port = server.server_address

	# start a thread with the server -- that thread will then start one
	# more thread for each request
	server_thread = threading.Thread(target = server.serve_forever)
	server_thread.daemon = True
	server_thread.start()

	c = client.messagingClient("testBest1", ip, port)
	c2 = client.messagingClient("testBest1", ip, port)

	c.checkMessages()
	c.sendMessage("testBest3", "test Mess")

	c2.checkMessages()
	c2.sendMessage("testBest1", "test Mess")

	server.shutdown()
