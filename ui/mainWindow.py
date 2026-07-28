import ctypes
import random
import time

import hmmm_rc as resource
from calc.enchantments import Enchantment as Ench
from calc.enchantments import enchantments as enchs # not cap cuz it's an instance
from calc.enchantments import EnchantmentId as EnchId
from calc.enchantments import EnchantmentTags as EnchTag
from ui.mainMenu import Ui_MainWindow

from PySide6.QtCore import Qt, QUrl, QDir, QTimer
from PySide6.QtWidgets import * # QApplication, QStyleFactory, QHeaderView, QTableWidgetItem
from PySide6.QtUiTools import * # QUiLoader
from PySide6.QtGui import * # QIcon
from PySide6.QtMultimedia import QSoundEffect

aGlobal = 0

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.window().setFixedHeight(self.window().height())
        self.window().setFixedWidth(self.window().width())
        tryGetDarkTitleBar(self.window())
        self.saveTable = saveTableControler(self.ui.saveTable)
        self.enchTable = enchTableControler(self.ui.enchTable)
        self.pendingTable = pendingTableControler(self.ui.pendingBookTable)

        # all this for a joke lmao
        soundDir = ":/Sound/sounds/"
        anvilSounds:list[QSoundEffect] = []; noAnvilSounds:list[QSoundEffect] = []
        anvilUsed = 0; anvilLife = 5
        anvilCDTimer = QTimer(); anvilCDTimer.setSingleShot(True)
        anvilCDTimer.timeout.connect(lambda:self.ui.titleLabel.setEnabled(True))
        for file in QDir(soundDir).entryList():
            sound = QSoundEffect(source=QUrl("qrc"+soundDir+file)) # qrc is necessary here
            if file.startswith("anvil"):
                anvilSounds.append(sound)
                if file != "anvilD3.wav": anvilSounds.append(sound) # less *DEEP* sound
            elif file.startswith("noAnvil"): noAnvilSounds.append(sound)
        def playAnvil(e):
            nonlocal anvilUsed, anvilLife
            if anvilUsed >= 16:
                random.choice(noAnvilSounds).play()
                anvilUsed = 0
                self.ui.titleLabel.setEnabled(False)
                if anvilLife <= 1:
                    oldFont = self.ui.titleLabel.font()
                    oldFont.setPointSize(17)
                    self.ui.titleLabel.setText("AIN'T NO FUCKING WAY")
                    self.ui.titleLabel.setFont(oldFont)
                else:
                    anvilCDTimer.start(6767)
                    anvilLife -= 1
                return
            random.choice(anvilSounds).play()
            anvilUsed += 1
        self.ui.titleLabel.mousePressEvent = playAnvil

        self.ui.hatB.clicked.connect(self.test)


    def test(self):
            self.saveTable.addItem(QIcon(r"ui/icons/sword.png"),"2026/12/25","The big man is here")
            self.enchTable.addItem(enchs[EnchId.gravity])
            self.enchTable.addItem(enchs[EnchId.efficiency])
            # addItem(enchTable,QCheckBox(),QCheckBox(),"動作音效 紲星燈", 4)


# Should've use TableView for these...
# Too bad I just clicked on the first thing that says TABLE in QT Designer
class saveTableControler:
    def __init__(self, table:QTableWidget):
        self.table:QTableWidget = table
        table.setWordWrap(True)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        table.setColumnWidth(0, 35)
        table.setColumnWidth(1, 65)
    def addItem(self,icon:QIcon,date:str,name:str):
        row = self.table.rowCount()
        self.table.insertRow(row)

        iconObj = QLabel()
        iconObj.setPixmap(icon.pixmap(16,16))
        iconObj.setAlignment(Qt.AlignmentFlag.AlignCenter)
        iconObj.setStyleSheet("background: transparent; border: none;")
        dateObj = QTableWidgetItem(date)
        dateObj.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        nameObj = QTableWidgetItem(name)
        # nameObj.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.table.setCellWidget(row,0, iconObj)
        self.table.setItem(row,1, dateObj)
        self.table.setItem(row,2, nameObj)
        self.table.resizeRowsToContents()

