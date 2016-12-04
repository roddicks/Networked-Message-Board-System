from autobahn.twisted.websocket import WebSocketClientProtocol

class Client(WebSocketClientProtocol):
	
	def __init__(self, onMessageReceived):
		self.onMessageReceived = onMessageReceived
	
	def onConnect(self, response):
		print("Server connected: {0}".format(response.peer))
	
	def onOpen(self):
		print("WebSocket connection open.")
		
		self.sendMessage(u"Hello!".encode('utf8'))
	
	def onMessage(self, payload, isBinary):
		if isBinary:	#Should not receive binary messages
			return
			
		self.onMessageReceived(payload)
	
	def onClose(self, wasClean, code, reason):
		print("WebSocket connection closed: {0}".format(reason))
	
