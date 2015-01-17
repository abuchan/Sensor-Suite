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
		self.ox1 = 0
		self.oy1 = 0
		self.ox2 = 0
		self.heading = 0.0
		self.roll = 0.0
		self.pitch = 0.0
		self.yaw = 0.0
		self.angle = 0
		self.ATLS = 0
		self.HBS = 0

		self.start()

	def run(self):
		while(True):
			pass

	def add_sinks(self, sinks):
		self.dispatcher.add_sinks(sinks)

	def put(self, data):
		self.position_queue.put(data)

	#used when defining obstacles with IR sensor
	def set_obstacle(self, ob_x1, ob_x2):
		self.ox1 = ob_x1
		self.ox2 = ob_x2

	#sets a user defined source
	def set_source(self, type, x_pos, y_pos, z_pos, time):
		self.type = type
		self.sx = x_pos
		self.sy = y_pos
		self.sz = z_pos
		self.t = time

	#sets position of source if tracking 2 bodies with optitrak
	def set_moving_source(self, x, y, z):
		self.sx = x * 1000.0
		self.sy = y * 1000.0
		self.sz = z * 1000.0

	#sets the position of the robot
	def set_postion(self, x, y, z, qx, qy, qz, qw):
		self.px = x * 1000.0
		self.py = y * 1000.0
		self.pz = z * 1000.0
		self.qx = qx  
		self.qy = qy 
		self.qz = qz
		self.qw = qw
		self.convert_quat_euler()

	#IR sensor used to avoid an obstacle
	def calc_ir_sensor_value(self):
		self.x_dis = (self.px + 50) - self.ox1
		self.z_dis = (self.pz + 50) - self.oz1
		if self.x_dis < 200  and self.x_dis > 0 and self.z_dis < 200 and self.z_dis > 100:
			self.dispatcher.dispatch(Message('calc_sens', [-70, self.sx-self.px, self.sz-self.pz]))
		elif self.x_dis < 200 and self.x_dis > 0 and self.z_dis < -100 and self.z_dis > -200:
			self.dispatcher.dispatch(Message('calc_sens', [70, self.sx-self.px, self.sz-self.pz]))
		elif self.x_dis < 200  and self.x_dis > 0 and self.z_dis <= 0 and self.z_dis > -100:
			self.dispatcher.dispatch(Message('calc_sens', [70, self.sx-self.px, self.sz-self.pz]))
		elif self.x_dis < 200 and self.x_dis > 0 and self.z_dis > 0 and self.z_dis < 100:
			self.dispatcher.dispatch(Message('calc_sens', [70, self.sx-self.px, self.sz-self.pz]))
		elif self.x_dis > -200 and self.x_dis <= 0 and self.z_dis < 200 and self.z_dis > 100:
			self.dispatcher.dispatch(Message('calc_sens', [70, self.sx-self.px, self.sz-self.pz]))
		elif self.x_dis > -200 and self.x_dis <= 0 and self.z_dis < -100 and self.z_dis > -200:
			self.dispatcher.dispatch(Message('calc_sens', [-70, self.sx-self.px, self.sz-self.pz]))
		elif self.x_dis > -200 and self.x_dis <= 0 and self.z_dis <=0 and self.z_dis > -100:
			self.dispatcher.dispatch(Message('calc_sens', [70, self.sx-self.px, self.sz-self.pz]))
		elif self.x_dis > -100 and self.x_dis < 0 and self.z_dis > 0 and self.z_dis < 100:
			self.dispatcher.dispatch(Message('calc_sens', [-70, self.sx-self.px, self.sz-self.pz]))
		else:
			#print 'calc_bearing_sensor_value'
			self.calc_bearing_sensor_value()

	#IR Sensor used to traverse a tunnel
	def calc_double_ir_sensor_value(self):
		sen_11 = (self.px - 25) - self.ox1
		sen_22 = (self.px + 25) - self.ox2
		sen_12 = (self.px - 25) - self.ox2
		sen_21 = (self.px + 25) - self.ox1
