from watchdog.observers import Observer
from websocket import WebSocketConnectionClosedException
from watchdog.events import FileSystemEventHandler
import datetime
import time

class WatchdogEventHandler(FileSystemEventHandler):
	def __init__(self, ws, callback):
		FileSystemEventHandler.__init__(self)
		self.ws = ws
		self.callback = callback
	def on_created(self, event):
		self.callback(time.time())
		borktime = datetime.datetime.now().isoformat()
		try:
			self.ws.send("{\"_type\":\"MOTION\", \"date\":\"" + borktime + "Z\", \"value\":1, \"device\":\"MESSAGE_BOARD\"}")
		except WebSocketConnectionClosedException:
			pass
			
observer = Observer()
