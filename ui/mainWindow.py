import ctypes
import random
from enum import Enum

import hmmm_rc as resource
from calc import calc
from calc.calc import Book
from calc.enchantments import Enchantment as Ench
from calc.enchantments import enchantments as enchs # not cap cuz it's an instance
from calc.enchantments import EnchantmentId as EnchId
from calc.enchantments import EnchantmentTags as EnchTag
from calc.enchantments import EnchantableItems as EnchItems
from ui.mainMenu import Ui_MainWindow

from PySide6.QtCore import Qt, QUrl, QDir, QTimer, QAbstractTableModel, QModelIndex, QEvent, QObject, Signal
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
        self.saveTable = SaveTableControler(self.ui.saveTable)
        self.enchTable = EnchTableControler(self.ui.enchTable,self.ui.enchSelFrame)
        self.pendingTable = PendingTableControler(self.ui.pendingBookTable,self.ui.pendingBookFram,self.ui.pendingBookSlotDisplayLabel)
        self.equSelection = EquipmentSelectionControler(self.equSelectButtons())

        self.mankAnvilLabel(self.ui.titleLabel)
        self.ui.enchSelHighlightCheckBox.toggled.connect(self.enchTable.setSelectdHighlight)
        self.ui.enchSelHighlightCheckBox.toggle()
        self.ui.theOneTheOriTHEONETHEORITOTOtotoTOTALtoto.clicked.connect(self.generateSteps)

        self.equSelection.oneHasBeenChosen.connect(self.onEquChoose)
        self.enchTable.model.updatePending.connect(self.generatePendingBooks)

    def onEquChoose(self,button:QPushButton,item:Enum):
        self.pendingTable.clearItem()
        if button is None: self.enchTable.clearItem(); return # generatePendingBooks will clear it again otherwise
        self.enchTable.populateFromNewItem(item)
        self.generatePendingBooks()
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
        totalSound = 0

        for file in QDir(soundDir).entryList():
            sound = QSoundEffect(source=QUrl("qrc"+soundDir+file)) # qrc is necessary here
            if file.startswith("anvil"):
                totalSound += 1
                if file == "anvilD3.wav": # less *DEEP* sound
                    anvilSounds.append(sound)
                else: 
                    for i in range(totalSound): anvilSounds.append(sound)
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
    def generatePendingBooks(self):
        # global aGlobal
        # aGlobal+=1; print("GEN PENDING BOOKS "+str(aGlobal))
        data = self.enchTable.gimmeTheThing()
        books = calc.generateBooks(data,self.equSelection.theChosenItem)
        self.pendingTable.clearItem()
        self.pendingTable.setItems(books,self.equSelection.getChosenIcon())
    def generateSteps(self):
        targetEnch = self.enchTable.gimmeTheThing()
        bookBag = self.pendingTable.gimmeTheThing()
        calc.generateSteps(targetEnch,bookBag)
    def test(self):
            self.saveTable.addItem(QIcon(r"ui/icons/sword.png"),"2026/12/25","The big man is here")
            self.enchTable.addItem(enchs[EnchId.gravity])
            self.enchTable.addItem(enchs[EnchId.efficiency])
            # addItem(enchTable,QCheckBox(),QCheckBox(),"動作音效 紲星燈", 4)


class SaveTableControler:
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

class EquipmentSelectionControler(QObject): # QObject just for the signal
    oneHasBeenChosen:Signal = Signal(QPushButton,Enum)
    buttons = []
    theChosenOne:QPushButton = None
    theChosenItem:Enum = None
    def __init__(self,buttons:list[list[QPushButton,Enum]]):
        super().__init__()
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
            self.theChosenItem = item
        else:
            self.theChosenOne = None
            self.theChosenItem = None
        self.oneHasBeenChosen.emit(self.theChosenOne,self.theChosenItem)
    def getChosenIcon(self):
        if self.theChosenOne is None: return None
        return self.theChosenOne.icon()

