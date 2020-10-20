#!/usr/bin/env python

import rospy
import sys, os, time
import string
from diagnostic_msgs.msg import DiagnosticArray, DiagnosticStatus, KeyValue

global cpu_file
global mem_file

def callback(data):
	for dev in data.status:
		if dev.name == 'CPU Usage (ubuntu)':
			cpu_file.write(str(data.header.stamp.secs))
			for v in dev.values:
				if v.key in ['Core 0 User', 'Core 1 User', 'Core 2 User', 'Core 3 User', 'Core 4 User', 
				'Core 5 User', 'Core 6 User', 'Core 7 User']: 
					cpu_file.write(';'+v.value)
			cpu_file.write('\n')
		elif dev.name == 'Memory Usage (ubuntu)':
			mem_file.write(str(data.header.stamp.secs))
			for v in dev.values:
				if v.key in ['Total Memory (Physical)', 'Used Memory (Physical)', 'Free Memory (Physical)']: 
					mem_file.write(';'+v.value)
			mem_file.write('\n')

if __name__ == '__main__':
	rospy.init_node('listener', anonymous=True)

	timestr = time.strftime("%Y-%m-%d-%H-%M-%S")
	path_mem = rospy.get_param("~path")+'/'+"mem-monitor-"+timestr
	path_cpu = rospy.get_param("~path")+'/'+"cpu-monitor-"+timestr
	mem_file = open(path_mem,"w+")
	cpu_file = open(path_cpu,"w+")

	rospy.Subscriber("/diagnostics", DiagnosticArray, callback)

	rospy.spin()

	mem_file.close()
	cpu_file.close()