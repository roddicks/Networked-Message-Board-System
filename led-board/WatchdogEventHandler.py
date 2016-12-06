from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import datetime

class WatchdogEventHandler(watchdog.events.FileSystemEventHandler):
	def __init__(self, ws):
		watchdog.events.FileSystemEventHandler.__init(self)
		self.ws = ws
	def on_any_event(event):
		time = datetime.datetime.now().isoformat()
		self.ws.send("{\"_type\": \"MOTION\", \"date\": \"" + time + "\", \"value\": \"DETECTED\", \"device\": \"MESSAGE_BOARD\"")
		
observer = Observer()