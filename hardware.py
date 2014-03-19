# This library performs actions to generate and parse hardware information
# from hardware.cfg file

import shutil
import ConfigParser
import argparse

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

def main():
	print "TODO: Add command line args for this library"
	parser = argparse.ArgumentParser(description = "Manages hardware network data")
	parser.add_argument("-i", "--init", action = "store_true", help = "Initializes .cfg file")
	args = parser.parse_args()
	if args.init == True:
		initHardwareCFG()
		exit()

if __name__ == "__main__":
	main()
