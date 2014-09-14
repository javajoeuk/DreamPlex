# -*- coding: utf-8 -*-
"""
DreamPlex Plugin by DonDavici, 2012
 
https://github.com/DonDavici/DreamPlex

Based on XBMCLocalProxy 0.1 Copyright 2011 Torben Gerkensmeyer
Based on PleXBMC Remote Helper 0.2 Copyright 2013 Hippojay

DreamPlex Plugin is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 2 of the License, or
(at your option) any later version.

DreamPlex Plugin is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
"""
#===============================================================================
# IMPORT
#===============================================================================
from threading import currentThread
from enigma import ePythonMessagePump

from BaseHTTPServer import HTTPServer
from threading import Thread

from DPH_PlexGdm import PlexGdm
from DPH_RemoteHandler import RemoteHandler
from DP_Syncer import ThreadQueue

from __init__ import getVersion
from __common__ import printl2 as printl, getBoxInformation

#===============================================================================
#
#===============================================================================
class HttpDeamon(Thread):

	session = None

	#===========================================================================
	#
	#===========================================================================
	def __init__(self):
		self.playerData = ThreadQueue()
		self.playerDataPump = ePythonMessagePump()

	#===========================================================================
	#
	#===========================================================================
	def getPlayerDataPump(self):
		printl("", self, "S")

		printl("", self, "C")
		return self.playerDataPump

	#===========================================================================
	#
	#===========================================================================
	def getPlayerDataQueue(self):
		printl("", self, "S")

		printl("", self, "C")
		return self.playerData

	#===========================================================================
	#PROPERTIES
	#===========================================================================
	PlayerDataPump = property(getPlayerDataPump)
	PlayerData = property(getPlayerDataQueue)

	#===========================================================================
	#
	#===========================================================================
	def startDeamon(self):
		printl("", self, "S")

		Thread.__init__(self)

		self.HandlerClass = RemoteHandler
		self.ServerClass = HTTPServer
		self.protocol = "HTTP/1.0"

		self.start()

		# this starts updatemechanism to show up as player in devices like ios
		client = PlexGdm(debug=False)
		version = str(getVersion())
		gBoxType = getBoxInformation()
		clientBox = "8000"
		printl("clientBox: " + str(gBoxType), self, "D")
		client.clientDetails(clientBox, "192.168.45.80", "8000", "DreamPlex", version)
		client.start_registration()

		if client.check_client_registration():
			printl("Successfully registered", self, "D")
		else:
			printl("Unsuccessfully registered", self, "D")


		printl("", self, "C")

	#===========================================================================
	#
	#===========================================================================
	#def runHttp(session, playerCallback, HandlerClass = MyHandler,ServerClass = HTTPServer, protocol="HTTP/1.0"):
	def run(self):
		"""
		Test the HTTP request handler class.

		This runs an HTTP server on port 8000 (or the first command line
		argument).
		"""
		printl("", __name__, "S")

		port = 8000
		server_address = ('', port)

		self.HandlerClass.protocol_version = self.protocol
		self.HandlerClass.session = self.session
		self.HandlerClass.playerCallback = self.nowDoIt
		httpd = self.ServerClass(server_address, self.HandlerClass)

		sa = httpd.socket.getsockname()
		printl("Serving HTTP on" + str(sa[0]) + "port " + str(sa[1]) + "...", __name__, "D")
		httpd.serve_forever()

		printl("", __name__, "C")

	#===========================================================================
	#
	#===========================================================================
	def nowDoIt(self, data):
		print "nowDoIt =>"
		print currentThread()

		self.playerData.push((data,))
		self.playerDataPump.send(0)

