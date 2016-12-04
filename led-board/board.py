#Main message board controller
import Client
import time
import websocket
import Queue
import logging
import json

logging.basicConfig()

messages = ["message1", "message2"]
alert_message_buffer = Queue.Queue(3)

updated = False

#Print messages
def printMessages(messageArr):
	updated = False
	
	for m in messageArr:
		print(m)
		time.sleep(1)
	
	if len(messageArr) == 0:
		time.sleep(1)
	
	if not updated:
		printMessages(messageArr)
	else:
		global messages
		printMessages(messages)
		
		
#Websocket callbacks
def onMessage(ws, message):
	print("received")
	updated = True
	global messages 
	messages = []
	data = json.loads(message)
	for m in data:
		messages.append(m)

def onError(ws, error):
	print(error)
	
def onClose(ws):
	print("Connection closed")
	
def onOpen(ws):
	print("Connection opened")
	time.sleep(3)
	ws.send("[\"hello\", \"world\"]")

SERVER_ADDRESS = 'messageboard.fuzzlesoft.ca'
SERVER_PORT = 9011
str = 'ws://' + SERVER_ADDRESS + ":" + str(SERVER_PORT)

ws = websocket.WebSocketApp(str,
							on_message = onMessage,
							on_error = onError,
							on_close = onClose)
ws.on_open = onOpen
ws.run_forever()
printMessages(messages)
