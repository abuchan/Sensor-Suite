import wx
import wx.grid as gridlib
from wxPython.wx import *
from wxPython.lib.dialogs import *
import threading

import sys, time, traceback
from asynch_dispatch import *

from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg
from matplotlib.backends.backend_wx import NavigationToolbar2Wx
import numpy as np

from matplotlib.figure import Figure

class GUIStream(threading.Thread):
	def __init__(self, frameClass=None, title='Sources and Sensors', callbacks=None, sinks=None, autoStart=True):
		threading.Thread.__init__(self)
		self.daemon = True
    
		self.frameClass = wx.Frame

		self.title = title
		global dispatcher
		dispatcher = AsynchDispatch(sinks=sinks, callbacks = callbacks)
 
		self.start()

	def run(self):
		self.app = wx.App()
		self.frame = ThreadedFrame(self.title, self.frameClass)
		self.frame.Show(True)
		self.app.MainLoop()

	def put(self, data):
		dispatcher.put(message)
  
	def add_sinks(self,sinks):
		dispatcher.add_sinks(sinks)

	def setDataFileName(self, file):
		global dataFileName
		dataFileName = file

#The main page of the program
class PageOne(wx.Panel):
	def __init__(self,parent): 
		wx.Panel.__init__(self,parent)
		
		self.left_throt = 0
		self.right_throt = 0
		
		#defining all the sizers
		sizer = wx.GridBagSizer()
		tbs1 = wx.BoxSizer(wx.HORIZONTAL)		
		tbs3 = wx.BoxSizer(wx.VERTICAL)
		tbsGridSize = wx.GridBagSizer()
		mbs = wx.BoxSizer(wx.HORIZONTAL)
		bbs1 = wx.GridBagSizer()
		bbs2 = wx.BoxSizer(wx.HORIZONTAL)
	
		#label for robot selector
		self.roboSelectLabel = wx.StaticText(self,label = "Select Robot:")
		tbs1.Add(self.roboSelectLabel, 1, wx.EXPAND, 5)
	
		#selector for arbitrary number of robots
		self.roboSelect=wx.ListBox(self,style=wx.LB_SINGLE,size=(-1,-1), name = 'Robot Selector')
		self.roboSelect.Append("x3002")
		self.roboSelect.Append("2")
		self.roboSelect.Append("3")
		self.roboSelect.Append("4")
		self.roboSelect.Append("xffff")
		tbs1.Add(self.roboSelect,2, wx.GROW|wx.ALL,5)
		self.Bind(wx.EVT_LISTBOX, self.OnSelect, self.roboSelect)

		#emergency stop button
		self.eStop = wx.Button(self,-1,label="E STOP!")
		self.eStop.SetBackgroundColour("red")
		tbsGridSize.Add(self.eStop,(1,0))
		self.Bind(wx.EVT_BUTTON, self.emergencyStopButtonClick, self.eStop)

		#Forward Button
		self.sB = wx.Button(self, -1, label = "Forward")
		tbsGridSize.Add(self.sB, (1,1))
		self.Bind(wx.EVT_BUTTON, self.forwardButtonClick, self.sB)
		
		#Straight Button
		self.straightB = wx.Button(self, -1, label = "Straight")
		tbsGridSize.Add(self.straightB, (1,2))
		self.Bind(wx.EVT_BUTTON, self.straightButtonClick, self.straightB)

		#Left Button
		self.lB = wx.Button(self, -1, label = "Left")
		tbsGridSize.Add(self.lB, (2,0))
		self.Bind(wx.EVT_BUTTON, self.leftButtonClick, self.lB)
		
		#Right Button
		self.rB = wx.Button(self, -1, label="Right")
		tbsGridSize.Add(self.rB, (2,2))
		self.Bind(wx.EVT_BUTTON, self.rightButtonClick, self.rB)

		#Slow Button
		self.slowB = wx.Button(self, -1, label="Slow")
		tbsGridSize.Add(self.slowB, (2,1))
		self.Bind(wx.EVT_BUTTON, self.slowButtonClick, self.slowB)

		#text area for output data
		self.outputData = wx.TextCtrl(self, size=(300,100),style = wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)
		self.outputData.WriteText("This Displays ouput data...\n")
		tbs3.Add(self.outputData,1,wx.GROW|wx.ALL,5)
		tbs1.Add(tbs3,6,wx.EXPAND,5)

		#Redirecting sys.out to text field
		redir=RedirectText(self.outputData)
		sys.stdout=redir

		#input boxes
		self.source_type_label = wx.StaticText(self, -1, label = 'SOURCE TYPE')
		bbs1.Add(self.source_type_label, (0,1))
		self.source_type = wx.Choice(self, choices = ['Light', 'Chemical', 'Radioactive', 'Humidity', 'Sound'])
		self.source_type.Select(0)
		bbs1.Add(self.source_type, (1,1))
		self.source_label = wx.StaticText(self, -1, label = 'DEFINE \n' + 'SOURCE')
		bbs1.Add(self.source_label, (1,0))
		self.x_label = wx.StaticText(self, -1, label = 'X POSITION')
		bbs1.Add(self.x_label, (0,2))
		self.x_pos = wx.TextCtrl(self,-1, name = 'x position')
		bbs1.Add(self.x_pos, (1,2))
		self.y_label = wx.StaticText(self, -1, label = 'Y POSITION')
		bbs1.Add(self.y_label, (0,3))
		self.y_pos = wx.TextCtrl(self, -1, name = 'y position')
		bbs1.Add(self.y_pos, (1,3))
		self.z_label = wx.StaticText(self, -1, label = 'Z POSITION')
		bbs1.Add(self.z_label, (0,4))
		self.z_pos = wx.TextCtrl(self, -1, name = 'z position')
		bbs1.Add(self.z_pos, (1,4))
		self.time_label = wx.StaticText(self, -1, label = 'TIME VARIANCE')
		bbs1.Add(self.time_label, (0,5))
		self.source_time = wx.Choice(self, choices = ['linear', 'log', 'sine', 'cosine'])
		self.source_time.Select(0)
		bbs1.Add(self.source_time, (1,5))

		#Add sources Button
		self.add_sources = wx.Button(self,-1,label="Add Source")
		self.Bind(wx.EVT_BUTTON,self.add_source_click,self.add_sources)
		bbs2.Add(self.add_sources,1,wx.ALL,5)

		#show sources Button
		self.show_sources = wx.Button(self, -1, label = 'Show Sources')
		self.Bind(wx.EVT_BUTTON, self.show_sources_click, self.show_sources)
		bbs2.Add(self.show_sources,2,wx.ALL,1)

		self.seek_source = wx.Button(self, -1, label = 'Seek Source')
		self.Bind(wx.EVT_BUTTON, self.seek_sources_click, self.seek_source)
		bbs2.Add(self.seek_source,3,wx.ALL,1)
		
		tbs1.Add(tbsGridSize,3,wx.EXPAND,5)

		#adding all the sizers to the panel; layout of the panel
		sizer.Add(tbs1,(0,0))
		sizer.Add(mbs,(2,0))
		sizer.Add(bbs1,(3,0))
		sizer.Add(bbs2,(4,0))

		#Formats sizers to resize when resizing the window
		sizer.AddGrowableCol(0)
		self.SetSizerAndFit(sizer)
		self.SetSizeHints(-1,self.GetSize().y,-1,self.GetSize().y);
		self.Show(True)

	#defining what the buttons actually do, can possibly put as a sink to another stream
	def forwardButtonClick(self,e):
		self.right_throt = self.right_throt + 20
		self.left_throt = self.left_throt + 20
		dispatcher.dispatch(Message('throt_speed', [self.addr, self.left_throt, self.right_throt]))

	def straightButtonClick(self,e):
		self.right_throt = 50
		self.left_throt = 50
		dispatcher.dispatch(Message('throt_speed', [self.addr, self.left_throt, self.right_throt]))

	def slowButtonClick(self,e):
		self.right_throt = self.right_throt - 20
		self.left_throt = self.left_throt - 20
		dispatcher.dispatch(Message('throt_speed', [self.addr, self.left_throt, self.right_throt]))

	def emergencyStopButtonClick(self,event):
		self.right_throt = 0
		self.left_throt = 0
		dispatcher.dispatch(Message('throt_speed', [self.addr, self.left_throt, self.right_throt]))

	def rightButtonClick(self,e):
		self.left_throt = self.right_throt + 20
		dispatcher.dispatch(Message('throt_speed', [self.addr, self.left_throt, self.right_throt]))

	def leftButtonClick(self,e):
		self.right_throt = self.left_throt + 20
		dispatcher.dispatch(Message('throt_speed', [self.addr, self.left_throt, self.right_throt]))

	#Determines which destination address to send commands to
	def OnSelect(self, event):
		select=event.GetSelection()
		if select == 0:
			self.addr = '\x30\x02'
			dispatcher.dispatch(Message('set_addr', self.addr))
			print "You chose number: " + str(repr(self.addr)) + " robot"

	def add_source_click(self, e):
		self.type = self.source_type.GetStringSelection()
		self.x = self.x_pos.GetValue()
		self.y = self.y_pos.GetValue()
		self.z = self.z_pos.GetValue()
		self.time = self.source_time.GetStringSelection()

		dispatcher.dispatch(Message('source_coord',[self.type, self.x, self.y, self.z, self.time]))

	def show_sources_click(self, e):
		dispatcher.dispatch(Message('show_source', 'show'))
	
	def seek_sources_click(self, e):
		dispatcher.dispatch(Message('seek_source', [50, 50]))

	def on_text(self, text):
		self.outputData.AppendText(text)

