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

	exit

Exits **dbaseManager**.

	new

Creates a new database.

	load -n FILENAME

Loads an existing database from a *.db* file.

	add

Adds a new entry to the database.

	info

Shows infos on the database.

	show [-FIELD_1 QUERY_1 ... -FIELD_N QUERY_N]

Prints the database entry with optional queries passed as single dash options.