class EnchTableControler:
    def __init__(self, table:QTableView, enchSelectionFrame:QFrame):
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

        self.filter = self.filterObj(self,table.viewport())
        table.viewport().installEventFilter(self.filter) # for the level scroll
    class filterObj(QObject):
        def __init__(self, controller:"EnchTableControler", parent=None):
            super().__init__(parent) # To prevent effor when close program
            self.controller = controller
        def eventFilter(self, obj, event): # for the level scroll
            if obj == self.controller.table.viewport():
                if event.type() == QEvent.Type.Wheel:
                    index = self.controller.table.indexAt(event.position().toPoint())
                    if index.isValid() and index.column() == EnchTableModel.LEVEL_COL:
                        self.controller.model.changelvl(index.row(), event.angleDelta().y()>0)
                        return True
            return super().eventFilter(obj, event)

    def populateFromNewItem(self,item:Enum):
        self.clearItem()
        self.grayOut(False)
        for ID, ench in enchs.dict.items():
            if ench.isCompatibleWith(item):
                self.model.addItem(ench)
        self.table.resizeRowsToContents()

    def setSelectdHighlight(self, doIt:bool|Qt.CheckState):
        if isinstance(doIt,Qt.CheckState): doIt = doIt==Qt.CheckState.Checked
        self.model.setSelectdHighlight(doIt)
    def clearItem(self): self.model.clearData();self.grayOut(True)
    def grayOut(self,doIt:bool): 
        self.enchSelectionFrame.setDisabled(doIt)
        self.table.verticalScrollBar().setProperty("grayOut",doIt)
        repolish(self.table.verticalScrollBar())

    def gimmeTheThing(self):
        """get a copy of the table's data"""
        return self.model.giveUTheThing()