#This class redirects the text from sysout/systerr to the text field
class RedirectText(object):
	def __init__(self,aWxTextCtrl):
		self.out=aWxTextCtrl

	def write(self, string):
		wx.CallAfter(self.out.WriteText, string.decode('latin-1'))

class ThreadedFrame(wx.Frame):
	def __init__(self, title, frameClass):
		wx.Frame.__init__(self, None, title=title, size = (950,500))

		# create a panel and a notebook on the panel
		p = wx.Panel(self)
		nb = wx.Notebook(p)

		self.addr = '\x30\x02'

		# create the page windows as children of the notebook
		page1 = PageOne(nb)

		# add the pages to the notebook with the label to show on the tab
		nb.AddPage(page1, "Main")

		#packing the notebook into a sizer.
		sizer = wx.BoxSizer()
		sizer.Add(nb, 1, wx.EXPAND)
		p.SetSizer(sizer)
	
		self.status_bar = self.CreateStatusBar() # A StatusBar in the bottom of the window
		self.gauge = wx.Gauge(self.status_bar, -1, 100)#puts a progress bar in status bar

		# Setting up the menus.
		fileMenu= wx.Menu()
		modeMenu = wx.Menu()
		robotMenu = wx.Menu()

		# Standard wx menu widgets
		menuAbout = fileMenu.Append(wx.ID_ABOUT, "&About"," Information about this program")
		menuExit = fileMenu.Append(wx.ID_EXIT,"E&xit"," Exit the program")

		#Robot menu widgets
		menu_Octo = robotMenu.Append(1, "&OctoRoach", "load presets for OctoROACH")
		menu_Orni = robotMenu.Append(2, "&Ornithopter", "load presets for Ornithopter")
		menu_CLASH = robotMenu.Append(3, "&CLASH", "load presets for CLASH")
		menu_DASH = robotMenu.Append(4, "&DASH", "load presets for DASH")

		# Creates the menubar.
		menuBar = wx.MenuBar()
		menuBar.Append(fileMenu,"&File")
		menuBar.Append(robotMenu, "&Robots")
		self.SetMenuBar(menuBar)

		self.Bind(wx.EVT_MENU, self.onOcto, menu_Octo)
		self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
		self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
	
		# Bind close event here
		self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)	
		self.Show(True)

	def onOcto(self, e):
		dispatcher.dispatch(Message('file', None))

		dispatcher.dispatch(Message('reset', self.addr))
		time.sleep(0.15)

		dispatcher.dispatch(Message('motor',[5000,100,0,0,0,5000,100,0,0,0]))
		
		dispatcher.dispatch(Message('steer_gains', [50,10,0,0,0,0]))

	def OnAbout(self,e):
		# Standard dialogue box with an "ok" button
		dlg = wx.MessageDialog( self, "A GUI to operate robots", "About SkyNet", wx.OK)
		dlg.ShowModal() # Show it
		dlg.Destroy() # finally destroy it when finished.
	
	def OnExit(self,e):
		self.Destroy() # Close the frame.
		sys.exit()

	def OnCloseWindow(self,e):
		dispatcher.dispatch(Message('quit','quit'))
		sys.exit()