#		print [(self.px + 20), (self.px - 20), sen_11, sen_22, sen_12, sen_21]
#		if (self.px - 25) > self.ox1 and (self.px + 25) < self.ox2 and sen_11 >= 40 and sen_22 <= -40:
#			self.heading = 0
		if (self.px - 25) > self.ox1 and (self.px + 25) < self.ox2 and sen_11 > -30 and sen_11 < 40:
			self.heading = -30
		elif (self.px - 25) > self.ox1 and (self.px + 25) < self.ox2 and sen_22 < 30 and sen_22 > -40:
			self.heading = 30
		elif (self.px + 25) < self.ox1 and sen_21 <= 30 and sen_21 > -100:
			self.heading = 30
		elif (self.px - 25) > self.ox2 and sen_12 >= 30 and sen_12 < 100:
			self.heading = -30
		else:
			self.heading = 0
#			self.calc_bearing_sensor_value()

		if self.yaw < -90 or self.yaw > 90:
			self.dispatcher.dispatch(Message('calc_sens', [self.heading, self.sx-self.px, self.sz-self.pz]))
		else:
			self.dispatcher.dispatch(Message('calc_sens', [(self.heading * -1), self.sx-self.px, self.sz-self.pz]))

	#simple bearing to target sensor algorithm
	def calc_bearing_sensor_value(self):
		self.angle = (math.atan2(self.sx - self.px, self.sz - self.pz))*(180/math.pi)
		if self.angle < -90 and self.yaw > 90:
			self.heading = (self.angle-self.yaw) % 180
		elif self.angle > 90 and self.yaw < -45:
			self.heading = ((self.yaw - self.angle) % 180) * -1
		elif self.angle < 0 and self.angle > -90 and self.yaw > 135:
			self.heading = (self.angle - self.yaw) % 180
		elif self.angle > 0 and self.angle < 90 and self.yaw < -135:
			self.heading = ((self.angle - self.yaw) % 180) * -1
		else:
			self.heading = self.angle - self.yaw

#		print [self.heading, self.angle, self.yaw, self.sx - self.px, self.sz - self.pz]
		self.dispatcher.dispatch(Message('calc_sens',[self.heading, self.sx-self.px, self.sz-self.pz]))

	#sensor that emulates a light source
	def TeMuBeTraR(self):
		self.angle = (math.atan2(self.sx - self.px, self.sz - self.pz))*(180/math.pi)
		if self.sx == 0 and self.sz == 0:
			self.HBS = self.HBS + 1
			self.heading = 70
		elif self.angle - self.yaw <= 20 and self.angle - self.yaw >= 0:
			self.heading = self.angle - self.yaw
			self.ATLS = 1
			self.HBS = 0
		elif self.angle - self.yaw >= -20 and self.angle - self.yaw < 0:
			self.heading = self.angle - self.yaw
			self.ATLS = -1
			self.HBS = 0
		else:
			if self.ATLS == -1:
				self.heading = -70
				self.HBS = self.HBS + 1
			else:
				self.heading = 70
				self.HBS = self.HBS + 1

		if self.HBS > 30 and self.HBS <= 60:
			self.dispatcher.dispatch(Message('calc_sens', [(self.heading * 10), self.sx-self.px, self.sz-self.pz]))
		elif self.HBS > 60 and self.HBS <= 100:
			self.dispatcher.dispatch(Message('calc_sens', [(self.heading * 15), self.sx-self.px, self.sz-self.pz]))	
		elif self.HBS > 100 and self.HBS <= 150:
			self.dispatcher.dispatch(Message('calc_sens', [(self.heading * 20), self.sx-self.px, self.sz-self.pz]))
		elif self.HBS > 150:
			self.dispatcher.dispatch(Message('calc_sens', [5, 50, 50]))
		else:
			self.dispatcher.dispatch(Message('calc_sens',[self.heading, self.sx-self.px, self.sz-self.pz]))

	#converts quaternion output of optitrak to euler angles
	def convert_quat_euler(self):
		#qw:q0, qx:q1, qy:q2, qz:q3
		self.roll = (math.atan2(2.0*(self.qw * self.qx + self.qy * self.qz),
															(1.0-(2.0*(self.qx**2 + self.qz**2))))) * (180/math.pi)
		self.pitch = (math.asin(2.0*(self.qw * self.qz - self.qy * self.qx))) *(180/math.pi)
		self.yaw = (math.atan2(2.0*(self.qw * self.qy + self.qx * self.qz),
															(1.0-(2.0*(self.qy**2 + self.qz**2))))) * (180/math.pi)
		self.TeMuBeTraR()