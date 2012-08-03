from asynch_dispatch import *
import threading, Queue
import sys, time

class SearchStream(threading.Thread):
	def __init__(self, sinks = None, callbacks = None, dispatcher=None, autoStart=True):
		threading.Thread.__init__(self)
		self.daemon = True

		self.dispatcher = AsynchDispatch(sinks = sinks, callbacks = callbacks)
		self.sensor_queue = Queue.Queue()
#		self.start()

	def set_seek_source(self):
		self.start()
		
	def run(self):
		while True:
			time.sleep(.75)
			self.get_sensor_data()
			pass
	
	def add_sinks(self, sinks):
		self.dispatcher.add_sinks(sinks)

	def put(self, data):
		self.sensor_queue.put(data)

	def get_sensor_data(self):
		self.dispatcher.dispatch(Message('get_sensor', 'sensor'))

	def search_move(self, data):
		if data[1] < 150 and data[1] > -150 and data[2] < 150 and data[2] > -150:
			self.dispatcher.dispatch(Message('steer_rate', [0,0]))
		elif data[0] <= -50:
			self.dispatcher.dispatch(Message('steer_rate', [70, 30]))
		elif data[0] >= 50:
			self.dispatcher.dispatch(Message('steer_rate', [30, 70]))
		elif data[0] > -50 and data[0] < -20:
			self.dispatcher.dispatch(Message('steer_rate', [30, 15]))
		elif data[0] > 20 and data[0] < 50:
			self.dispatcher.dispatch(Message('steer_rate', [15, 30]))
		elif data[0] == 0:
			self.dispatcher.dispatch(Message('steer_rate', [30, 30]))
		else:
			self.dispatcher.dispatch(Message('steer_rate', [70, 70]))