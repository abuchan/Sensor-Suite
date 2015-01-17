#from optitrak_stream import OptitrakStream
from asynch_dispatch import AsynchDispatch
#from s_sGUI import GUIStream
from basestation_stream import BasestationStream
from callback_stream import CallbackStream
from or_helpers_stream import HelpersStream
#from sources_stream import SourcesStream
#from sensor_stream import SensorStream
#from sources_search import SearchStream
#from obstacle_stream import ObstacleStream

import sys, glob
import time

#gets data from helperstream and sends it to the robot
def xb_send(val):
	b.put(['packet',val.data[0], val.data [1]])

#updates the sensor class with optitrak positioning data and source data if tracking 2 bodies
def optitrak_update(val):
	#comment out when defining a source and not tracking two bodies
	se.set_moving_source(val.data[7], val.data[8], val.data[9])
#	ob.set_z_position(val.data[2])
	#sends the position of the robot to the sensor class
	se.set_postion(val.data[0],val.data[1],val.data[2],val.data[3],val.data[4], val.data[5],
								val.data[6])

#updates the source class with source information
def add_source(val):
	so.put([str(val.data[0]), float(val.data[1]), float(val.data[2]), float(val.data[3]), str(val.data[4])])

#shows all current sources
def show_sources(val):
	so.show()
	
#sets the location of the source for the sensor class
def set_source(val):
	se.set_source(val.data[0],val.data[1],val.data[2],val.data[3],val.data[4])

#sets the robots address	
def set_addr(val):
	h.set_address(val.data)

#sends command to helperstream to resets the robot
def basestation_reset(val):
	h.resetRobot(val.data)

#sends command to helperstream to set the motor gains
def basestation_motor(val):
	h.setMotorGains(val.data)

#sends command to helperstream to set the motor speeds
def basestation_throt(val):
	h.setMotorSpeeds(val.data[0], val.data[1])
	
#sends the command to helperstream to set the steering gains
def set_steer_gains(val):
	h.setSteeringGains(val.data)

#tells the basestation to close the serial and xbee
def basestation_quit(val):
	input_data = ('quit','quit')
	b.put(input_data)

#sends the command to helperstream to stream telemetry //currently not being used
def stream_telemetry(val):
	numSamples = 100
	h.startTelemetryStream(val.data)

#sends data recieved from the xbee to be processed by the callbackstream
def robotData(val):
	cal.xbee_received(val.data[2])

#writes telemetry data to a file //currently not being used
def callback_stream(val):
	f = open('streaming_data.txt', 'a')
	f.write(val.data + '\n')
	f.close()

#gets the position of rigid bodies from the optitrak streaming data
def get_sensor_data(val):
	o.get_optitrak_position()

#sends the sensor data from the sensor class to the emulated robot class
def sensor_update(val):
	sch.search_move(val.data)

#starts the emulated robot thread
def seek_source(val):
	sch.set_seek_source()

#sends command to helperstream to set the steering rate of the robot
def set_steer_rate(val):
	h.setSteeringRate(val.data)
	
def set_obstacle(val):
	se.set_obstacle(val.data[0], val.data[1])
	
def e_stop(val):
	sch.stop()
	h.setMotorSpeeds(0, 0)

'''g = GUIStream(sinks = {'source_coord':[add_source], 'show_source':[show_sources],
							'reset':[basestation_reset], 'quit':[basestation_quit],'motor':[basestation_motor], 
							'throt_speed':[basestation_throt], 'seek_source':[seek_source], 
							'set_addr':[set_addr], 'steer_gains':[set_steer_gains], 'e-stop':[e_stop]}, 
							callbacks = None)
'''
#o = OptitrakStream(sinks = {'optitrak_data':[optitrak_update]}, autoStart = False)

b = BasestationStream(sinks = {'robot_data':[robotData]}, callbacks = None)

cal = CallbackStream(sinks = {'streaming_data':[callback_stream]}, callbacks = None)

h = HelpersStream(sinks = {'xb_send':[xb_send]}, callbacks = None, fileName = None)

#so = SourcesStream(sinks = {'source':[set_source]}, callbacks = None)

#se = SensorStream(sinks = {'calc_sens':[sensor_update]}, callbacks = None)

#sch = SearchStream(sinks = {'get_sensor':[get_sensor_data], 'steer_rate':[basestation_throt]},
#									callbacks = None)
									
#ob = ObstacleStream(sinks = {'tunnel':[set_obstacle]}, callbacks = None)

time.sleep(0.5)

print 'running'

while(True):
  try:
    time.sleep(0.1)
  except KeyboardInterrupt:
    sys.exit()