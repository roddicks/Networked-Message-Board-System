#Main message board controller
import websocket
import threading
import Queue
import time
import logging
import json
import PPMUtil
import WatchdogEventHandler
import subprocess
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
		observer.schedule(self.handler, "/home/pi/motion-snapshots/", recursive=True)
		observer.start()
		try:
			while True:
				time.sleep(1)
		except KeyboardInterrupt:
			observer.stop()
		observer.join()
		
		
#Global variables
messageQueue = Queue.Queue()
updated = False
brightness = 50


#Print messages
def printMessages(messageQueue):
	global updated
	updated = False
	update_triggered = False
	
	if messageQueue.empty():
		messageQueue.put(None)
	
	for m in iter(messageQueue.get, None):
		msg = m['msg']
		print(msg)
		
		#Put regular messages back in queue
		if not updated:
			PPMUtil.text_to_ppm(msg + ".ppm", msg)	#Digest message
			try:
				subprocess.call(["/home/pi/board-test/rpi-rgb-led-matrix/examples-api-use/demo", "-t 10", "-D 1", "--led-brightness=" + str(brightness), "--led-rows=16", msg + ".ppm"])
			except Exception:
				pass
				
			if m['_type'] != 'ALERT' and not updated:
				messageQueue.put(m)
		
		#Prepare to break from queue
		if updated and not update_triggered:
			messageQueue.put(None)
			update_triggered = True
		
		messageQueue.task_done()
	time.sleep(0.5)
		
		
#Websocket callbacks
def onMessage(ws, message):
	print("received")
	
	payload = json.loads(message)
	type = payload['_type']
	data = payload['data']
	global messageQueue
	if type == 'ALERT':
		messageQueue.put({'msg':data, '_type':type})
	else:
		global updated
		updated = True
		while updated:
			time.sleep(0.25)
		for m in data:
			messageQueue.put({'msg':m, '_type':type})
		#Send message count to server
		ayy = datetime.datetime.now().isoformat()
		count = str(len(data))
		ws.send("{\"_type\":\"MESSAGE_COUNT\", \"date\":\"" + ayy + "Z\", \"value\":" + count + ", \"device\":\"MESSAGE_BOARD\"}")
def onError(ws, error):
	print(error)
def onClose(ws):
	print("Connection closed")
def onOpen(ws):
	print("Connection opened")
	
	
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
time.sleep(1)

ws.run_forever()