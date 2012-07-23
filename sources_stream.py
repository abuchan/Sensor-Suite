from asynch_dispatch import *
import threading, Queue
import sys

class SourcesStream(threading.Thread):
	def __init__(self, sinks = None, callbacks = None, dispatcher=None, autoStart=True):
		threading.Thread.__init__(self)
		self.daemon = True

		self.dispatcher = AsynchDispatch(sinks = sinks, callbacks = callbacks)
		self.sources_list = []

		if autoStart:
			self.start()

	def run(self):
		while(True):
			pass

	def add_sinks(self, sinks):
		self.dispatcher.add_sinks(sinks)

	def put(self, message):
		print message

	def update(self, type, x_pos, y_pos, z_pos, time):
		self.new_source = [type, x_pos, y_pos, z_pos, time]
		self.sources_list.append(self.new_source)
		self.define_source(self.new_source)

	def show(self):
		self.list= 0
		for self.list in self.sources_list:
			print self.list
	
	#defines a source, can perform options to customize source
	def define_source(self, source):
		self.dispatcher.dispatch(Message('source', source))