class enchTableControler:
    def __init__(self, table:QTableWidget):
        PMS = 16
        self.__CHECKED__ = QIcon(":/UI/checked.png").pixmap(PMS,PMS)
        self.__UNCHECKED__ = QIcon(":/UI/unChecked.png").pixmap(PMS,PMS)
        self.table = table
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        table.setColumnWidth(0, 35)
        table.setColumnWidth(1, 59)
        # print(table.columnWidth(2)) -> 89
        table.setColumnWidth(3, 55)
        # self.table.cellClicked only emit event on mouse UP instead of DOWN, which feels terrible
        # cellDoubleClicked is called on mouse DOWN
        self.table.cellPressed.connect(self.onCellClicked)
        self.table.cellDoubleClicked.connect(self.onCellClicked)

    def addItem(self, ench:Ench):
        row = self.table.rowCount()
        self.table.insertRow(row)

        # the build in check box and QCheck box has a problem where
        # the click is only registerted when mouse been pressed DOWN then UP at the check box
        # which can cause the click to not reg if your mouse is moving, which is annoying
        # also centering the build in one requires you to write a delegate youself

        # selContainter = QWidget()
        # selCB = QCheckBox()
        # selCB.checkStateChanged.connect(lambda state: self.onEnchSel(state,ench))
        # selLayout = QHBoxLayout(selContainter)
        # selLayout.addWidget(selCB)
        # selLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # selLayout.setContentsMargins(0,0,0,0)

        # selCB = QTableWidgetItem()
        # selCB.setCheckState(Qt.CheckState.Unchecked)

        selCB = QLabel()
        selCB.setStyleSheet("background: transparent; border: none;")
        selCB.setProperty("checked", False)
        selCB.setProperty("ench", ench)
        selCB.setPixmap(self.__UNCHECKED__)
        selCB.setAlignment(Qt.AlignmentFlag.AlignCenter)

        fromOneUpCB = QLabel()
        fromOneUpCB.setStyleSheet("background: transparent; border: none;")
        fromOneUpCB.setAlignment(Qt.AlignmentFlag.AlignCenter)
        isBud = EnchTag.catBud in ench.tags
        fromOneUpCB.setProperty("checked", isBud)
        fromOneUpCB.setPixmap(self.__CHECKED__ if isBud else self.__UNCHECKED__)
        
        nameObj = QTableWidgetItem(ench.names[0])
        nameObj.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        lvlObj = QTableWidgetItem(getRomanNum(ench.maxlvl))
        lvlObj.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

        self.table.setCellWidget(row,0, selCB)
        self.table.setCellWidget(row,1, fromOneUpCB)
        self.table.setItem(row,2, nameObj)
        self.table.setItem(row,3, lvlObj)
        self.table.resizeRowsToContents()

    def onCellClicked(self,row,column):
        if column in (0,1):
            cell:QLabel = self.table.cellWidget(row, column)
            cellState:bool = cell.property("checked")
            cell.setProperty("checked", not cellState)
            cell.setPixmap(self.__UNCHECKED__ if cellState else self.__CHECKED__)
            if column != 0: return
            ench:Ench = cell.property("ench")
            global aGlobal
            print("clikie "+ str(aGlobal) + " for " + ench.names[0])
            print(f"state now: {not cellState}")
            aGlobal += 1

class pendingTableControler:
    def __init__(self, table:QTableWidget):
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        table.setColumnWidth(0, 120)
        table.setColumnWidth(1, 59)
        # print(table.columnWidth(2)) -> 369

def tryGetDarkTitleBar(window, dark=True):
    try:
        hwnd = int(window.winId())
        # Windows 10 1809+ / Windows 11
        DWMWA_USE_IMMERSIVE_DARK_MODE = 20
        value = ctypes.c_int(1 if dark else 0)
        ctypes.windll.dwmapi.DwmSetWindowAttribute(
            hwnd,
            DWMWA_USE_IMMERSIVE_DARK_MODE,
            ctypes.byref(value),
            ctypes.sizeof(value)
        )
    except Exception as e:
        print(f"Unable to set window frame theme: {e}")

def getRomanNum(n):
    """up to 10 cuz lazy"""
    ROMAN_NUMS = {1:"I",2:"II",3:"III",4:"IV",5:"V",6:"VI",7:"VII",8:"VIII",9:"IX",10:"X"}
    rom = ROMAN_NUMS.get(n)
    return str(n) if rom is None else rom

def addItem(table:QTableWidget,*args):
    """Just for testing, will write individual function for each table"""
    row = table.rowCount()
    table.insertRow(row)
    for index,item in enumerate(args):
        if(isinstance(item, QIcon)):
            thing = QTableWidgetItem()
            thing.setIcon(item)
            table.setItem(row,index,thing)
        elif(isinstance(item, str)):
            table.setItem(row,index, QTableWidgetItem(item))
        elif(isinstance(item,int)):
            table.setItem(row,index, QTableWidgetItem(str(item)))
        else:
            table.setCellWidget(row,index,item)
    table.resizeRowsToContents()