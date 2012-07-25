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

		self.command_queue = Queue.Queue()

		self.start()
	
	def run(self):
		while True:
			pass

	def setFileName(self, fileName):
		self.fileName = fileName
		print self.fileName

	def put(self, data):
		self.command_queue.put(data)
  
	def add_sinks(self,sinks):
		self.dispatcher.add_sinks(sinks)

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

########## Helper functions #################
	def xb_send(self, DEST_ADDR, status, type, data):
		payload = chr(status) + chr(type) + ''.join(data)
		data = [DEST_ADDR, payload]
		self.dispatcher.dispatch(Message('xb_send', data))

	def resetRobot(self, DEST_ADDR):
		print "Resetting robot..."
		self.xb_send(DEST_ADDR, 0, command.SOFTWARE_RESET, pack('h',1))


	def sendEcho(self, msg):
		self.xb_send(DEST_ADDR, 0, command.ECHO, msg)

	def wakeRobot(self):
		self.awake = 0;
		while not(self.awake):
			print "Waking robot ... "
			self.xb_send(DEST_ADDR, 0, command.SLEEP, pack('b',0))
			time.sleep(0.2)

	def sleepRobot(self):
		print "Sleeping robot ... "
		self.xb_send(DEST_ADDR, 0, command.SLEEP, pack('b',1))


	def setMotorGains(self, DEST_ADDR, gains):
		count = 1
		self.motorGains = gains
#		while not(self.motor_gains_set):
		print "Setting motor gains...   ",count,"/8"
		self.xb_send(DEST_ADDR, \
						0, command.SET_PID_GAINS, pack('10h',*gains))
		time.sleep(0.3)
#			if count > 8:
#				print "Unable to set motor gains, exiting."
#				xb_safe_exit()

	def setMotorSpeeds(self, DEST_ADDR, spleft, spright):
		thrust = [spleft, 0, spright, 0, 0]
		self.xb_send(DEST_ADDR, \
						0, command.SET_THRUST_CLOSED_LOOP, pack('5h',*thrust))