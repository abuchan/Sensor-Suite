from optitrak_stream import OptitrakStream
from asynch_dispatch import AsynchDispatch
from s_sGUI import GUIStream
from basestation_stream import BasestationStream
from callback_stream import CallbackStream
from or_helpers_stream import HelpersStream
from console_stream import ConsoleStream
from keyboard_control_stream import keyboardStream
from sources_stream import SourcesStream
from sensor_stream import SensorStream
from sources_search import SearchStream

import sys, glob
import time

def xb_send(val):
	outgoing = ('packet',val.data[0], val.data [1])
	b.put(outgoing)

def OptitrakUpdate(val):
	se.set_position(val.data[0],val.data[1],val.data[2],val.data[3],val.data[4], val.data[5],
				val.data[6])

def add_source(val):
	so.update(str(val.data[0]), int(val.data[1]), int(val.data[2]), int(val.data[3]), int(val.data[4]))

def show_sources(val):
	so.show()
	
def set_source(val):
	se.set_source(val.data[0],val.data[1],val.data[2],val.data[3],val.data[4])

def setMotor_Gains(val):
	h.setMotorGainsSet()

def setSteer_Gains(val):
	h.setSteeringGainsSet()

def setSteer_Rate(val):
	h.setSteeringRateSet()

def setNumSamples(val):
	t.setNumSamples(val.data)

def setCount2Deg(val):
	h.setCount2Deg(val.data)

def setBytesIn(val):
	h.setBytesIn()

def setFlashErased(val):
	h.setFlashErase()

def basestationReset(val):
	h.resetRobot(val.data)

def basestationMotor(val):
	print val
	h.setMotorGains(val.data[0], val.data[1])

def basestationThrot(val):
	print val
	h.setMotorSpeeds(val.data[0], val.data[1], val.data[2])

def basestationSteer(val):
	h.put([val.type, val.data[0], val.data[1]])

def basestationTurning(val):
	h.put([val.type, val.data[0], val.data[1]])

def basestationQuit(val):
	input_data = ('quit','quit')
	b.put(input_data)

def stream_telemetry(val):
	numSamples = 100
	h.startTelemetryStream(val.data)

def robotData(val):
	cal.xbee_received(val.data[2])

def callback_stream(val):
	f = open('streaming_data.txt', 'a')
	f.write(val.data + '\n')
	f.close()

def eraseFlashMemory(val):
	h.put([val.type, val.data[0], val.data[1]])

def saveTelemetry(val):
	h.put([val.type, val.data[0], val.data[1]])

def readTelemetry(val):
	h.put([val.type, val.data[0], val.data[1]])

def console_input(val):
	input_val = ['keypress', val.data]
	k.put(input_val)

def get_sensor_data(val):
	sensor = se.calc_sensor_value()
	sch.put(sensor)

g = GUIStream(sinks = {'source_coord':[add_source], 'show_sources':[show_sources],
							'reset':[basestationReset], 'quit':[basestationQuit],'motor':[basestationMotor], 
							'throt_speed':[basestationThrot]}, callbacks = None)

#o = OptitrakStream(sinks = {'optitrak_data':[OptitrakUpdate]}, autoStart = False)

b = BasestationStream(sinks = {'robot_data':[robotData]}, callbacks = None)

cal = CallbackStream(sinks = {'streaming_data':[callback_stream], 'steering_rate_set':[setSteer_Rate], 
										'motor_gains_set':[setMotor_Gains],'steering_gains_set':[setSteer_Gains], 
										'bytes_in':[setBytesIn], 'flash_erased':[setFlashErased],'turning_rate':[setCount2Deg]}, callbacks = None)

h = HelpersStream(sinks = {'xb_send':[xb_send]}, callbacks = None, fileName = None)

so = SourcesStream(sinks = {'source':[set_source]}, callbacks = None)

se = SensorStream(sinks = None, callbacks = None)

sch = SearchStream(sinks = {'get_sensor':[get_sensor_data]}, callbacks = None)

time.sleep(0.5)

while(True):
  try:
    time.sleep(0.1)
  except KeyboardInterrupt:
    sys.exit()