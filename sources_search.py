from asynch_dispatch import *
import threading, Queue
import sys, time

class SearchStream(threading.Thread):
	def __init__(self, sinks = None, callbacks = None, dispatcher=None, autoStart=True):
		threading.Thread.__init__(self)
		self.daemon = True

		self.dispatcher = AsynchDispatch(sinks = sinks, callbacks = callbacks)
		self.sensor_queue = Queue.Queue()
		
		self.start()

	def run(self):
		while True:
			time.sleep(5)
			self.get_sensor_data()
			pass
	
	def add_sinks(self, sinks):
		self.dispatcher.add_sinks(sinks)

	def put(self, data):
		self.sensor_queue.put(data)

	def get_sensor_data(self):
		self.dispatcher.dispatch(Message('get_sensor', 'sensor'))
		
	def search_move(self, data):
		print data