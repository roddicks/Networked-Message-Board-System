#Main message board controller
import Queue
import Client
import time
from twisted.internet import reactor
from autobahn.twisted.websocket import WebSocketClientFactory

messages = ["message 1", "message 2"];
updated = False
alert_message_buffer = Queue.Queue(3)	#Limit to 3 alert messages

SERVER_ADDRESS = 'messageboard.fuzzlesoft.ca'
SERVER_PORT = 9011

#Setup

#Subscribe to message board server
factory = WebSocketClientFactory(SERVER_ADDRESS + ":" + SERVER_PORT)
protocol = Client.Client(onMessagesReceived)
factory.protocol = protocol

reactor.connectTCP(SERVER_ADDRESS, SERVER_PORT, factory)
reactor.run()

#Set up message board
def onMessagesReceived(payload):
	print payload

def printMessages(messages):
	for(m in messages):
		print m
		time.sleep(0.25)
	
	if not updated
		printMessages(messages)
	
	return
		



