#!/bin/sh
#
# Projector Interface

from selenium import webdriver
import time
from multiprocessing import Process

def togglePower(ip, *args):

	browser = webdriver.Chrome()
	
	# left projector
	url = "http://" + ip + "/control.html"
	browser.get(url)
	assert "HDX" in browser.title
	lamp = browser.find_element_by_id("lamp")
	lamp.click()
	time.sleep(1)
	
	browser.quit()

def main():

	# define function pointers
	left = Process(target = togglePower, args = ("10.5.30.201",))
	center = Process(target = togglePower, args = ("10.5.30.202",))
	right = Process(target = togglePower, args = ("10.5.30.203",))
	
	# start processes
	left.start()
	center.start()
	right.start()
	
	# join processes
	left.join()
	center.join()
	right.join()
	
if __name__ == "__main__":
	main()
	