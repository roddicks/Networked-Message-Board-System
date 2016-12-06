#Main message board controller
import websocket
import threading
import Queue
import time
import logging
import json
import PPMUtil
import WatchdogEventHandler
from subprocess import call

logging.basicConfig()

#Define Message Board Threading class
class MessageBoardThread(threading.Thread):
	def __init__(self, tID, name, queue):
		threading.Thread.__init__(self)
		self.tID = tID
		self.name = name
		self.queue = queue
	def run(self):
		while True:
			printMessages(self.queue)
		
		
#Define Motion Detection Threading class
class MotionThread(threading.Thread):
	def __init__(self, tID, name, ws, handler):
		threading.Thread.__init(self)
		self.tID = tID
		self.name = name
		self.ws = ws
		self.handler = handler
	def run(self):
		observer = WatchdogEventHandler.observer
		observer.schedule(self.handler, "PATH", recursive=True)
		observer.start()
		try:
			while True:
				time.sleep(1)
		except KeyboardInterrupt:
			observer.stop()
		observer.join()
		
#Global variables
messageQueue = Queue.Queue()
messageQueue.put({"_type":"MESSAGE", "msg":"mymessageA"})
messageQueue.put({"_type":"MESSAGE", "msg":"mymessageB"})
messageQueue.put({"_type":"ALERT", "msg":"alertmessage"})
alert_message_buffer = Queue.Queue(3)
updated = False


#Print messages
def printMessages(messageQueue):
	global updated
	update_triggered = False
	for m in iter(messageQueue.get, None):
		msg = m['msg']
		PPMUtil.text_to_ppm(msg + ".ppm", msg)	#Digest message
		#call(["./demo", "-D", "1", m + ".ppm"])
		
		#Put regular messages back in queue
		if not updated and m['_type'] != 'ALERT':
			messageQueue.put(m)
		
		#Prepare to break from queue
		if updated and not update_triggered:
			messageQueue.put(None)
			update_triggered = True
		
		messageQueue.task_done()
		time.sleep(1)
		
		
		
#Websocket callbacks
def onMessage(ws, message):
	print("received")
	
	payload = json.loads(message)
	type = payload['_type']
	data = payload['data']
	
	global messageQueue
	if type == 'ALERT':
		messageQueue.put({'_type':type, 'msg':data})
	else:
		global updated
		updated = True
		for m in data:
			messageQueue.put({'_type':type, 'msg':m})
def onError(ws, error):
	print(error)
def onClose(ws):
	print("Connection closed")
def onOpen(ws):
	print("Connection opened")
	time.sleep(3)
	ws.send("")
	
	
#Create websocket
SERVER_ADDRESS = 'messageboard.fuzzlesoft.ca'
SERVER_PORT = 9011
str = 'ws://' + SERVER_ADDRESS + ":" + str(SERVER_PORT)
ws = websocket.WebSocketApp(str,
	on_message = onMessage,
	on_error = onError,
	on_close = onClose)
ws.on_open = onOpen


#Create motion thread
handler = WatchdogEventHandler.WatchdogEventHandler()
motionThread = MotionThread(1, "motionThread", ws, handler)
motionThread.start()

#Create message thread
messageThread = MessageBoardThread(2, "messageThread", messageQueue)
messageThread.start()

ws.run_forever()