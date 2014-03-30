#!/usr/bin/python
#
# This library performs actions to generate and parse hardware information
# from hardware.cfg file

import shutil
import ConfigParser
import argparse
from Crypto.Cipher import AES

_USING_RSA_KEYS = False

_COMPUTER_LIST = [
	"play1",
	"cg",
	"teleprompt",
	"pvp",
]

_PROJECTOR_LIST = [
	"rightProjector",
	"centerProjector",
	"leftProjector",
]

_DEVICE_LIST = [
	"archive",
]

_DDR_LIST = [
	"kipro",
]

def getComputerList():
	"""Returns list of computers."""
	return _COMPUTER_LIST

def getProjectorList():
	"""Returns list of projectors."""
	return _PROJECTOR_LIST

def getDDRList():
	"""Returns list of DDR devices."""
	return _DDR_LIST

def getAllDeviceNames():
	"""Returns list of every device within PCP."""
	return getComputerList() + getProjectorList() + getDDRList()

def _addComputer(config, section):
	config.set(section, "ip")
	if _USING_RSA_KEYS: config.set(section, "rsaKey")
	config.set(section, "username")
	config.set(section, "password")
	config.set(section, "_shutdown", "OFF")
	config.set(section, "_talk", "OFF")
	return config

def _addDDR(config, section):
	config.set(section, "ip")
	config.set(section, "_record", "OFF")
	config.set(section, "_stop", "OFF")
	config.set(section, "_unmount", "OFF")
	return config

def _addDevice(config, section):
	config.set(section, "ip")
	config.set(section, "_power", "OFF")
	return config

def _initHardwareCFG():

	# build new config file (use config.read() to read existing)
	config = ConfigParser.ConfigParser()
	
	# Computers
	list = getComputerList()
	for computer in list:
		config.add_section(computer)
		config = _addComputer(config, computer)
		
	list = getDDRList()
	for DDR in list:
		config.add_section(computer)
		config = _addComputer(config, computer)

	# Devices with only IP addresses and power control
	list = getProjectorList()
	for device in list:
		config.add_section(device)
		config = _addDevice(config, device)

	# overwrite new hardware.cfg file
	with open("./hardware.cfg", "wb") as hwcfg:
		config.write(hwcfg)

def _encryptPasswords():

	config = ConfigParser.ConfigParser()
	config.read("hardware.cfg")

	# make sure they are not already encrypted
	passwords = []
	sections = config.sections()
	for section in sections:
		items = config.items(section)
		for item in items:
			if item[0] == "password":
				for char in item[1]:
					if char.isalpha() == False:
						# TODO: make this a realtime password
						aes = AES.new("this is the pcp password")
						ciphertext = aes.encrypt(item[1] + ((32 - len(item[1])) * " "))
						config.set(section, "password", ciphertext)

	# overwrite new hardware.cfg file
	with open("./hardware.cfg", "wb") as hwcfg:
		config.write(hwcfg)

def decryptPassword(config, section):
	"""Decrypts passwords from hardware.cfg."""

	encrypted = False
	config.read("hardware.cfg")
	aes = AES.new("this is the pcp password")
	for char in config.get(section, "password"):
		if (char.isalnum() == False):
			encrypted = True

	if encrypted:
		return aes.decrypt(config.get(section, "password")).strip()
	else:
		return config.get(section, "password")

def _main():
	
	# command line argument parser
	parser = argparse.ArgumentParser(description = "Manages hardware network data")
	parser.add_argument("-i", "--init", action = "store_true", help = "Initializes .cfg file")
	parser.add_argument("-e", "--encrypt", action = "store_true", help = "Encrypts passwords")
	args = parser.parse_args()
	
	if args.init: _initHardwareCFG()
	if args.encrypt: _encryptPasswords()

if __name__ == "__main__":
	_main()
