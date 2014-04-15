#!/usr/bin/python
#
# Main Start Menu

import projectors, computers, kipro
import pcpUtils as utils

def _printStartMenu(interfaces):

	print "\n",
	print "********************************\n" * 2
	print "Welcome to the COL Production Control Panel!\n"
	print "********************************\n" * 2
	
	# list out devices
	choices = {}
	for i, interface in enumerate(interfaces):
		id = i + 1
		choices[id] = interface
		print str(id) + ".\t" + choices[id]
	print str(i + 2) + ".\tExit\n"
	while True:
		try:
			choice = int(raw_input("Choose an interface: "))
		except ValueError:
			continue
		if choice < 0 or choice > (len(interfaces) + 1): continue
		if choice == (len(interfaces) + 1): exit()
		break

	# list out functions available to that device (use filter to only show options _ON)
	options = utils.loadOptions(choices[choice]).keys()
	if options == []:
		print "No options available!"
		exit()
	enabled = {}
	for j, option in enumerate(options):
		id = j + 1
		enabled[id] = option
		print str(id) + ".\t" + enabled[id]
	print str(j + 2) + ".\tExit\n"
	while True:
		try:
			choice = int(raw_input("Choose an function: "))
		except ValueError:
			continue
		if choice < 0 or choice > (len(interfaces) + 1): continue
		if choice == (len(enabled) + 1): exit()
		break

def _main():

	interfaces = utils.getAllDeviceNames()
	
	# Welcome to COL PCP
	_printStartMenu(interfaces)

if __name__ == "__main__":
	_main()