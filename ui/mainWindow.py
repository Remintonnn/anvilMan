import ctypes
import random
from enum import Enum

import hmmm_rc as resource
from calc.enchantments import Enchantment as Ench
from calc.enchantments import enchantments as enchs # not cap cuz it's an instance
from calc.enchantments import EnchantmentId as EnchId
from calc.enchantments import EnchantmentTags as EnchTag
from calc.enchantments import EnchantableItems as EnchItems
from ui.mainMenu import Ui_MainWindow

from PySide6.QtCore import Qt, QUrl, QDir, QTimer, QAbstractTableModel, QModelIndex, QEvent
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
        self.enchTable = enchTableControler(self.ui.enchTable,self.ui.generatePendingBookButton,self.ui.enchSelFrame)
        self.equSelection = equipmentSelectionControler(self.equSelectButtons(),self.enchTable)
        self.pendingTable = pendingTableControler(self.ui.pendingBookTable)

        self.mankAnvilLabel(self.ui.titleLabel)
        # self.ui.hatB.clicked.connect(self.test)
        # self.ui.clothB.clicked.connect(lambda: self.enchTable.clearItem())

    def equSelectButtons(self):
        ui = self.ui; EI = EnchItems
        return [
            [ui.hatB,EI.hat],
            [ui.clothB,EI.cloth],
            [ui.pantsB,EI.pants],
            [ui.shoesB,EI.shoes],
            [ui.wingB,EI.wing],
            [ui.swordB,EI.sword],
            [ui.axeB1,EI.axe],
            [ui.axeB2,EI.axe],
            [ui.spearB,EI.spear],
            [ui.maceB,EI.mase],
            [ui.tridentB,EI.trident],
            [ui.shieldB,EI.shield],
            [ui.crossbowB,EI.crossbow],
            [ui.bowB,EI.bow],
            [ui.pickaxeB,EI.pickaxe],
            [ui.shovelB,EI.shovel],
            [ui.hoeB,EI.hoe],
            [ui.shearsB,EI.shears],
            [ui.flientSteelB,EI.other]
        ]
    def mankAnvilLabel(self,label:QLabel):
        """all this for a joke lmao"""
        soundDir = ":/Sound/sounds/"
        anvilSounds:list[QSoundEffect] = []; noAnvilSounds:list[QSoundEffect] = []
        anvilUsed = 0; anvilLife = 5
        anvilCDTimer = QTimer(); anvilCDTimer.setSingleShot(True)
        anvilCDTimer.timeout.connect(lambda:label.setEnabled(True))
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
                label.setEnabled(False)
                if anvilLife <= 1:
                    oldFont = label.font()
                    oldFont.setPointSize(17)
                    label.setText("AIN'T NO FUCKING WAY")
                    label.setFont(oldFont)
                else:
                    anvilCDTimer.start(6767)
                    anvilLife -= 1
                return
            random.choice(anvilSounds).play()
            anvilUsed += 1
        label.mousePressEvent = playAnvil
    def test(self):
            self.saveTable.addItem(QIcon(r"ui/icons/sword.png"),"2026/12/25","The big man is here")
            self.enchTable.addItem(enchs[EnchId.gravity])
            self.enchTable.addItem(enchs[EnchId.efficiency])
            # addItem(enchTable,QCheckBox(),QCheckBox(),"動作音效 紲星燈", 4)


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

class equipmentSelectionControler:
    def __init__(self,buttons:list[list[QPushButton,Enum]],enchTable:"enchTableControler"):
        self.buttons = []
        self.enchTable = enchTable
        self.theChosenOne:QPushButton = None
        for button,item in buttons:
            button:QPushButton;item:Enum
            # print(f"connecting {button.objectName()} for {item.value}")
            self.buttons.append(button)
            button.mousePressEvent = lambda e, b=button, i=item: self.buttonAction(b,i)
            button.mouseDoubleClickEvent = lambda e, b=button, i=item: self.buttonAction(b,i)

    def buttonAction(self,button:QPushButton,item:Enum):
        if self.theChosenOne != None: # unchoosing chosen one:sob:
            self.theChosenOne.setProperty("chosenOne",False)
            repolish(self.theChosenOne)
        if button != self.theChosenOne:
            button.setProperty("chosenOne",True)
            repolish(button)
            self.theChosenOne = button
            self.enchTable.populateFromNewItem(item)
        else:
            self.theChosenOne = None
            self.enchTable.clearItem()

class enchTableControler:
    def __init__(self, table:QTableView, confirmButton:QPushButton, enchSelectionFrame:QFrame):
        self.table = table
        self.model = EnchTableModel()
        self.enchSelectionFrame = enchSelectionFrame
        self.grayOut(True)
        table.setModel(self.model)
        delegate = CheckBoxDelegate()
        table.setItemDelegateForColumn(0, delegate)
        table.setItemDelegateForColumn(1, delegate)
        
        
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        table.setColumnWidth(0, 35)
        table.setColumnWidth(1, 59)
        # print(table.columnWidth(2)) -> 89
        table.setColumnWidth(3, 55)
        table.verticalHeader().hide()

    def populateFromNewItem(self,item:Enum):
        self.clearItem()
        self.grayOut(False)
        for ID, ench in enchs.dict.items():
            if ench.isCompatibleWith(item):
                self.addItem(ench)

    def addItem(self, ench:Ench):
        self.model.addItem(ench)
        self.table.resizeRowsToContents()
    def clearItem(self): self.model.clearData();self.grayOut(True)
    def grayOut(self,doIt:bool): 
        self.enchSelectionFrame.setDisabled(doIt)
        self.table.verticalScrollBar().setProperty("grayOut",doIt)
        repolish(self.table.verticalScrollBar())
