from asynch_dispatch import *
import threading, Queue
import sys, time

class SearchStream(threading.Thread):
	def __init__(self, sinks = None, callbacks = None, dispatcher=None, autoStart=True):
		threading.Thread.__init__(self)
		self.daemon = True

		self.dispatcher = AsynchDispatch(sinks = sinks, callbacks = callbacks)
		self.sensor_queue = Queue.Queue()
		self._stop = threading.Event()

#		self.start()

	def set_seek_source(self):
		self._stop.clear()
		self.start()
		
	def run(self):
		while not self.stopped():
			time.sleep(.1)
			self.get_sensor_data()
			pass

	def stop(self):
		self._stop.set()
		
	def stopped(self):
		return self._stop.isSet()

	def add_sinks(self, sinks):
		self.dispatcher.add_sinks(sinks)

	def put(self, data):
		self.sensor_queue.put(data)

	def get_sensor_data(self):
		self.dispatcher.dispatch(Message('get_sensor', 'sensor'))

	def search_move(self, data):
		if data[1] < 150 and data[1] > -150 and data[2] < 150 and data[2] > -150 and data[0] < 20 and data[0] > -20:
			self.dispatcher.dispatch(Message('steer_rate', [0,0]))
		elif data[0] == 1400:
			self.dispatcher.dispatch(Message('steer_rate', [40, 70]))
		elif data[0] == -1400:
			self.dispatcher.dispatch(Message('steer_rate', [70, 40]))
		elif data[0] == 1050:
			self.dispatcher.dispatch(Message('steer_rate', [30, 70]))
		elif data[0] == -1050:
			self.dispatcher.dispatch(Message('steer_rate', [70, 30]))
		elif data[0] == 700:
			self.dispatcher.dispatch(Message('steer_rate', [20, 70]))
		elif data[0] == -700:
			self.dispatcher.dispatch(Message('steer_rate', [70, 20]))
		elif data[0] <= -50:
			self.dispatcher.dispatch(Message('steer_rate', [70, 0]))
		elif data[0] >= 50:
			self.dispatcher.dispatch(Message('steer_rate', [0, 70]))
		elif data[0] > -50 and data[0] < -20:
			self.dispatcher.dispatch(Message('steer_rate', [50, 15]))
		elif data[0] > 20 and data[0] < 50:
			self.dispatcher.dispatch(Message('steer_rate', [15, 60]))
		elif data[0] == 0:
			self.dispatcher.dispatch(Message('steer_rate', [50, 50]))
		else:
			self.dispatcher.dispatch(Message('steer_rate', [70, 70]))