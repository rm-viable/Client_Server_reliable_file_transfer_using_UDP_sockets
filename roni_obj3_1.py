#!/usr/bin/env python

import subprocess
import sys
import os
import re
import time

if __name__ == "__main__":
	

	proc1 = os.popen('sudo -S ovs-vsctl set-controller br0 tcp:10.20.30.2:6633')

	proc2=subprocess.Popen(["sudo -S ovs-vsctl show"],shell=True,stdout=subprocess.PIPE)
	temp=proc2.communicate()[0]
	decoded=temp.decode("ascii")
	
	reg1=r'(?m)(?<=\bis_connected: ).*$'
	q1=re.findall(reg1,decoded)
	
	reg2=r'(?m)(?<=\bfail_mode: ).*$'
	q2=re.findall(reg2,decoded)
	
	if q1=="true":
		print("The OpenFlow connection between OVS and controller is established.")
	else:
		print("The OpenFlow connection between OVS and controller is not established.")
	
	print("The OVS is currently in {} mode.".format(q2[0]))
