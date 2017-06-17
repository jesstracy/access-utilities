#!/usr/bin/env python

import os
import sys
import re

ssh_config = '~/.ssh/config'

box_ip = raw_input("Enter the IP of the box: ")

# r = '^10.\d+.\d+$'
r = '10\.\d+\.\d+'

if re.search(r, str(box_ip)):
	print("Possibly a valid IP")
else:
	print("Not valid IP")
	sys.exit(0)




