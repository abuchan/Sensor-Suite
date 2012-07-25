from asynch_dispatch import *
import threading, Queue
import sys
import numpy as np

class SensorStream(threading.Thread):
	def __init__(self, sinks = None, callbacks = None, dispatcher=None, autoStart=True):
		threading.Thread.__init__(self)
		self.daemon = True

		self.dispatcher = AsynchDispatch(sinks = sinks, callbacks = callbacks)
		self.position_queue = Queue.Queue()
		self.type = ''
		self.sx = 0
		self.sy = 0
		self.sz = 0
		self.t = ''
		self.px = 0
		self.py = 0
		self.pz = 0
		self.qx = 0
		self.qy = 0
		self.qz = 0
		self.qw = 0
		self.new_x = 0
		self.new_y = 0
		self.new_z = 0
		self.quat_v = []
		self.orn_v = []

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
		self.convert_quat_euler()
		
	def calc_sensor_value(self):
		print 'calc'
		self.new_x = self.sx - self.px
		self.new_y = self.sy - self.py
		self.new_z = self.sz - self.pz
		self.dispatcher.dispatch(Message('calc_sens', [self.new_x, self.new_y, self.new_z, 
														self.orn_v[i,0], self.orn_v[i,1], self.[i,2]]))

	def convert_quat_euler(self):
		print 'convert'
		self.quat_v = np.array((self.qw, self.qx, self.qy, self.qz)).transpose()
		self.orn_v = np.zeros((self.quat_v.shape[0], 3))

		self.orn_v[i,0] = (math.atan2(2.0*(self.quat_v[i,2] * self.quat_v[i,3] + self.quat_v[i,0] * self.quat_v[i,1]), \
											self.quat_v[i,0]**2 - self.quat_v[i,1]**2 - self.quat_v[i,2]**2 + self.quat_v[i,3]**2) + \
											2*math.pi) % (2*math.pi) - math.pi
		self.orn_v[i,1] = math.asin(-2*(self.quat_v[i,1] * self.quat_v[i,3] - self.quat_v[i,0] * self.quat_v[i,2]))
		self.orn_v[i,2] = math.atan2(2*(self.quat_v[i,1] * self.quat_v[i,2] + self.quat_v[i,0] * self.quat_v[i,3]), \
																self.quat_v[i,0]**2 + self.quat_v[i,1]**2 - self.quat_v[i,2]**2 - self.quat_v[i,3]**2)
		self.calc_sensor_value()