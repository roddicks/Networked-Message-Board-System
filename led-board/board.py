#Main message board controller
import Queue

messages = [];
alert_message_buffer = Queue.Queue(3)	#Limit to 3 alert messages

#Setup
#Subscribe to message board server

