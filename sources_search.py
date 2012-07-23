from asynch_dispatch import *
import threading, Queue
import sys, time

class SearchStream(threading.Thread):
	def __init__(self, sinks = None, callbacks = None, dispatcher=None, autoStart=True):
		threading.Thread.__init__(self)
		self.daemon = True

		self.dispatcher = AsynchDispatch(sinks = sinks, callbacks = callbacks)

		if autoStart:
			self.start()

	def run(self):
		while(True):
			time.sleep(20)
			self.dispatcher.dispatch(Message('get_sensor', 'sensor'))
			
			if not self.sensor_queue.empty():
				data = self.sensor_queue.get()

				self.search_move(data)

			pass

	def add_sinks(self, sinks):
		self.dispatcher.add_sinks(sinks)

	def put(self, data):
		self.sensor_queue.put(data)

	def search_move(self, data):
		print data