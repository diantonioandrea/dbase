# Linux and macOS only

manager:
	pyinstaller --onefile --console dbaseManager.py
	mv dist/dbaseManager .

dbase:
	mkdir dbase
	cp dbase.py dbase
	touch dbase/__init__.py
	echo "from .dbase import *" > dbase/__init__.py

clean:
	rm -rf dist build dbase data
	rm *.spec dbaseManager