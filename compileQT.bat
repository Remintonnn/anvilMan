rem hmmm_rc.py has to be in the root folder because compiled mainMenu.py always assume it's there
pyside6-rcc ui/resources/hmmm.qrc -o hmmm_rc.py
pyside6-uic ui/resources/QtFiles/mainMenu.ui -o ui/resources/QtFiles/mainMenu.py