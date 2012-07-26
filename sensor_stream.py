from asynch_dispatch import *
import threading, Queue
import sys
import math

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
		self.roll = 0.0
		self.pitch = 0.0
		self.yaw = 0.0
		self.angle_from_robot_to_source = 0

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
		self.px = x * 1000.0
		self.py = y * 1000.0
		self.pz = z * 1000.0
		self.qx = qx  
		self.qy = qy 
		self.qz = qz
		self.qw = qw
		self.convert_quat_euler()
		
	def calc_sensor_value(self):
		self.angle_from_robot_to_source = (math.atan2(self.px - self.sx, self.pz - self.sz))*(180/math.pi)
		self.dispatcher.dispatch(Message('calc_sens',[(self.angle_from_robot_to_source + self.pitch),
																								 self.px - self.sx, self.pz - self.sz]))

	def convert_quat_euler(self):
		#qw:q0, qx:q1, qy:q2, qz:q3
		self.roll = (math.atan2(2.0*(self.qw * self.qx + self.qy * self.qz),
															(1.0-(2.0*(self.qx**2 + self.qy**2))))) * (180/math.pi)
		self.pitch = (math.asin(2.0*(self.qw * self.qy - self.qz * self.qx))) *(180/math.pi)
		self.yaw = (math.atan2(2.0*(self.qw * self.qz + self.qx * self.qy),
															(1.0-(2.0*(self.qy**2 + self.qz**2))))) * (180/math.pi)
		self.calc_sensor_value()