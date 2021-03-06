#!/usr/bin/python
#
# Projector Interface

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from multiprocessing import Process
import argparse

# computer class
class _Projector:
	
	def __init__(self, name):
		
		self.ip = utils.getProperty(name, "ip")
		self.options = utils.loadOptions(name)
		
	def getOption(self, option):
		"""Returns hardware capability options."""
		return self.options[option]

	def togglePower(self, *args):
	#####def togglePower(self, ip, *args):
	
		if self.options["_power"] != "ON":
			print "Option not enabled. Exiting."
			return 1

		options = Options()
		# TODO: figure out how to supress Chrome window
		#options.add_argument("--no-startup-window")
		#options.add_argument("--silent-launch")
		browser = webdriver.Chrome(chrome_options = options)
		
		# left projector
		url = "http://" + self.ip + "/control.html"
		browser.get(url)
		assert "HDX" in browser.title
		lamp = browser.find_element_by_id("lamp")
		lamp.click()
		browser.quit()

def _main():

	parser = argparse.ArgumentParser(description = "Manages projectors")
	parser.add_argument("-l", "--left", action = "store_true", help = "toggles left projector power")
	parser.add_argument("-c", "--center", action = "store_true", help = "toggles center projector power")
	parser.add_argument("-r", "--right", action = "store_true", help = "toggles right projector power")
	parser.add_argument("-a", "--all", action = "store_true", help = "toggles all projectors' power")
	args = parser.parse_args()

	# define function pointers for multiprocessing
	left = Process(target = _Projector("leftProjector").togglePower())
	right = Process(target = _Projector("rightProjector").togglePower())
	center = Process(target = _Projector("centerProjector").togglePower())
	#####right = Process(target = togglePower, args = ("10.5.30.203",))
	
	# start processes
	if args.left or args.all: left.start()
	if args.center or args.all: center.start()
	if args.right or args.all: right.start()
	
	# join processes
	if args.left or args.all: left.join()
	if args.center or args.all: center.join()
	if args.right or args.all: right.join()
	
if __name__ == "__main__":
	_main()
	