#!/usr/bin/env python

import subprocess
import sys
import os
import re
import time

if __name__ == "__main__":
	
	#commands for the configuration or bridge, port and controller
	commands=[
	"echo sdn | sudo -S ovs-vsctl add-br P_bridge_MGMT_G",
	"echo sdn | sudo -S ovs-vsctl add-port P_bridge_MGMT_G eno1",
	"echo sdn | sudo -S ovs-vsctl set-controller P_bridge_G tcp:10.20.30.2:6633"
	]

	b = os.popen('sudo -S ovs-vsctl set-controller P_bridge_G tcp:10.20.30.2:6633')
	#subprocess to execute commands on linux server
	k=subprocess.Popen(commands,shell=True,stdout=subprocess.PIPE)
	
	time.sleep(30)
	
	#verifying the OpenFlow channel between switch and controller
	x=subprocess.Popen(["echo sdn | sudo -S ovs-vsctl show"],shell=True,stdout=subprocess.PIPE)
	y=x.communicate()[0]
	z=y.decode("ascii")
	
	reg1=r'(?m)(?<=\bis_connected: ).*$'
	find1=re.findall(reg1,z)
	
	reg2=r'(?m)(?<=\bfail_mode: ).*$'
	find2=re.findall(reg2,z)
	
	if find1=="true":
		print("The OpenFlow connection between OVS and controller is established.")
	else:
		print("The OpenFlow connection between OVS and controller is not established.")
	
	print("The OVS is currently in {} mode.".format(find2[0]))