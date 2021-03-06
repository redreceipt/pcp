#!/usr/bin/python
#
# Projector Interface

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import argparse
import pcpUtils as utils

# computer class
class _KiProDDR:
	
	def __init__(self, name):
		
		self.ip = utils.getProperty(name, "ip")
		self.options = utils.loadOptions(name)
		
	def getOption(self, option):
		"""Returns hardware capability options."""
		return self.options[option]

	def interface(self, id, showStatus):
	#####def togglePower(self, ip, *args):
	
		if id == "record" and self.options["_record"] != "ON":
			print "Option not enabled. Exiting."
			return 1
		elif  id == "stop" and self.options["_stop"] != "ON":
			print "Option not enabled. Exiting."
			return 1
		elif  id == "slot" and self.options["_unmount"] != "ON":
			print "Option not enabled. Exiting."
			return 1
		else:
			options = Options()
			# TODO: figure out how to supress Chrome window
			#options.add_argument("--no-startup-window")
			#options.add_argument("--silent-launch")
			browser = webdriver.Chrome(chrome_options = options)
			
			# open interface page
			url = "http://" + self.ip
			browser.get(url)
			time.sleep(1)
			transport = browser.find_element_by_id("transport_page_link")
			transport.click()
			browser.switch_to_frame(browser.find_element_by_id("transport_controls_frame"))
			
			# do kipro function
			if id:
				button = browser.find_element_by_id(id)
				button.click()
				button.click()
			
			if showStatus:
				disk = browser.find_element_by_id("eParamID_SelectedSlot").text
				space = browser.find_element_by_id("eParamID_CurrentMediaAvailable").text
				if space == "": space = "N/A"
				timecode = browser.find_element_by_id("eParamID_DisplayTimecode").text
				print "Selected Slot: " + disk
				print "Space Available: " + space
				if timecode == "00:00:00:00":
					print "Status: Stopped"
				else:
					print "Status: Recording..."
			
			browser.switch_to_default_content()
			browser.quit()

def _main():

	parser = argparse.ArgumentParser(description = "Manages KiPro DDR")
	functions = parser.add_mutually_exclusive_group()
	functions.add_argument("-r", "--record", action = "store_true", help = "starts recording")
	functions.add_argument("-s", "--stop", action = "store_true", help = "stops recording")
	functions.add_argument("-u", "--unmount", action = "store_true", help = "unmounts and changes slot")
	parser.add_argument("-d", "--diskStatus", action = "store_true", help = "shows current disk and space available")
	args = parser.parse_args()
	
	# initialize KiPro DDR
	kipro = _KiProDDR("kipro")
	id = None

	# interface with KiPro web page
	if args.record: id = "record"
	if args.stop: id = "stop"
	if args.unmount: id = "slot"
	
	kipro.interface(id, args.diskStatus)
	
if __name__ == "__main__":
	_main()
	