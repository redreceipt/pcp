#!/bin/sh python
#
# requires the sshpass utility

import os, time
import paramiko, base64

def openConnection(ip, hostkey, remoteUsername, remotePassword):
	key = paramiko.RSAKey(data = base64.decodestring(hostkey))
	client = paramiko.SSHClient()
	client = get_host_keys().add(ip, "ssh-rsa", key)
	client.connect(ip, username = remoteUsername, password = remotePassword)
	return client

def main():
	
	computers = {
		"play1": {"ip": "10.5.30.11", "key": "AAAAB3NzaC1yc2EAAAADAQABAAABAQDJ2KP+WJW5Uzakgk03dIW34AUoLOXaQbGed7aDj6NXeyVCgc7iK7BySeRc9RgU1rccSZm5Q8m7I5YA+xOpv5f00qVsrVZSlMMfIL955YUFd3yKTVdf15RUE4Dz1hyv1LHUZ4CnN19wAhQ+FZdzcWwYhLczwvZ2OMZbTi2PAiqyHlc55n+iKGX1ovQf7qEoA0M1qrMaDaaTYEq1O5yvKgi3s3uZGZK3Bnthy28P9CexXWRrbLGXkDBH52UFyABbbEqUZ3672CbTpByE+2V3I3B2WjgPinMH8Dl5zLdYy7jwxVaOgWTO/Q8IsvNyGOIbc6+ct2RNt9Uny+MwRAhju7Rl"},
		"pvp": "10.5.30.8",
		"cg": "10.5.30.7",
		"teleprompt": "10.5.30.9"
	}

	# connect to play 1 and shutdown
	computer = computers["play1"]
	client = openConnection(computer["ip"], computer["key"], "presentation", "Pr3s3ntation")
	###client.exec_command("say hello world")
	client.close()
	
	# shut down teleprompt
	# shut down cg

if __name__ == "__main__":
	main()
