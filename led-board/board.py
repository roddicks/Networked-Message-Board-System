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
import datetime

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
	def __init__(self, tID, name, handler):
		threading.Thread.__init__(self)
		self.tID = tID
		self.name = name
		self.handler = handler
	def run(self):
		observer = WatchdogEventHandler.observer
		observer.schedule(self.handler, "/home/pi/message-board-client/Networked-Message-Board-System/led-board", recursive=True)
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
brightness = 50


#Print messages
def printMessages(messageQueue):
	global updated
	update_triggered = False
	for m in iter(messageQueue.get, None):
		msg = m['msg']
		PPMUtil.text_to_ppm(msg + ".ppm", msg)	#Digest message
		call(["./demo", "-t", "3", "-D", "1", msg + ".ppm"])
		time.sleep(3)
		
		#Put regular messages back in queue
		if not updated and m['_type'] != 'ALERT':
			messageQueue.put(m)
		
		#Prepare to break from queue
		if updated and not update_triggered:
			messageQueue.put(None)
			update_triggered = True
		
		messageQueue.task_done()
		
		
		
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
		time = datetime.datetime.now().isoformat()
		count = str(len(data))
		ws.send("{\"_type\":\"MESSAGE_COUNT\", \"date\":\"" + time + "Z\", \"value\":" + count + ", \"device\":\"MESSAGE_BOARD\"}")
def onError(ws, error):
	print(error)
def onClose(ws):
	print("Connection closed")
def onOpen(ws):
	print("Connection opened")
	time.sleep(3)
	
	
#Create websocket
SERVER_ADDRESS = 'messageboard.fuzzlesoft.ca'
SERVER_PORT = 9011
s = 'ws://' + SERVER_ADDRESS + ":" + str(SERVER_PORT)
ws = websocket.WebSocketApp(s,
	on_message = onMessage,
	on_error = onError,
	on_close = onClose)
ws.on_open = onOpen


#Create motion thread
handler = WatchdogEventHandler.WatchdogEventHandler(ws)
motionThread = MotionThread(1, "motionThread", handler)
motionThread.start()

#Create message thread
messageThread = MessageBoardThread(2, "messageThread", messageQueue)
messageThread.start()

ws.run_forever()