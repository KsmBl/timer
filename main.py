#!/usr/bin/python

from playsound import playsound
from time import sleep, time
import os
import sys

ALARM_FILE = "/path/to/your/mp3/alarm.mp3"
HELP_MESSAGE = "usage:\n  timer new <timer_name> <time>\n  timer new pizza 15:00 (to create a timer which needs 15 minutes)\n  timer new pizza 900 (to create a timer which needs 900 seconds / 15 minutes)\n\n  timer view <timer_name>\n  timer view pizza (to see how much time the pizza timer needs left)\n\n  timer pause <timer_name>\n  timer pause pizza (to pause the timer named pizza)\n\n  timer continue <timer_name>\n  timer continue pizza (to continue the timer named pizza)\n\n  timer stop <timer_name>\n  timer stop pizza (delete the timer named pizza)\n\n  timer list (to list all active timers)"

def main():
	if not os.path.exists("/tmp/timer/"):
		os.makedirs("/tmp/timer/")

	argv = sys.argv
	if len(argv) <= 1:
		print(HELP_MESSAGE)
		sys.exit(1)

	if argv[1] == "new":
		if len(argv) == 4:
			timerName = argv[2]

			if ':' in argv[3]:
				splitTimes = argv[3].split(':')

				if len(splitTimes) == 2:
					minutes = int(splitTimes[0])
					seconds = int(splitTimes[1])
					time = (minutes * 60) + seconds
				elif len(splitTimes) == 3:
					hours = int(splitTimes[0])
					minutes = int(splitTimes[1])
					seconds = int(splitTimes[2])
					time = (hours * 60 * 60) + (minutes * 60) + seconds

			else:
				time = int(argv[3])

			newTimer(timerName, time)

		else:
			print("usage:    timer new <timername> <timerlength>")
			print("example:  timer new pizza 15:00")
			print("example:  timer new pizza 900")

	elif argv[1] == "_new":
		timer(argv[2], argv[3])
	elif argv[1] == "view":
		viewTimer(argv[2])
	elif argv[1] == "pause":
		pauseTimer(argv[2])
	elif argv[1] == "continue":
		continueTimer(argv[2])
	elif argv[1] == "stop":
		stopTimer(argv[2])
	elif argv[1] == "list":
		listTimers("normal")
	else:
		print(HELP_MESSAGE)

def newTimer(name, length):
	usedTimers = listTimers("array")

	if name + ".tmr" in usedTimers:
		print("timer name already used")
		return

	pid = os.fork()

	if pid > 0:
		print(f"timer set to {length} seconds")
		sys.exit(0)

	sys.stdout.flush()
	sys.stderr.flush()

	si = open("/dev/null", "r")
	so = open("/dev/null", "a+")
	se = open("/dev/null", "a+")

	os.dup2(si.fileno(), sys.stdin.fileno())
	os.dup2(so.fileno(), sys.stdout.fileno())
	os.dup2(se.fileno(), sys.stderr.fileno())

	file_name = f"/tmp/timer/{name}.tmr"
	f = open(file_name, 'w+')
	f.write("start")
	f.close()

	timer(name, length)

def pauseTimer(name):
	usedTimers = listTimers("array")

	if not name + ".tmr" in usedTimers:
		print("timer name does not exist")
		return

	filePath = f"/tmp/timer/{name}.tmr"
	f = open(filePath, 'w+')
	f.write("pause")
	f.close()

	print("pause timer")

def continueTimer(name):
	usedTimers = listTimers("array")

	if not name + ".tmr" in usedTimers:
		print("timer name does not exist")
		return

	filePath = f"/tmp/timer/{name}.tmr"
	f = open(filePath, 'w+')
	f.write("continue")
	f.close()

	print("pause timer")

def stopTimer(name):
	usedTimers = listTimers("array")

	if not name + ".tmr" in usedTimers:
		print("timer name does not exist")
		return

	filePath = f"/tmp/timer/{name}.tmr"
	f = open(filePath, 'w+')
	f.write("stop")
	f.close()

	print("stop timer")

def _stopTimer(name, playSound):
	filePath = f"/tmp/timer/{name}.tmr"
	os.remove(filePath)

	if playSound:
		playsound(ALARM_FILE)
		print("dingdong Sound")

	sys.exit(0)

def viewTimer(name):
	usedTimers = listTimers("array")

	if not name + ".tmr" in usedTimers:
		print("timer name does not exist")
		return

	filePath = f"/tmp/timer/{name}.tmr"
	f = open(filePath, "r")
	_timeLeft = f.read()
	f.close()
	print(f"timer '{name}' needs {_timeLeft} seconds left")

def listTimers(_type):
	allTimers = [
		f for f in os.listdir(os.path.join("/tmp/timer/"))
		if os.path.isfile(os.path.join("/tmp/timer/", f))
	]

	if _type == "normal":
		for i in allTimers:
			print(os.path.splitext(i)[0])
			return

	elif _type == "array":
		return allTimers

def timer(name, length):
	currentTimestamp = int(time())
	timeLeft = length
	pause = False

	while True:
		filePath = f"/tmp/timer/{name}.tmr"
		f = open(filePath, "r")
		message = f.read()

		if message == "start":
			f.close()
			cleanTmrFile(filePath, timeLeft)
		elif message == "pause":
			f.close()
			cleanTmrFile(filePath, timeLeft)
			pause = True
		elif message == "continue":
			f.close()
			cleanTmrFile(filePath, timeLeft)
			pause = False
		elif message == "stop":
			f.close()
			cleanTmrFile(filePath, timeLeft)
			_stopTimer(name, False)

		if int(time()) > currentTimestamp:
			cleanTmrFile(filePath, timeLeft)
			if not pause:
				timeLeft -= int(time()) - currentTimestamp
			currentTimestamp = int(time())

		if timeLeft <= 0:
			_stopTimer(name, True)

		sleep(1)

def cleanTmrFile(filePath, timeLeft):
	f = open(filePath, "a")
	f.seek(0)
	f.truncate()
	f.write(str(timeLeft))
	f.close()

main()
