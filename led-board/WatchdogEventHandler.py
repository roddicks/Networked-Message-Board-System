from watchdog.observers import Observer
from websocket import WebSocketConnectionClosedException
from watchdog.events import FileSystemEventHandler
import datetime

class WatchdogEventHandler(FileSystemEventHandler):
	def __init__(self, ws):
		FileSystemEventHandler.__init__(self)
		self.ws = ws
	def on_created(self, event):
		time = datetime.datetime.now().isoformat()
		try:
			self.ws.send("{\"_type\":\"MOTION\", \"date\":\"" + time + "Z\", \"value\":123, \"device\":\"MESSAGE_BOARD\"}")
		except WebSocketConnectionClosedException:
			pass
		
observer = Observer()