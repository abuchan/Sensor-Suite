from asynch_dispatch import *
import threading, Queue
import sys

class SourcesStream(threading.Thread):
	def __init__(self, sinks = None, callbacks = None, dispatcher=None, autoStart=True):
		threading.Thread.__init__(self)
		self.daemon = True

		self.dispatcher = AsynchDispatch(sinks = sinks, callbacks = callbacks)
		self.sources_list = []
		self.new_source = []
		self.source_queue = Queue.Queue()
		
		self.start()

	def run(self):
		while(True):
			if not self.source_queue.empty():
				entry = self.source_queue.get()
			
				if entry[0] == 'Light':
					self.light_source(entry[0], entry[1], entry[2], entry[3], entry[4])
				elif entry[0] == 'Chemical':
					self.chemical_source(entry[0], entry[1], entry[2], entry[3], entry[4])
				elif entry[0] == 'Radioactive':
					self.radioactive_source(entry[0], entry[1], entry[2], entry[3], entry[4])
				elif entry[0] == 'Humidity':
					self.humidity_source(entry[0], entry[1], entry[2], entry[3], entry[4])
				elif entry[0] == 'Sound':
					self.sound_source(entry[0], entry[1], entry[2], entry[3], entry[4])
				else:
					pass

	def add_sinks(self, sinks):
		self.dispatcher.add_sinks(sinks)

	def put(self, data):
		self.source_queue.put(data)

	def update(self, type, x_pos, y_pos, z_pos, time):
		if type == 'Light':
			self.light_source(type, x_pos, y_pos, z_pos, time)
		elif type == 'Chemical':
			self.chemical_source(type, x_pos, y_pos, z_pos, time)
		elif type == 'Radioactive':
			self.radioactive_source(type, x_pos, y_pos, z_pos, time)
		elif type == 'Humidity':
			self.humidity_source(type, x_pos, y_pos, z_pos, time)
		elif type == 'Sound':
			self.sound_source(type, x_pos, y_pos, z_pos, time)
	
	def show(self):
		print self.new_source
		
	def light_source(self, type, x, y, z, time):
		#X: -204, Y: 43.4, Z: -392
		self.new_source = [type, x, y, z, time]
		self.dispatcher.dispatch(Message('source', self.new_source))
		
	def chemical_source(self, type, x, y, z, time):
		self.new_source = [type, x, y, z, time]
		self.dispatcher.dispatch(Message('source', self.new_source))
		
	def radioactive_source(self, type, x, y, z, time):
		self.new_source = [type, x, y, z, time]
		self.dispatcher.dispatch(Message('source', self.new_source))
		
	def humidity_source(self, type, x, y, z, time):
		self.new_source = [type, x, y, z, time]
		self.dispatcher.dispatch(Message('source', self.new_source))
		
	def sound_source(self, type, x, y, z, time):
		self.new_source = [type, x, y, z, time]
		self.dispatcher.dispatch(Message('source', self.new_source))