class EnchTableModel(QAbstractTableModel):
    # Mutex column doesn't exist because yes
    SELECTED_COL, FROMONEUP_COL, NAME_COL, LEVEL_COL, MUTEX_COL = [0,1,2,3,4]
    HEADERS = ["選取","從I打起","名稱","目標等級"]
    ConflictedRole = Qt.ItemDataRole.UserRole+1
    updatePending = Signal()
    _data:list[tuple[bool,bool,Ench,int,list[Ench]]] = []
    highlightSelected = True
    selectedEnch = 0

    def __init__(self): super().__init__()

    def addItem(self,ench:Ench,selected=None,fromOneUp=None,lvl=None):
        # The mutex list means the currently conflicting enchantments that's selected
        # so it will always be init as empty because no enchantment has been selected yet
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
        self.selectedEnch = 0

    def data(self, index:QModelIndex, role:Qt.ItemDataRole):
        col, row = index.column(),index.row()
        selected,fromOneUp,ench,lvl,mutex = self._data[row]
        selected:bool;fromOneUp:bool;ench:Ench;lvl:int;mutex:list[Ench]
        if role == Qt.ItemDataRole.DisplayRole:
            if col == self.NAME_COL: return ench.names[0].replace(" ","\n")
            if col == self.LEVEL_COL: return getRomanNum(lvl)
        if role == Qt.ItemDataRole.CheckStateRole:
            if col == self.SELECTED_COL: return Qt.CheckState.Checked if selected else Qt.CheckState.Unchecked
            if col == self.FROMONEUP_COL: return Qt.CheckState.Checked if fromOneUp else Qt.CheckState.Unchecked
        if role == Qt.ItemDataRole.BackgroundRole:
            if len(mutex) != 0: return QColor("#171717")
            if selected and self.shouldHighlight(): return QColor("#2A2A2A")
        if role == Qt.ItemDataRole.ForegroundRole:
            if len(mutex) != 0:
                if col == self.LEVEL_COL and lvl!=ench.maxlvl:
                    return QColor("#0E4400") if fromOneUp else QColor("#4B2247")
                return QColor("#553803") if fromOneUp else QColor("#454545")
            if col == self.LEVEL_COL and lvl!=ench.maxlvl:
                return QColor("#38FF07") if fromOneUp else QColor("#FF6FF3")
                # return QColor("#07FFF3")
            # if self.shouldHighlight():
            #     if fromOneUp: return QColor("#FFA600") if selected else QColor("#C58001")
            #     if not selected: return QColor("#A7A7A7")
            # else:
            if fromOneUp: return QColor("#FFA600")
        if role == Qt.ItemDataRole.TextAlignmentRole: return Qt.AlignmentFlag.AlignCenter
        if role == Qt.ItemDataRole.FontRole:
            if col == self.NAME_COL and selected and self.shouldHighlight():
                font = QFont();font.setBold(True)
                return font
            if col == self.LEVEL_COL and lvl!=ench.maxlvl:
                font = QFont();font.setBold(True);font.setItalic(True)
                return font
        if role == self.ConflictedRole: return len(mutex)!=0
    def setData(self, index, value, /, role = ...):
        col, row = index.column(),index.row()
        if role == Qt.ItemDataRole.CheckStateRole:
            if col not in (self.SELECTED_COL,self.FROMONEUP_COL): return False
            stateNow = value==Qt.CheckState.Checked
            self._data[row][col] = stateNow

            if col == self.SELECTED_COL:
                self.updatePending.emit()
                if stateNow: 
                    if self.selectedEnch == 0:
                        self.beginResetModel()
                        self.selectedEnch += 1
                        self.endResetModel()
                    else: self.selectedEnch += 1
                else:
                    if self.selectedEnch == 1:
                        self.beginResetModel()
                        self.selectedEnch -= 1
                        self.endResetModel()
                    else: self.selectedEnch -= 1
                ench:Ench = self._data[row][self.NAME_COL]
                if len(ench.mutexEnch)!=0:
                    for dataIndex in range(len(self._data)):
                        data = self._data[dataIndex]
                        if not ench.conflictsWith(data[self.NAME_COL]): continue
                        if stateNow: data[self.MUTEX_COL].append(ench)
                        else: data[self.MUTEX_COL].remove(ench)
                        self.dataChanged.emit(
                            self.index(dataIndex, 0),
                            self.index(dataIndex, 3), # This is a range
                            [
                                Qt.ItemDataRole.CheckStateRole,
                                Qt.ItemDataRole.ForegroundRole,
                                Qt.ItemDataRole.BackgroundRole,
                                Qt.ItemDataRole.DisplayRole,
                            ]
                        )
            elif self._data[row][self.SELECTED_COL]: self.updatePending.emit()
            self.dataChanged.emit(
                self.index(row, 0), 
                self.index(row, 3), # This is a range
                [
                    Qt.ItemDataRole.CheckStateRole,
                    Qt.ItemDataRole.ForegroundRole,
                    Qt.ItemDataRole.DisplayRole,
                ]
            )
            return True
        return False
    def changelvl(self,row:int,lvlUp:bool):
        if self.data(self.index(row,0),self.ConflictedRole): return
        lvlCap = self._data[row][self.NAME_COL].maxlvl
        lvlNow = self._data[row][self.LEVEL_COL]
        lvlNow = lvlNow+1 if lvlUp else lvlNow-1
        if lvlNow in (0,lvlCap+1): return
        # print(f"LEVEL CHANGE AT ROW {row} GOING {"up" if lvlUp else "down"} from {lvlOld} to {lvlNow}")
        self._data[row][self.LEVEL_COL] = lvlNow
        index = self.index(row,self.LEVEL_COL)
        if self._data[row][self.SELECTED_COL]: self.updatePending.emit()
        self.dataChanged.emit(index,index,[Qt.ItemDataRole.FontRole,Qt.ItemDataRole.DisplayRole])
    def giveUTheThing(self):
        """get a list of all ench selected"""
        result = [[data[1],data[2],data[3]] for data in self._data if data[0]]
        return result

    def flags(self, index):
        flags = Qt.ItemFlag.ItemIsEnabled
        if index.column() in (0,1): flags |= Qt.ItemFlag.ItemIsUserCheckable
        return flags
    def shouldHighlight(self):
        return self.highlightSelected and self.selectedEnch!=0
    def setSelectdHighlight(self, value:bool):
        if value == self.highlightSelected: return
        self.beginResetModel()
        self.highlightSelected = value
        self.endResetModel()
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
        self.checkedGrayout = QIcon(":/UI/checkedGrayout.png").pixmap(16,16)
        self.uncheckedGrayout = QIcon(":/UI/unCheckedGrayout.png").pixmap(16,16)
    def paint(self, painter, option, index):
        if index.column() not in (0,1): return
        opt = QStyleOptionViewItem(option)
        self.initStyleOption(opt, index)
        opt.features &= ~QStyleOptionViewItem.ViewItemFeature.HasCheckIndicator
        style = opt.widget.style() if opt.widget else QApplication.style()
        style.drawControl(QStyle.ControlElement.CE_ItemViewItem, opt, painter, opt.widget)

        checkState = index.data(Qt.ItemDataRole.CheckStateRole) == Qt.CheckState.Checked
        conflicted = index.data(EnchTableModel.ConflictedRole)
        pix = None
        if conflicted: pix = self.checkedGrayout if checkState else self.uncheckedGrayout
        else: pix = self.checked if checkState else self.unchecked
        x = option.rect.center().x() - pix.width()//2
        y = option.rect.center().y() - pix.height()//2
        painter.drawPixmap(x,y,pix)

    def editorEvent(self, event, model, option, index:QModelIndex):
        conflicted = index.data(EnchTableModel.ConflictedRole)
        if conflicted: return False
        # MouseButtonDoubleClick is called on the second mouse DOWN
        if event.type() in (QEvent.Type.MouseButtonPress,QEvent.Type.MouseButtonDblClick):
            checkState = index.data(Qt.CheckStateRole)==Qt.CheckState.Checked
            model.setData(index, Qt.CheckState.Unchecked if checkState else Qt.CheckState.Checked, Qt.ItemDataRole.CheckStateRole)
            return True
        return False