class EnchTableModel(QAbstractTableModel):
    # Mutex column doesn't exist because yes
    SELECTED_COL, FROMONEUP_COL, NAME_COL, LEVEL_COL, MUTEX_COL = [0,1,2,3,4]
    HEADERS = ["選取","從I打起","名稱","目標等級"]
    ConflictedRole = Qt.ItemDataRole.UserRole+1

    def __init__(self):
        super().__init__()
        self._data = []

    def addItem(self,ench:Ench,selected=None,fromOneUp=None,lvl=None):
        row = self.rowCount()
        self.beginInsertRows(QModelIndex(), row, row)
        if selected is None: selected = False
        if fromOneUp is None: fromOneUp = EnchTag.catBud in ench.tags
        if lvl is None: lvl = ench.maxlvl
        self._data.append([selected,fromOneUp,ench,lvl,[]])
        self.endInsertRows()
    def clearData(self):
        self.beginResetModel()
        self._data.clear()
        self.endResetModel()

    def data(self, index:QModelIndex, role:Qt.ItemDataRole):
        col, row = index.column(),index.row()
        selected,fromOneUp,ench,lvl,mutex = self._data[row]
        selected:bool;fromOneUp:bool;ench:Ench;lvl:int;mutex:list[Ench]
        if role == Qt.ItemDataRole.DisplayRole:
            if col == self.NAME_COL: return ench.names[0]
            if col == self.LEVEL_COL: return getRomanNum(lvl)
        if role == Qt.ItemDataRole.CheckStateRole:
            if col == self.SELECTED_COL: return Qt.CheckState.Checked if selected else Qt.CheckState.Unchecked
            if col == self.FROMONEUP_COL: return Qt.CheckState.Checked if fromOneUp else Qt.CheckState.Unchecked
        if role == Qt.ItemDataRole.ForegroundRole:
            if len(mutex) != 0: return QColor("#676767")
            if fromOneUp: return QColor("#FFA600")
        if role == Qt.ItemDataRole.TextAlignmentRole: return Qt.AlignmentFlag.AlignCenter
        if role == self.ConflictedRole: return len(mutex)==0
    def setData(self, index, value, /, role = ...):
        col, row = index.column(),index.row()
        if role == Qt.ItemDataRole.CheckStateRole:
            if col not in (self.SELECTED_COL,self.FROMONEUP_COL): return False
            self._data[row][col] = value==Qt.CheckState.Checked

            self.dataChanged.emit(
                self.index(row, 2), 
                self.index(row, 3), # This is a range
                [
                    Qt.ItemDataRole.CheckStateRole,
                    Qt.ItemDataRole.ForegroundRole,
                    Qt.ItemDataRole.DisplayRole,
                ]
            )
            return True
        return False

    def flags(self, index):
        flags = Qt.ItemFlag.ItemIsEnabled
        if index.column() in (0,1): flags |= Qt.ItemFlag.ItemIsUserCheckable
        return flags

    def rowCount(self, index=0): return len(self._data)
    def columnCount(self, index=0): return 4
    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role != Qt.ItemDataRole.DisplayRole: return
        if orientation == Qt.Vertical: return
        if orientation == Qt.Horizontal:
            return str(self.HEADERS[section])
class CheckBoxDelegate(QStyledItemDelegate):
    def __init__(self):
        super().__init__()
        self.checked = QIcon(":/UI/checked.png").pixmap(16,16)
        self.unchecked = QIcon(":/UI/unChecked.png").pixmap(16,16)

    def paint(self, painter, option, index):
        if index.column() not in (0,1): super().paint(painter, option, index); return
        checkState = index.data(Qt.ItemDataRole.CheckStateRole) == Qt.CheckState.Checked
        conflicted = index.data(EnchTableModel.ConflictedRole)
        pix = self.checked if checkState else self.unchecked
        x = option.rect.center().x() - pix.width()//2
        y = option.rect.center().y() - pix.height()//2
        painter.drawPixmap(x,y,pix)

    def editorEvent(self, event, model, option, index):
        # MouseButtonDoubleClick is called on the second mouse DOWN
        if event.type() in (QEvent.Type.MouseButtonPress,QEvent.Type.MouseButtonDblClick):
            checkState = index.data(Qt.CheckStateRole)==Qt.CheckState.Checked
            model.setData(index, Qt.CheckState.Unchecked if checkState else Qt.CheckState.Checked, Qt.ItemDataRole.CheckStateRole)
            return True
        return False


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
def repolish(b:QPushButton):
    """QT jank"""
    b.style().unpolish(b)
    b.style().polish(b)
    b.update()