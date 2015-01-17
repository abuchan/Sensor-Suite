import glob
import time
import sys
from lib import command
from callback_stream import CallbackStream
import datetime
import serial
from struct import pack
from xbee import XBee
from math import ceil,floor
import numpy as np
from asynch_dispatch import *
import threading, Queue
## Constants
###
MOVE_SEG_CONSTANT = 0
MOVE_SEG_RAMP = 1
MOVE_SEG_SIN = 2
MOVE_SEG_TRI = 3
MOVE_SEG_SAW = 4
MOVE_SEG_IDLE = 5
MOVE_SEG_LOOP_DECL = 6
MOVE_SEG_LOOP_CLEAR = 7
MOVE_SEG_QFLUSH = 8

##
STEER_MODE_DECREASE = 0
STEER_MODE_INCREASE = 1
STEER_MODE_SPLIT = 2

class HelpersStream(threading.Thread):
	def __init__(self, sinks = None, callbacks = None, fileName = ''):
		threading.Thread.__init__(self)
		self.daemon = True

		self.dispatcher = AsynchDispatch(sinks=sinks, callbacks = callbacks)
		self.fileName = fileName

		self.imudata = []
		self.fileName = ''
		self.steering_rate_set = False
		self.motor_gains_set = False
		self.steering_rate_set = False
		self.flash_erased = False
		self.leadinTime = 0
		self.leadoutTime = 0
		self.angRateDeg = 0
		self.deg2count = 0
		self.count2deg = 0
		self.angRate = 0
		self.addr = '\x30\x02'
		
		self.command_queue = Queue.Queue()

		self.start()

	def setFileName(self, fileName):
		self.fileName = fileName
		print self.fileName

	def put(self, data):
		self.command_queue.put(data)
  
	def add_sinks(self,sinks):
		self.dispatcher.add_sinks(sinks)

	def setImuData(self, telem_index, data):
		self.imudata[telem_index] = data

	def set_address(self, addr):
		self.addr = addr

	def setMotorGainsSet(self):
		self.motor_gains_set = True

	def setSteeringGainsSet(self):
		self.steering_gains_set = True

	def setSteeringRateSet(self):
		self.steering_rate_set = True

	def setBytesIn(self):
		self.bytesIn = self.bytesIn + (2*4 + 15*2)

	def setCount2Deg(self, rate):
		self.Count2Deg = self.Count2Deg * rate
		print "degrees: ", self.Count2Deg
		print "counts: ", rate

	def setFlashErase(self):
		self.flash_erased = True

	def run(self):
		while True:
			pass


########## Helper functions #################
	def xb_send(self, DEST_ADDR, status, type, data):
		payload = chr(status) + chr(type) + ''.join(data)
		data = [DEST_ADDR, payload]
		self.dispatcher.dispatch(Message('xb_send', data))

	def xb_safe_exit(self):
		print "Halting xb"
		self.xb.halt()
		print "Closing serial"
		self.ser.close()
		print "Exiting..."

	def resetRobot(self, DEST_ADDR):
		print "Resetting robot..."
		self.xb_send(self.addr, 0, command.SOFTWARE_RESET, pack('h',1))

	def sendEcho(self, msg):
		self.xb_send(self.addr, 0, command.ECHO, msg)

	def wakeRobot(self):
		self.awake = 0;
		while not(self.awake):
			print "Waking robot ... "
			self.xb_send(self.addr, 0, command.SLEEP, pack('b',0))
			time.sleep(0.2)

	def sleepRobot(self):
		print "Sleeping robot ... "
		self.xb_send(self.addr, 0, command.SLEEP, pack('b',1))

	def setSteeringRate(self, rate):
		self.angRateDeg = rate
		self.deg2count = 14.375
		self.count2deg = 1/self.deg2count
		self.angRate = round( self.angRateDeg / self.count2deg)
		self.xb_send(self.addr, 0, command.SET_CTRLD_TURN_RATE, pack('=h',self.angRate))
		time.sleep(0.3)
		
	def setMotorGains(self, gains):
		self.motorGains = gains
		print "Setting motor gains...   "
		self.xb_send(self.addr, \
						0, command.SET_PID_GAINS, pack('10h',*gains))
		time.sleep(0.3)

	def setSteeringGains(self, gains):
		self.steeringGains = gains
		print "Setting steering gains...   "
		self.xb_send(self.addr, \
						0, command.SET_STEERING_GAINS, pack('6h',*gains))
		time.sleep(0.3)

	def setMotorSpeeds(self, spleft, spright):
		thrust = [spleft, 0, spright, 0, 0]
		self.xb_send(self.addr, \
						0, command.SET_THRUST_CLOSED_LOOP, pack('5h',*thrust))