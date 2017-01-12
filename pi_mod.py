#!/usr/bin/python

import os, sys, subprocess #if subprocess not working do subprocess.call()

def is_root():
	if os.getuid() != 0:
		print "You Need Root Privileges"
		sys.exit()

def validate(pin): #validate if input is valid
	try:
		pin = int(pin)
	except:
		return False
	return True

class rasppi():
	def __init__(self):
		is_root()
		self.exported = []
		self.out = 0
		self.in_ = 0
		self.connected = []

	def __str__(self):
		stats = """ \nSTATS:		
  Exported pins: {}
  Out pin: {}
  In pin: {}
  Values of connected pins: {}
		""".format(self.exported, self.out, self.in_, self.connected)
		return stats

	def export(self, pin):
		directory =  " > /sys/class/gpio/export"
		if type(pin) == list:
			for i in pin:
				base = "echo " + str(i) + directory
				subprocess.call(base)
				self.exported.append(i)
		elif type(pin) == int:
			base = "echo {} > /sys/class/gpio/export".format(pin)
			subprocess.call(base)
			self.exported.append(pin)
		else:
			print "Unable to run command: Export pin ({})".format(pin)

	def unexport(self, pin):
		directory =  " > /sys/class/gpio/unexport"
		if type(pin) == list:
			for i in pin:
				if i not in self.exported:
					continue
				base = "echo " + str(i) + directory
				subprocess.call(base)
				self.exported.remove(i)
		elif type(pin) == int:
			if pin not in self.exported:
				return None
			base = "echo {} > /sys/class/gpio/unexport".format(pin)
			subprocess.call(base)
			self.exported.remove(pin)
		else:
			print "Unable to run command: Unexport pin ({})".format(pin)

	def setdir(self, out, in_): 
		if validate(out) and validate(in_):
			if in_ in self.exported and out in self.exported:
				subprocess.call("echo 'out' > /sys/class/gpio/gpio{}/direction".format(out))
				subprocess.call("echo 'in' > /sys/class/gpio/gpio{}/direction".format(in_))
			else:
				print "Selected pins ({},{}) were not exported correctly".format(out, in_)
		else:
			print "Check arguments provided: " + str(out) + ", " + str(in_)

	def setvalue(self, pin, value): #value can be ON / OFF ????
		dict = {"ON" : 1, "OFF" : 0}
		on_off = "echo '{}' > /sys/class/gpio/gpio{}/value".format(dict[value], pin)
		if validate(pin) and int(pin) in self.exported:
			subprocess.call(on_off)
		else:
			print "Check your input pin is correct"

	def check_value(self, pin):
		if validate(pin) and int(pin) in self.exported:
			print "Pin number {} status: ".format(str(pin)), subprocess.call("cat /sys/class/gpio/gpio{}/value".format(pin))
		else:
			print "Check your input pin is correct"

	def unexport_all(self):
		for n in self.exported:
			base = "echo {} > /sys/class/gpio/unexport".format(n)
			subprocess.call(base)
			self.exported.remove(n)

if "__main__" == __name__:
	rasp = rasppi()
	print rasp
	rasp.export([2,3])
	print rasp.exported
	rasp.setdir("2e",3)
	rasp.setvalue(2, "ON")
	rasp.setvalue(2, "OFF")
	rasp.setvalue(3, "OFF")
	print rasp
	rasp.check_value(2)
	rasp.check_value(3)
	rasp.unexport_all()
	print rasp

