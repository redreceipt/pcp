#!/usr/bin/python
#
# Projector Interface

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import ConfigParser
import argparse

# computer class
class _KiProDDR:
	
	def __init__(self, name):
		
		config = ConfigParser.ConfigParser()
		config.read("hardware.cfg")
		self.ip = config.get(name, "ip")

	def interface(self, id, showStatus = False):
	#####def togglePower(self, ip, *args):

		options = Options()
		# TODO: figure out how to supress Chrome window
		#options.add_argument("--no-startup-window")
		#options.add_argument("--silent-launch")
		browser = webdriver.Chrome(chrome_options = options)
		
		# left projector
		url = "http://" + self.ip
		browser.get(url)
		###button = browser.find_element_by_id(id)
		####button.click()
		
		if showStatus:
			disk = browser.find_element_by_id("eParamID_SelectedSlot")
			space = browser.find_element_by_id("eParamID_CurrentMediaAvailable")
			print "Selected Slot: " + disk
			print "Space Available: " + space
			
		browser.quit()

	def showStatus(self):



def _main():

	parser = argparse.ArgumentParser(description = "Manages KiPro DDR")
	parser.add_argument("-r", "--record", action = "store_true", help = "starts recording")
	parser.add_argument("-s", "--stop", action = "store_true", help = "stops recording")
	parser.add_argument("-u", "--unmount", action = "store_true", help = "unmounts and changes slot")
	parser.add_argument("-d", "--diskStatus", action = "store_true", help = "shows current disk and space available")
	args = parser.parse_args()
	
	# initialize KiPro DDR
	kipro = _KiProDDR("kipro")
	id = "status_page_link"

	# interface with KiPro web page
	if args.record: id = "record"
	if args.stop: id = "stop"
	if args.unmount: id = "slot"
	
	kipro.interface(id, args.diskStatus)
	
if __name__ == "__main__":
	_main()
	