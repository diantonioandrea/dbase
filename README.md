[![GitHub license](https://img.shields.io/github/license/diantonioandrea/dbase)](https://github.com/diantonioandrea/dbase/blob/main/LICENSE)

# dbase

Database utility written in Python and built with [CLIbrary](https://github.com/diantonioandrea/CLIbrary).

## Usage

**dbaseManager** can be built by:

	make manager

**dbase** can be integrated in an existing project by:

	make dbase

and inserting the resulting folder into the project, remembering to import **dbase** by:

	import dbase

## Commands

**dbaseManager** supports its own help through **CLIbrary**'s help system.  
By:

	help

you'll obtain:

	exit
			Exits the program.
	new
			Creates a new database.
	load
			Loads the specified database from a .db file.
			Options:
					-n DATABASE_NAME
	add
			Adds a new entry.
			Options:
					-n ENTRIES_NUMBER
	info
			Shows database's infos.
	show
			Prints the database entries with optional queries passed as single dash options and a query mode passed as a double dash option. The available flags are: in, eq, neq, gt, lt, geq, leq.
			Options:
					-FIELD_1 QUERY_1 ... -FIELD_N QUERY_N --QUERYFLAG
	edel
			Deletes the specified entry by passing its serial number.
			Options:
					-s ENTRY_SERIAL
	emod
			Edits the specified entry by passing its serial number and at least one field.
			Options:
					-s ENTRY_SERIAL --FIELD_1 ... --FIELD_N
	fadd
			Adds a new field with a dedicated prompt.
	fdel
			Deletes the specified field by passing its serial name as a double dash option.
			Options:
					--FIELD
	export
			Exports the database to a .csv file into the data/ folder.
			Options:
					-f FILENAME

Color coding, in **dbaseManager** will help you distinguish between optional and mandatory options.