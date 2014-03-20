# This library performs actions to generate and parse hardware information
# from hardware.cfg file

import shutil
import ConfigParser
import argparse
from Crypto.Cipher import AES

def _addComputer(config, section):
	config.set(section, "ip")
	config.set(section, "rsaKey")
	config.set(section, "username")
	config.set(section, "password")
	return config

def _addDevice(config, section):
	config.set(section, "ip")
	return config

def initHardwareCFG():

	# build new config file (use config.read() to read existing)
	config = ConfigParser.ConfigParser()

	# Computers
	list = ["Play1", "CG", "Teleprompt", "PVP"]
	for computer in list:
		config.add_section(computer)
		config = _addComputer(config, computer)

	# Projectors
	list = ["rightProjector", "centerProjector", "leftProjector"]
	for device in list:
		config.add_section(device)
		config = _addDevice(config, device)

	# overwrite new hardware.cfg file
	with open("./hardware.cfg", "wb") as hwcfg:
		config.write(hwcfg)

def encryptPasswords():

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
						aes = AES.new("this is the pcp password")
						ciphertext = aes.encrypt(item[1] + ((32 - len(item[1])) * " "))
						config.set(section, "password", ciphertext)

	# overwrite new hardware.cfg file
	with open("./hardware.cfg", "wb") as hwcfg:
		config.write(hwcfg)

def decryptPassword(config, section):

	encrypted = False
	config.read("hardware.cfg")
	aes = AES.new("this is the pcp password")
	for char in config.get(section, "password"):
		if (char.isalpha() == False and char.isnum() == False):
			encrypted = True

	if encrypted:
		return aes.decrypt(config.get(section, "password")).strip()
	else:
		return config.get(section, "password")

def main():
	
	# command line argument parser
	parser = argparse.ArgumentParser(description = "Manages hardware network data")
	parser.add_argument("-i", "--init", action = "store_true", help = "Initializes .cfg file")
	parser.add_argument("-e", "--encrypt", action = "store_true", help = "Encrypts passwords")
	args = parser.parse_args()
	
	if args.init: initHardwareCFG()
	if args.encrypt: encryptPasswords()

if __name__ == "__main__":
	main()