class PendingTableControler:
    def __init__(self, table:QTableView, pendingBookFrame:QFrame,slotLabel:QLabel):
        self.table = table
        self.model = pendingTableModel()
        self.pendingBookFrame = pendingBookFrame
        self.slotLabel = slotLabel
        delegate = AmountDisplayDelegate()
        table.setItemDelegateForColumn(pendingTableModel.AMOUNT_ICON_COL,delegate)
        self.grayOut(True)
        table.setModel(self.model)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        table.setColumnWidth(0, 120)
        table.setColumnWidth(1, 39)
        # print(table.columnWidth(2)) -> 330
        table.setColumnWidth(3, 39)

        table.verticalHeader().hide()
    def setItems(self,bookBag:list[Book],currentIcon:QIcon):
        self.model.setItems(bookBag,currentIcon)
        self.table.resizeRowsToContents()
        self.grayOut(False)
        self.slotLabel.setText(self.model.getSlotLabelText())
    def clearItem(self): self.model.clearData();self.grayOut(True)
    def grayOut(self,doIt:bool): 
        self.slotLabel.setText("")
        self.pendingBookFrame.setDisabled(doIt)
        self.table.verticalScrollBar().setProperty("grayOut",doIt)
        repolish(self.table.verticalScrollBar())
    def gimmeTheThing(self):
        """get a copy of the table's data"""
        return self.model.giveUTheThing()
