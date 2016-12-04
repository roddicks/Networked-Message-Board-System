#Main message board controller
import websocket
import threading
import Queue
import time
import logging
import json

logging.basicConfig()

#Define Threading class
class MyThread(threading.Thread):
	def __init__(self, tID, name, queue):
		threading.Thread.__init__(self)
		self.tID = tID
		self.name = name
		self.queue = queue
	def run(self):
		printMessages(messages)
		
		
#Global variables
messages = ["message1", "message2"]
alert_message_buffer = Queue.Queue(3)
updated = False


#Print messages
def printMessages(messageArr):
	global updated
	updated = False
	for m in messageArr:
		print(m)
		time.sleep(1)
	
	if len(messageArr) == 0:
		time.sleep(1)
	
	if not updated:
		printMessages(messageArr)
	else:
		print("messages were updated")
		global messages
		printMessages(messages)
		
		
#Websocket callbacks
def onMessage(ws, message):
	print("received")
	global updated
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
	
	
#Create websocket
SERVER_ADDRESS = 'messageboard.fuzzlesoft.ca'
SERVER_PORT = 9011
str = 'ws://' + SERVER_ADDRESS + ":" + str(SERVER_PORT)
ws = websocket.WebSocketApp(str,
	on_message = onMessage,
	on_error = onError,
	on_close = onClose)
ws.on_open = onOpen


#Create message thread
messageThread = MyThread(1, "msgThread", alert_message_buffer)
messageThread.start()

ws.run_forever()