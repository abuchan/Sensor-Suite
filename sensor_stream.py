from asynch_dispatch import *
import threading, Queue
import sys
import numpy as np

class SensorStream(threading.Thread):
	def __init__(self, sinks = None, callbacks = None, dispatcher=None, autoStart=True):
		threading.Thread.__init__(self)
		self.daemon = True

		self.dispatcher = AsynchDispatch(sinks = sinks, callbacks = callbacks)
		self.source = []
		self.position_queue = Queue.Queue()

		if autoStart:
			self.start()

	def run(self):
		while(True):
			pass

	def add_sinks(self, sinks):
		self.dispatcher.add_sinks(sinks)

	def put(self, data):
		self.position_queue.put(data)

	def set_source(self, type, x_pos, y_pos, z_pos, time):
		self.type = type
		self.sx = x_pos
		self.sy = y_pos
		self.sz = z_pos
		self.t = time

	def set_postion(self, x, y, z, qx, qy, qz, qw):
		self.px = x
		self.py = y
		self.pz = z
		self.qx = qx
		self.qy = qy
		self.qz = qz
		self.qw = qw

	def calc_sensor_value(self):
		quat_v = np.array((self.qw, self.qx, self.qy, self.qz)).transpose()
		orn_v = np.zeros((quat_v.shape[0], 3))

		orn_v[i,0] = (math.atan2(2.0*(quat_v[i,2] * quat_v[i,3] + quat_v[i,0] * quat_v[i,1]), \
								 quat_v[i,0]**2 - quat_v[i,1]**2 - quat_v[i,2]**2 + quat_v[i,3]**2) + \
								 2*math.pi) % (2*math.pi) - math.pi
		orn_v[i,1] = math.asin(-2*(quat_v[i,1] * quat_v[i,3] - quat_v[i,0] * quat_v[i,2]))
		orn_v[i,2] = math.atan2(2*(quat_v[i,1] * quat_v[i,2] + quat_v[i,0] * quat_v[i,3]), \
													 quat_v[i,0]**2 + quat_v[i,1]**2 - quat_v[i,2]**2 - quat_v[i,3]**2)
		return orn_v