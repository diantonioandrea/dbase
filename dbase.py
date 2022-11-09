from colorama import Fore, Back, Style
import CLIbrary

# Database utility built with CLIbrary

class dbase:
	def __init__(self, name) -> None:
		self.name = name # Database name.
		self.entries = [] # Databse entries.
		self.fields = [] # Database fields.
		
		self.sorter = "" # Database sorter field.
		
		self.serialCounter = 0 # Serial counter which gets updated on each new entry.
		
		# Initialization fields.
		while True:
			if CLIbrary.boolIn({"request": "Add a new field"}):
				self.addField()
			
			else:
				if len(self.fields) > 0:
					break
		
	def __str__(self) -> str: # Prints the database's infos.
		string = "Database: " + self.name + "\nEntries: " + str(len(self.entries))

		if self.sorter != "":
			string += "\nSorter: " + self.sorter

		string += "\nFields:"
		
		for field in self.fields:
			string += "\n\t" + field["id"] + ", " + field["type"]
			
		return string
	
	def addEntry(self) -> None: # Adds a new entry.
		newEntry = dbaseEntry(self)
		self.serialCounter += 1
		
		self.entries.append(newEntry)
			
	def addField(self) -> None: # Adds a new field.
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
		
		# Update all entries if any.
		
		for entry in self.entries:
			entry.insertFields([newField])
			
	def showEntries(self, sdOpts=[]) -> str: # Shows and queries entries.
		# sdOpts work as queries.
		
		self.sort()
		toBeShown = self.entries
		
		for queryKey in sdOpts:
			try:
				toBeShown = [entry for entry in toBeShown if sdOpts[queryKey] in str(entry.fields[queryKey])]
				
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
		
	def sort(self) -> None: # Sorts the entries.
		if self.sorter != "":
			self.entries.sort(key = lambda entry: entry.fields[self.sorter])
			
		else:
			self.entries.sort(key = lambda entry: entry.fields["serial"])

	def export(self, dest: str) -> dict: # Exports the database to a .csv file
		try:
			if ".csv" not in dest:
				dest += ".csv"

			csvFile = open(dest, "w")
		except:
			return {"value": -1, "status": "FILE ERROR"}

		csvString = "dbase .csv export for " + self.name + "\n"
		csvString += "serial," + ",".join(field["id"] for field in self.fields) + "\n"

		if self.sorter != "":
			csvString += "sorter: " + self.sorter + "\n"

		for entry in self.entries:
			csvString += "\n" + str(entry.fields["serial"]) + ","

			csvList = []

			for field in self.fields:
				csvList.append(str(entry.fields[field["id"]]))

			csvString += ",".join(csvList)

		csvFile.write(csvString)
		return {"value": 0, "status": "", "destination": dest}

class dbaseEntry:
	def __init__(self, database: dbase) -> None:
		self.fields = {}
		self.fields["serial"] = database.serialCounter
		
		self.insertFields(database.fields)
		
	def getStringSerial(self):
		return Fore.MAGENTA + str(self.fields["serial"]) + Style.RESET_ALL

	def __str__(self) -> str:
		string = Back.WHITE + "Serial: " + self.getStringSerial()
		
		for field in self.fields:
			if field != "serial":
				string += "\n\t" + field + ": " + str(self.fields[field])
				
		return string
		
	def insertFields(self, fields) -> None:
		print("Insert field(s) for serial: " + self.getStringSerial())
		
		for field in fields:
			if field["type"] == "number":
				self.fields[field["id"]] = CLIbrary.numIn({"request": "Insert " + field["id"]})
				
			elif field["type"] == "boolean":
				self.fields[field["id"]] = CLIbrary.boolIn({"request": "Insert " + field["id"]})
				
			elif field["type"] == "string":
				self.fields[field["id"]] = CLIbrary.strIn({"request": "Insert " + field["id"]})