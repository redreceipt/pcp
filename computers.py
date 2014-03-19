#!/bin/sh python
#
# requires the sshpass utility

import os
import time

def shutdown(ip):
	
	# shutdown computer
	os.system("sshpass -p Pr3s3ntation ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no presentation@" + ip)
	time.sleep(5)
	os.system("say hello")
	
def main():
	
	shutdown("10.5.30.7")
	
	# shut down teleprompt
	# shut down play 1

if __name__ == "__main__":
	main()