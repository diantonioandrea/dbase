# Interface for dbase built with CLIbrary

from colorama import Fore, Back, Style
import CLIbrary
import os, sys

try:
	cmdString = os.getlogin() + "@dbase"
except:
	cmdString = "unknown@dbase"

print("dbaseManager")
print("Wrapper for dbase written in Python and built with CLIbrary for database management")
print("Developed by Andrea Di Antonio")

while True:
	cmdHandler = {}
	cmdHandler["request"] = cmdString
	cmdHandler["style"] = Back.GREEN + Fore.MAGENTA
	cmdHandler["allowedCommands"] = []

	command = CLIbrary.cmdIn(cmdHandler)

	cmd = command["command"]
	sdOpts = command["sdOpts"]
	ddOpts = command["ddOpts"]

	if cmd == "exit":
		break