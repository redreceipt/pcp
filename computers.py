#!/usr/bin/python
#
# manages computer functions

import os, time
import paramiko, base64
import argparse
import pcpUtils as utils

class _Computer:
	
	def __init__(self, name):
		
		self.ip = utils.getProperty(name, "ip")
		self.key = utils.getProperty(name, "rsaKey")
		self.username = utils.getProperty(name, "username")
		self.password = utils.decryptPassword(name)
		self.client = None
		self.options = utils.loadOptions(name)
		
	def getOption(self, option):
		"""Returns hardware capability options."""
		return self.options[option]

	def openConnection(self):
		
		self.client = paramiko.SSHClient()
		self.client.set_missing_host_key_policy(paramiko.client.AutoAddPolicy())
		
		# use for hostkey authentication
		#key = paramiko.RSAKey(data = base64.decodestring(self.key))
		#self.client.get_host_keys().add(self.ip, "ssh-rsa", key)
		#self.client.set_missing_host_key_policy(paramiko.client.RejectPolicy())
		
		self.client.connect(self.ip, username = self.username, password = self.password)
	
	def closeConnection(self):
		self.client.close()
	
	def talk(self, message):
	
		if self.options["_talk"] != "ON":
			print "Option not enabled. Exiting."
			return 1
		
		# uses the say application
		message = "say " + message
		self.client.exec_command(message)

	def shutdown(self):
		
		if self.options["_shutdown"] != "ON":
			print "Option not enabled. Exiting."
			return 1
			
		chan = self.client.invoke_shell()
		
		# Ssh and wait for the password prompt.
		chan.send("sudo shutdown -h now\n")
		####chan.send("sudo shutdown -u now\n"), use this with UPS when looking at power on functions
		buff = ""
		while "Password:" not in buff:
			resp = chan.recv(9999)
			buff += resp

		chan.send(self.password + "\n")
		chan.close()

def _main():
	
	parser = argparse.ArgumentParser(description = "Manages production computers")
	functions = parser.add_mutually_exclusive_group()
	functions.add_argument("-s", "--shutdown", action = "append", help = "Shuts down computer", metavar = "COMPUTER", choices = utils.getComputerList())
	functions.add_argument("-t", "--talk", nargs = "+", help = "Speaks a message", metavar = ("COMPUTER", "MESSAGE"), choices = utils.getComputerList())
	args = parser.parse_args()
	
	if args.shutdown:
		computerList = args.shutdown
		if "all" in computerList: computerList = utils.getComputerList()
		for name in filter(lambda x: x in utils.getComputerList(), computerList):
			computer = _Computer(name)
			computer.openConnection()
			computer.shutdown()
			computer.closeConnection()
	
	if args.talk:
		computer = _Computer(args.talk[0])
		computer.openConnection()
		computer.talk(" ".join(talk[1:]))
		computer.closeConnection()

if __name__ == "__main__":
	_main()
