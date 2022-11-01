from colorama import Fore, Back, Style
import CLIbrary

# Database utility built with CLIbrary

class dbase:
	def __init__(self, name) -> None:
		self.name = name
		self.entries = []
		self.fields = []
		
		self.sorter = ""
		
		self.serialCounter = 0
		
		while True:
			if CLIbrary.boolIn({"request": "Add a new field"}):
				self.addField()
			
			else:
				if len(self.fields) > 0:
					break
		
	def __str__(self) -> str:
		string = "Database: " + self.name + "\nEntries: " + str(len(self.entries))

		if self.sorter != "":
			string += "\nSorter: " + self.sorter

		string += "\nFields:"
		
		for field in self.fields:
			string += "\n\t" + field["id"] + ", " + field["type"]
			
		return string
	
	def addEntry(self) -> None:
		newEntry = dbaseEntry(self)
		self.serialCounter += 1
		
		self.entries.append(newEntry)
			
	def addField(self) -> None:
		newField = {}

		fieldHandler = {}
		typeHandler = {}

		fieldHandler["request"] = "Field identifier"
		fieldHandler["blockedAnswers"] = ["serial"]
		typeHandler["request"] = "Field type"
		typeHandler["allowedAnswers"] = ["number", "string"]
		
		newField["id"] = CLIbrary.strIn(fieldHandler)

		if newField["id"] != "sorter":
			typeHandler["allowedAnswers"].append("boolean")
		
		if newField["id"] == "sorter":
			fieldHandler["request"] = "Sorter field identifier"
			newField["id"] = CLIbrary.strIn(fieldHandler)
			self.sorter = newField["id"]

		newField["type"] = CLIbrary.strIn(typeHandler)
			
		self.fields.append(newField)
		print("Field added")
		
		# Update all entries if any
		
		for entry in self.entries:
			entry.insertField([newField])
			
	def showEntries(self, sdOpts=[]) -> str:
		# sdOpts work as queries
		
		self.sort()
		toBeShown = self.entries
		
		for sdOption in sdOpts:
			try:
				toBeShown = [entry for entry in toBeShown if sdOption[1] in str(entry.fields[sdOption[0].replace("-", "")])]
				
			except:
				pass
		
		string = "Entries for database: " + self.name
		
		if len(sdOpts) > 0:
			string += ", queried\nShowing " + str(len(toBeShown)) + " out of " + str(len(self.entries)) + " entries"
		
		for entry in toBeShown:
			string += "\n" + str(entry)
			
		if len(toBeShown) == 0:
			string += "\nNothing to see here"
			
		return string
		
	def sort(self) -> None:
		if self.sorter != "":
			self.entries.sort(key = lambda entry: entry.fields[self.sorter])
			
		else:
			self.entries.sort(key = lambda entry: entry.fields["serial"])

class dbaseEntry:
	def __init__(self, database: dbase) -> None:
		self.fields = {}
		self.fields["serial"] = database.serialCounter
		
		self.insertField(database.fields)
		
	def getStringSerial(self):
		return Fore.MAGENTA + str(self.fields["serial"]) + Style.RESET_ALL

	def __str__(self) -> str:
		string = Back.WHITE + "Serial: " + self.getStringSerial()
		
		for field in self.fields:
			if field != "serial":
				string += "\n\t" + field + ": " + str(self.fields[field])
				
		return string
		
	def insertField(self, fields) -> None:
		print("Insert field(s) for serial: " + self.getStringSerial())
		
		for field in fields:
			if field["type"] == "number":
				self.fields[field["id"]] = CLIbrary.numIn({"request": "Insert " + field["id"], "verbose": True})
				
			elif field["type"] == "boolean":
				self.fields[field["id"]] = CLIbrary.boolIn({"request": "Insert " + field["id"], "verbose": True})
				
			elif field["type"] == "string":
				self.fields[field["id"]] = CLIbrary.strIn({"request": "Insert " + field["id"], "verbose": True})