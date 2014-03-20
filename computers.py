#!/bin/sh python

import os, time
import paramiko, base64
import ConfigParser
import argparse
import hardware

# computer class
class _Computer:
	
	def __init__(self, name):
		
		config = ConfigParser.ConfigParser()
		config.read("hardware.cfg")
		
		self.ip = config.get(name, "ip")
		self.key = config.get(name, "rsaKey")
		self.username = config.get(name, "username")
		self.password = hardware.decryptPassword(config, name)
		self.client = None

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
		
		# uses the say application
		message = "say " + message
		self.client.exec_command(message)

	def shutdown(self):
		
		# sudo shutdown and type in the password
		self.client.exec_command("sudo shutdown now")
		time.sleep(1)
		self.client.exec_command(self.password)

def _main():
	
	parser = argparse.ArgumentParser(description = "Manages production computers")
	parser.add_argument("-s", "--shutdown", action = "append", help = "Shuts down computer", default = "all")
	parser.add_argument("-t", "--talk", nargs = 2, help = "Speaks a message")
	args = parse_args()
	
	computerList = args.shutdown
	if args.shutdown == ["all"]:
		computerList = hardware.getComputerList()
	for name in computerList:
		computer = _Computer(name)
		computer.openConnection()
		computer.shutdown()
		computer.closeConnection()
	
	if args.talk:
		computer = _Computer(args.talk[0])
		computer.openConnection()
		computer.talk(args.talk[0], args.talk[1])
		computer.closeConnection()

if __name__ == "__main__":
	_main()