class pendingTableModel(QAbstractTableModel):
    # custom column doesn't exist because yes as well
    ENCHESS_COL, AMOUNT_NUM_COL, AMOUNT_ICON_COL, PUNUSHENT_COL, CUSTOM_COL = [0,1,2,3,4]
    HEADERS = ["內含附魔","數量","數量示意圖","懲罰"]

    def __init__(self):
        super().__init__()
        self._data:list[Book] = []
    def setItems(self,theData,currentIcon:QIcon):
        self._equIcon = currentIcon
        self.beginInsertRows(QModelIndex(),0,len(theData)-1)
        self._data = theData
        self.endInsertRows()
    def clearData(self):
        self.beginResetModel()
        self._data.clear()
        self.endResetModel()

    def data(self, index:QModelIndex, role:Qt.ItemDataRole):
        col, row = index.column(),index.row()
        enchess, punishent, amount, isBook, isCustom = self._data[row].asList()
        if role == Qt.ItemDataRole.DisplayRole:
            if col == self.ENCHESS_COL:
                string = ""; first = True
                for ench,lvl in enchess.items():
                    if first: first = False
                    else: string+='\n'                  
                    string += f"{ench.names[0]} {getRomanNum(lvl)}"
                return string
            if col == self.PUNUSHENT_COL: return punishent
            if col == self.AMOUNT_NUM_COL: return amount
            if col == self.AMOUNT_ICON_COL:
                return amount, None if isBook else self._equIcon
                # return '📓'*amount
            # print(f"WAT ARE YOU TALKING ABOUT IN {row},{col} ?")
            # print(f"IS THIS AMOUNT COL? THE ANSWER IS {col == self.AMOUNT_ICON_COL}")
            # print(f"IT IS {type(col)} TYPE BTW")
        if role == Qt.ItemDataRole.BackgroundRole:
            if isCustom: return QColor("#3B1500")
        if role == Qt.ItemDataRole.ForegroundRole:
            if col == self.PUNUSHENT_COL:
                if punishent!=0: return QColor("#FF0000")
                else: return QColor("#AAAAAA")
        if role == Qt.ItemDataRole.TextAlignmentRole:
            return Qt.AlignmentFlag.AlignCenter
            if col<self.AMOUNT_ICON_COL: return Qt.AlignmentFlag.AlignCenter
            else: return Qt.AlignmentFlag.AlignLeft
        if role == Qt.ItemDataRole.FontRole:
            if col == self.PUNUSHENT_COL and punishent!=0:
                font = QFont();font.setBold(True)
                return font
    def setData(self, index, value, /, role = ...): return False
    def giveUTheThing(self):
        """get a copy of all data"""
        result = [book.copy() for book in self._data]
        return result
    def getSlotLabelText(self):
        if not len(self._data): return ""
        slotNum = sum(d.amount*(2**d.punishent) for d in self._data)
        # for d in self._data: print(f"DA: {d.amount}, DP: {d.punishent}, {d.amount}*(2**{d.punishent})={d.amount*(2**d.punishent)}")
        color = "#FFFFFF"; warning = ""
        if slotNum > 36: color = "#FF0000"; warning = "警告: 使用槽位超過36基本上無解(不管怎麼敲都太貴)"
        elif slotNum > 32: color = "#FFFF00" # ; warning = "警告: 敲完後東西將無法再次升級(以後敲啥都會太貴)"
        return f"<font color='{color}'>附魔槽位使用: {slotNum}{"&nbsp;"*2}{warning}</font>"
    def flags(self, index):
        flags = Qt.ItemFlag.ItemIsEnabled
        return flags
    def rowCount(self, index=0): return len(self._data)
    def columnCount(self, index=0): return 4
    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role != Qt.ItemDataRole.DisplayRole: return
        if orientation == Qt.Vertical: return
        if orientation == Qt.Horizontal:
            return str(self.HEADERS[section])
class AmountDisplayDelegate(QStyledItemDelegate):
    def __init__(self):
        super().__init__()
        self.iconSize = 16
        self.enchBook = QIcon(":/UI/enchantedBook.webp").pixmap(self.iconSize,self.iconSize)
    def paint(self, painter, option, index):
        if index.column() != pendingTableModel.AMOUNT_ICON_COL: return False

        count, icon = index.data(Qt.ItemDataRole.DisplayRole)
        if icon is None: icon = self.enchBook
        else: icon = icon.pixmap(self.iconSize,self.iconSize)
        x = option.rect.x() + 4
        y = option.rect.y() + (option.rect.height() - self.iconSize) // 2

        # This breaks if there's like 32 books,
        # But I won't think about that for now
        for _ in range(count):
            painter.drawPixmap(x,y,self.iconSize,self.iconSize,icon)
            x += self.iconSize
        return True

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