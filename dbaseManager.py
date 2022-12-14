# Interface for dbase built with CLIbrary

from colorama import Fore, Back, Style
import CLIbrary, dbase
import os, sys

dataPath = str(os.getcwd()) + "/data"
helpPath = str(os.getcwd()) + "/dbaseHelp.json"

try: # Check the existence or create the data folder.
	if not os.path.exists(dataPath):
		os.makedirs(dataPath)
	
except:
	print(Back.RED + Fore.WHITE + "DATA ERROR" + Style.RESET_ALL)
	sys.exit(-1)

print("dbaseManager")
print("Wrapper for dbase written in Python and built with CLIbrary for database management")
print("Developed by Andrea Di Antonio, more on https://github.com/diantonioandrea/dbase")
print("Type \'help\' if needed\n")

# Interface

current = None

while True:
	try: # Define a "shell prompt".
		cmdString = "[" + os.getlogin() + "@dbase"
	except:
		cmdString = "[unknown@dbase"

	if current != None:
		cmdString += "+" + current.name

	cmdString += "]"

	cmdHandler = {}
	cmdHandler["request"] = cmdString
	cmdHandler["style"] = Fore.MAGENTA
	cmdHandler["verboseStyle"] = Back.YELLOW
	cmdHandler["allowedCommands"] = ["new", "load"]
	cmdHandler["helpPath"] = helpPath

	if current != None:
		cmdHandler["allowedCommands"] += ["add", "fadd", "info", "show"]

		if len(current.entries) > 0:
			cmdHandler["allowedCommands"] += ["edel", "emod", "export"]

		if len(current.fields) > 1:
			cmdHandler["allowedCommands"] += ["fdel"]

		dumpHandler = {"path": dataPath + "/" + current.name + ".db", "data": current}
		CLIbrary.aDump(dumpHandler)

	command = CLIbrary.cmdIn(cmdHandler)

	cmd = command["command"]
	sdOpts = command["sdOpts"]
	ddOpts = command["ddOpts"]
	output = command["output"]

	if cmd == "exit":
		break

	if cmd == "help":
		print(output)
		continue

	if cmd == "new":
		current = dbase.dbase(CLIbrary.strIn({"request": "Database name", "noSpace": True}))
		continue

	if cmd == "load":
		toBeLoaded = ""

		if "n" in sdOpts:
			toBeLoaded = "/" + sdOpts["n"] + ".db"

		else:
			print(Back.RED + Fore.WHITE + "MISSING OPTION" + Style.RESET_ALL)
			continue

		loadHandler = {"path": dataPath + toBeLoaded}
		current = CLIbrary.aLoad(loadHandler)
		continue

	if current == None:
		continue

	if cmd == "info":
		print(str(current))
		continue

	if cmd == "show":
		if (len(sdOpts) > 0 and len(ddOpts) == 0) or (len(ddOpts) > 1):
			print(Back.RED + Fore.WHITE + "INCONSISTENT QUERIES" + Style.RESET_ALL)
			continue

		print(current.showEntries(sdOpts, ddOpts[0] if len(ddOpts) > 0 else ""))
		continue

	if cmd == "add":
		bulkNumber = 1

		if "n" in sdOpts:
			try:
				bulkNumber = max([int(sdOpts["n"]), 1])

			except(ValueError):
				bulkNumber = 1
				print(Back.RED + Fore.WHITE + "ARGUMENT ERROR, FALLING BACK TO 1" + Style.RESET_ALL)

		for _ in range(bulkNumber):
			current.addEntry()

		continue

	if cmd == "fadd":

		if len(current.entries) == 0:
			current.addField()
		
		elif CLIbrary.boolIn({"request": "Add a new field"}):
			current.addField()

		continue

	if cmd == "edel":
		serial = -1

		if "s" in sdOpts:
			try:
				serial = max([int(sdOpts["s"]), -1])

			except(ValueError):
				print(Back.RED + Fore.WHITE + "SERIAL ERROR" + Style.RESET_ALL)
				continue
		
		else:
			print(Back.RED + Fore.WHITE + "MISSING OPTION" + Style.RESET_ALL)
			continue

		toBeRemoved = None

		for entry in current.entries:
			if entry.fields["serial"] == serial:
				current.entries.remove(entry)

				print(entry)
				print(cmdHandler["verboseStyle"] + "Deleted" + Style.RESET_ALL)
				break
				
		continue
	
	if cmd == "fdel":
		if len(set(ddOpts).intersection(set([field["id"] for field in current.fields]))) == 0:
			print(Back.RED + Fore.WHITE + "FIELD NOT FOUND" + Style.RESET_ALL)
			continue

		for field in current.fields:
			if field["id"] in ddOpts:
				current.fields.remove(field)

				if current.sorter == field["id"]:
					current.sorter = ""

				for entry in current.entries:
					del entry.fields[field["id"]]
		
				print(cmdHandler["verboseStyle"] + field["id"] + " DELETED" + Style.RESET_ALL)
				break
		
		continue
	
	if cmd == "emod":
		serial = -1

		if "s" in sdOpts and len(ddOpts) > 0:
			try:
				serial = max([int(sdOpts["s"]), -1])

			except(ValueError):
				print(Back.RED + Fore.WHITE + "SERIAL ERROR" + Style.RESET_ALL)
				continue
		
		else:
			print(Back.RED + Fore.WHITE + "MISSING OPTIONS" + Style.RESET_ALL)
			continue

		for entry in current.entries:
			if entry.fields["serial"] == serial:
				toBeEdited = [field for field in current.fields if field["id"] in ddOpts]

				if len(toBeEdited) == 0:
					print(Back.RED + Fore.WHITE + "TO BE EDITED FIELDS NOT FOUND" + Style.RESET_ALL)
				
				oldEntry = str(entry)

				entry.insertFields(toBeEdited)

				print(cmdHandler["verboseStyle"] + "From" + Style.RESET_ALL)
				print(oldEntry)
				print(cmdHandler["verboseStyle"] + "To" + Style.RESET_ALL)
				print(entry)
				break
				
		continue
	
	if cmd == "export":
		if "f" in sdOpts:
			destination = dataPath + "/" + sdOpts["f"]
		else:
			print(Back.RED + Fore.WHITE + "MISSING OPTION" + Style.RESET_ALL)
			continue

		exportStatus = current.export(destination)
		
		if exportStatus["value"] != 0:
			print(Back.RED + Fore.WHITE + exportStatus["status"] + Style.RESET_ALL)
		
		else:
			print(cmdHandler["verboseStyle"] + "EXPORTED TO " + exportStatus["destination"] + Style.RESET_ALL)
		
		continue