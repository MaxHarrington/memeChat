import socket

class messagingClient():

	def __init__(self, username, ip, port):
		self.username = username + "!#U#!"
		self.ip = ip
		self.port = port

		# creates a socket object
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	
	def sendMessage(self, destination, message):
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		self.s.connect((self.ip, self.port))

		destination += "!#D#!"
		message += "!#E#!"

		self.s.sendall(bytes(self.username, 'ascii'))
		self.s.sendall(bytes(destination,'ascii'))
		self.s.sendall(bytes(message, 'ascii'))

		self.s.close()

	def checkMessages(self):
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		self.s.connect((self.ip, self.port))
		self.s.sendall(bytes('!#N#!!#E#!', 'ascii'))
