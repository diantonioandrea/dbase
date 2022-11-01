manager:
	pyinstaller --onefile --console dbaseManager.py

dbase:
	mkdir dbase
	cp dbase.py dbase
	touch dbase/__init__.py
	echo "from .dbase import *" > dbase/__init__.py

clean:
	rm -rf dist build dbase data
	rm *.spec