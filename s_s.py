from optitrak_stream import OptitrakStream
from asynch_dispatch import AsynchDispatch
from s_sGUI import GUIStream
from basestation_stream import BasestationStream
from callback_stream import CallbackStream
from or_helpers_stream import HelpersStream
from sources_stream import SourcesStream
from sensor_stream import SensorStream
from sources_search import SearchStream

import sys, glob
import time

def xb_send(val):
	b.put(['packet',val.data[0], val.data [1]])

def optitrak_update(val):
	se.set_postion(val.data[0],val.data[1],val.data[2],val.data[3],val.data[4], val.data[5],
								val.data[6])

def add_source(val):
	so.put([str(val.data[0]), float(val.data[1]), float(val.data[2]), float(val.data[3]), str(val.data[4])])

def show_sources(val):
	so.show()
	
def set_source(val):
	se.set_source(val.data[0],val.data[1],val.data[2],val.data[3],val.data[4])
	
def set_addr(val):
	h.set_address(val.data)

def basestationReset(val):
	h.resetRobot(val.data)

def basestationMotor(val):
	h.setMotorGains(val.data)

def basestationThrot(val):
	h.setMotorSpeeds(val.data[0], val.data[1])
	
def set_steer_gains(val):
	h.setSteeringGains(val.data)

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

def get_sensor_data(val):
	o.get_optitrak_position()

def sensor_update(val):
	sch.search_move(val.data)

def seek_source(val):
	h.setMotorSpeeds(val.data[0], val.data[1])
	
def set_steer_rate(val):
	h.setSteeringRate(val.data)
	
def exit(val):
	sys.exit()

g = GUIStream(sinks = {'source_coord':[add_source], 'show_source':[show_sources],
							'reset':[basestationReset], 'quit':[basestationQuit],'motor':[basestationMotor], 
							'throt_speed':[basestationThrot], 'seek_source':[seek_source], 
							'set_addr':[set_addr], 'steer_gains':[set_steer_gains]}, callbacks = None)

o = OptitrakStream(sinks = {'optitrak_data':[optitrak_update]}, autoStart = False)

b = BasestationStream(sinks = {'robot_data':[robotData], 'safe_exit':[exit]}, callbacks = None)

cal = CallbackStream(sinks = {'streaming_data':[callback_stream]}, callbacks = None)

h = HelpersStream(sinks = {'xb_send':[xb_send]}, callbacks = None, fileName = None)

so = SourcesStream(sinks = {'source':[set_source]}, callbacks = None)

se = SensorStream(sinks = {'calc_sens':[sensor_update]}, callbacks = None)

sch = SearchStream(sinks = {'get_sensor':[get_sensor_data], 'steer_rate':[set_steer_rate],
									'found':[basestationMotor]}, callbacks = None)

time.sleep(0.5)

while(True):
  try:
    time.sleep(0.1)
  except KeyboardInterrupt:
    sys.exit()