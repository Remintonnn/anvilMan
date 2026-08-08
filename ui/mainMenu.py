# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainMenu.ui'
##
## Created by: Qt User Interface Compiler version 6.11.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QCheckBox, QFrame,
    QHeaderView, QLabel, QMainWindow, QMenu,
    QMenuBar, QPlainTextEdit, QPushButton, QSizePolicy,
    QTableView, QTableWidget, QTableWidgetItem, QWidget)
import hmmm_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(910, 862)
        font = QFont()
        font.setBold(False)
        MainWindow.setFont(font)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setStyleSheet(u"\n"
"\n"
"\n"
"/*====== The Test Zone Above ======*/\n"
"\n"
"\n"
"\n"
"QFrame {\n"
"    background-color: #222222;\n"
"    border-radius:8px;\n"
"    border: 2px solid #b87700;\n"
"}QFrame:disabled {\n"
"    background-color: #151515;\n"
"    border-radius:8px;\n"
"    border: 2px solid #454545;\n"
"}\n"
"\n"
"QWidget {\n"
"    selection-background-color: #878787;\n"
"    selection-color: #ffffff;\n"
"}\n"
"\n"
"QMainWindow {\n"
"    background-color: #111115;\n"
"}\n"
"\n"
"QMenuBar {\n"
"    background-color: rgb(60, 35, 0);\n"
"    color: white;\n"
"}\n"
"\n"
"QTableView {\n"
"    background-color: #202020;\n"
"    alternate-background-color: #3b1500;\n"
"    border-radius: 0px;\n"
"    border: 2px solid #676767;\n"
"    gridline-color: #454545;\n"
"    color: #FFFFFF;\n"
"}QTableView::item:hover {\n"
"    background-color: #333333;\n"
"}QTableView::item:selected:active {\n"
"    background-color: #878787;\n"
"    color: white;\n"
"}QHeaderView{\n"
"	border:none;\n"
"}QHeaderView::section {\n"
"	background"
                        "-color: #333333;\n"
"	color: #FFFFFF;\n"
"	border:none;\n"
"    border-right: 1px solid #676767;\n"
"	font: 10pt \"OCR A Extended\";\n"
"	font-weight: bold;\n"
"}\n"
"\n"
"QTableView:disabled {\n"
"    border: 2px solid #333333;\n"
"	border-radius: 0px;\n"
"}QHeaderView:disabled{\n"
"	border:none;\n"
"}QHeaderView::section:disabled {\n"
"	color: #454545;\n"
"	background-color: #202020;\n"
"	border:none;\n"
"    border-right: 1px solid #333333;\n"
"	font: 10pt \"OCR A Extended\";\n"
"	font-weight: bold;\n"
"}\n"
"\n"
"QScrollBar:vertical {\n"
"    background-color: #222222;\n"
"    width: 19px;\n"
"    margin: 19px 1px 19px 1px;\n"
"}QScrollBar::handle:vertical {\n"
"    background-color: #454545;\n"
"    min-height: 20px;\n"
"    border-radius: 0px;\n"
"}QScrollBar::handle:hover {background-color: #777777;}\n"
"QScrollBar::add-line, QScrollBar::sub-line{/* Arrow Things */\n"
"    background-color: #303030;\n"
"    height: 13px;\n"
"    subcontrol-origin: margin;\n"
"	border: 2px solid #676767;\n"
" 	margin: 1p"
                        "x 1px 1px 1px;\n"
"}QScrollBar::add-line:hover, QScrollBar::sub-line:hover{background-color: #555555;}\n"
"QScrollBar::up-arrow:vertical {image: url(:/UI/upArrow.png);}\n"
"QScrollBar::down-arrow:vertical {image: url(:/UI/downArrow.png);}\n"
"\n"
"QScrollBar[grayOut=true]::handle:vertical {\n"
"    background-color: #252525;\n"
"}QScrollBar[grayOut=true]::add-line:disabled, QScrollBar[grayOut=true]::sub-line{/* Arrow Things */\n"
"	border: 2px solid #333333;\n"
"	background-color: #222222\n"
"}QScrollBar[grayOut=true]::up-arrow:vertical {image: url(:/NOTATHING);}\n"
"QScrollBar[grayOut=true]::down-arrow:vertical {image: url(:/NOTATHING);}\n"
"\n"
"/*====== Smol things ======*/\n"
"\n"
"QLabel {\n"
"	color: #ffffff;\n"
"    border-radius: 8px;\n"
"    border: 2px solid #505050;\n"
"}QLabel:disabled{\n"
"	color: #454545;\n"
"	border: 2px solid #333333;\n"
"}\n"
"\n"
"QPlainTextEdit{\n"
"	border-radius: 0px;\n"
"	border: 2px solid #676767;\n"
"	color: #FFFFFF;\n"
"}\n"
"QPlainTextEdit:disabled{\n"
"	border: 2px s"
                        "olid #181818;\n"
"	color: #676767;\n"
"}\n"
"\n"
"QPushButton {\n"
"    background-color: #222222;\n"
"    color: #FFFFFF;\n"
"    border-radius: 4px;\n"
"	border: 2px solid #505050;\n"
"}QPushButton:hover {\n"
"	background-color: #565656;\n"
"	border: 2px solid #878787;\n"
"}QPushButton:disabled{\n"
"	border: 2px solid #181818;\n"
"	color: #676767;\n"
"}\n"
"\n"
"QPushButton[chosenOne=True]{\n"
"    background-color: #454545;\n"
"    color: #FFFFFF;\n"
"    border-radius: 0px;\n"
"	border: 2px solid #E87700;\n"
"}QPushButton[chosenOne=True]:hover {\n"
"	background-color: #5656FF;\n"
"	border: 2px solid #878787;\n"
"}\n"
"\n"
"QCheckBox{\n"
"    spacing: 6px;\n"
"    font-size: 12px;\n"
"    color: #CCCCCC;\n"
"}QCheckBox:hover{color: #FFFFFF;}QCheckBox::indicator{\n"
"    width: 12px;\n"
"    height: 12px;\n"
"    border: 2px solid #676767;\n"
"    border-radius: 0px;\n"
"}QCheckBox::indicator:checked{\n"
"	image: url(:/UI/checked10x10Center.png)\n"
"}\n"
"\n"
"QCheckBox:disabled{\n"
"    spacing: 6px;\n"
"  "
                        "  font-size: 12px;\n"
"    color: #333333;\n"
"}\n"
"QCheckBox::indicator:disabled{\n"
"    width: 12px;\n"
"    height: 12px;\n"
"    border: 2px solid #333333;\n"
"    border-radius: 0px;\n"
"}QCheckBox::indicator:checked:disabled{\n"
"	image: url(:/UI/checked10x10CenterGrayout.png)\n"
"}\n"
"\n"
"\n"
"QToolTip {\n"
"    background-color: #2b2b2b;\n"
"    color: white;\n"
"    border: 1px solid #676767;\n"
"    border-radius: 6px;\n"
"    padding: 5px;\n"
"    font-size: 12px;\n"
"}")
        MainWindow.setUnifiedTitleAndToolBarOnMac(False)
        self.centralWidget = QWidget(MainWindow)
        self.centralWidget.setObjectName(u"centralWidget")
        self.titleLabel = QLabel(self.centralWidget)
        self.titleLabel.setObjectName(u"titleLabel")
        self.titleLabel.setEnabled(True)
        self.titleLabel.setGeometry(QRect(10, 10, 271, 41))
        self.titleLabel.setStyleSheet(u"QLabel {\n"
"    border: 2px solid #676767;\n"
"}\n"
"QLabel:disabled{\n"
"	border: 2px solid #2f2f2f;\n"
"	color: #676767;\n"
"}")
        self.newEquFrame = QFrame(self.centralWidget)
        self.newEquFrame.setObjectName(u"newEquFrame")
        self.newEquFrame.setEnabled(True)
        self.newEquFrame.setGeometry(QRect(290, 10, 311, 401))
        self.newEquFrame.setStyleSheet(u"QPushButton {\n"
"    background-color: #383838;\n"
"    color: #FFFFFF;\n"
"    border-radius: 8px;\n"
"	border: 0px solid #505050;\n"
"}QPushButton:hover {\n"
"	background-color: #767676\n"
"}\n"
"\n"
"QPushButton[chosenOne=true]{\n"
"    background-color: #51514D;\n"
"    color: #FFFFFF;\n"
"	border: 2px solid #D87700;\n"
"}QPushButton[chosenOne=true]:hover {\n"
"	background-color: #AAAAAA;\n"
"	border: 2px solid #FFAA00;\n"
"}")
        self.newEquFrame.setFrameShape(QFrame.StyledPanel)
        self.newEquFrame.setFrameShadow(QFrame.Raised)
        self.armorAndWingLabel = QLabel(self.newEquFrame)
        self.armorAndWingLabel.setObjectName(u"armorAndWingLabel")
        self.armorAndWingLabel.setGeometry(QRect(10, 40, 111, 31))
        self.newEquTitleLabel = QLabel(self.newEquFrame)
        self.newEquTitleLabel.setObjectName(u"newEquTitleLabel")
        self.newEquTitleLabel.setGeometry(QRect(10, 10, 111, 23))
        self.meleeLabel = QLabel(self.newEquFrame)
        self.meleeLabel.setObjectName(u"meleeLabel")
        self.meleeLabel.setGeometry(QRect(10, 130, 95, 31))
        self.rangeLabel = QLabel(self.newEquFrame)
        self.rangeLabel.setObjectName(u"rangeLabel")
        self.rangeLabel.setGeometry(QRect(10, 220, 95, 31))
        self.miningToolLabel = QLabel(self.newEquFrame)
        self.miningToolLabel.setObjectName(u"miningToolLabel")
        self.miningToolLabel.setGeometry(QRect(10, 310, 136, 31))
        self.hatB = QPushButton(self.newEquFrame)
        self.hatB.setObjectName(u"hatB")
        self.hatB.setGeometry(QRect(10, 80, 41, 41))
        self.hatB.setFocusPolicy(Qt.NoFocus)
        self.hatB.setToolTipDuration(-1)
        icon = QIcon()
        icon.addFile(u":/armors/helmet.webp", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.hatB.setIcon(icon)
        self.hatB.setIconSize(QSize(32, 32))
        self.hatB.setProperty(u"chosenOne", False)
        self.clothB = QPushButton(self.newEquFrame)
        self.clothB.setObjectName(u"clothB")
        self.clothB.setGeometry(QRect(60, 80, 41, 41))
        self.clothB.setFocusPolicy(Qt.NoFocus)
        icon1 = QIcon()
        icon1.addFile(u":/armors/chestplate.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.clothB.setIcon(icon1)
        self.clothB.setIconSize(QSize(32, 32))
        self.clothB.setProperty(u"chosenOne", False)
        self.pantsB = QPushButton(self.newEquFrame)
        self.pantsB.setObjectName(u"pantsB")
        self.pantsB.setGeometry(QRect(110, 80, 41, 41))
        self.pantsB.setFocusPolicy(Qt.NoFocus)
        icon2 = QIcon()
        icon2.addFile(u":/armors/leggings.webp", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pantsB.setIcon(icon2)
        self.pantsB.setIconSize(QSize(32, 32))
        self.pantsB.setProperty(u"chosenOne", False)
        self.shoesB = QPushButton(self.newEquFrame)
        self.shoesB.setObjectName(u"shoesB")
        self.shoesB.setGeometry(QRect(160, 80, 41, 41))
        self.shoesB.setFocusPolicy(Qt.NoFocus)
        icon3 = QIcon()
        icon3.addFile(u":/armors/boots.webp", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.shoesB.setIcon(icon3)
        self.shoesB.setIconSize(QSize(32, 32))
        self.shoesB.setProperty(u"chosenOne", False)
        self.wingB = QPushButton(self.newEquFrame)
        self.wingB.setObjectName(u"wingB")
        self.wingB.setGeometry(QRect(210, 80, 41, 41))
        self.wingB.setFocusPolicy(Qt.NoFocus)
        icon4 = QIcon()
        icon4.addFile(u":/armors/elytra.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.wingB.setIcon(icon4)
        self.wingB.setIconSize(QSize(32, 32))
        self.wingB.setProperty(u"chosenOne", False)
        self.maceB = QPushButton(self.newEquFrame)
        self.maceB.setObjectName(u"maceB")
        self.maceB.setGeometry(QRect(160, 170, 41, 41))
        self.maceB.setFocusPolicy(Qt.NoFocus)
        icon5 = QIcon()
        icon5.addFile(u":/melee/mace.webp", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.maceB.setIcon(icon5)
        self.maceB.setIconSize(QSize(32, 32))
        self.maceB.setProperty(u"chosenOne", False)
        self.tridentB = QPushButton(self.newEquFrame)
        self.tridentB.setObjectName(u"tridentB")
        self.tridentB.setGeometry(QRect(210, 170, 41, 41))
        self.tridentB.setFocusPolicy(Qt.NoFocus)
        icon6 = QIcon()
        icon6.addFile(u":/melee/trident.webp", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.tridentB.setIcon(icon6)
        self.tridentB.setIconSize(QSize(32, 32))
        self.tridentB.setProperty(u"chosenOne", False)
        self.swordB = QPushButton(self.newEquFrame)
        self.swordB.setObjectName(u"swordB")
        self.swordB.setGeometry(QRect(10, 170, 41, 41))
        self.swordB.setFocusPolicy(Qt.NoFocus)
        icon7 = QIcon()
        icon7.addFile(u":/melee/sword.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.swordB.setIcon(icon7)
        self.swordB.setIconSize(QSize(32, 32))
        self.swordB.setProperty(u"chosenOne", False)
        self.shieldB = QPushButton(self.newEquFrame)
        self.shieldB.setObjectName(u"shieldB")
        self.shieldB.setGeometry(QRect(260, 170, 41, 41))
        self.shieldB.setFocusPolicy(Qt.NoFocus)
        icon8 = QIcon()
        icon8.addFile(u":/melee/shield.webp", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.shieldB.setIcon(icon8)
        self.shieldB.setIconSize(QSize(32, 32))
        self.shieldB.setProperty(u"chosenOne", False)
        self.spearB = QPushButton(self.newEquFrame)
        self.spearB.setObjectName(u"spearB")
        self.spearB.setGeometry(QRect(110, 170, 41, 41))
        self.spearB.setFocusPolicy(Qt.NoFocus)
        self.spearB.setStyleSheet(u"")
        icon9 = QIcon()
        icon9.addFile(u":/melee/spear.webp", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.spearB.setIcon(icon9)
        self.spearB.setIconSize(QSize(32, 32))
        self.spearB.setProperty(u"chosenOne", False)
        self.axeB1 = QPushButton(self.newEquFrame)
        self.axeB1.setObjectName(u"axeB1")
        self.axeB1.setGeometry(QRect(60, 170, 41, 41))
        self.axeB1.setFocusPolicy(Qt.NoFocus)
        icon10 = QIcon()
        icon10.addFile(u":/melee/axe.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.axeB1.setIcon(icon10)
        self.axeB1.setIconSize(QSize(32, 32))
        self.axeB1.setProperty(u"chosenOne", False)
        self.crossbowB = QPushButton(self.newEquFrame)
        self.crossbowB.setObjectName(u"crossbowB")
        self.crossbowB.setGeometry(QRect(10, 260, 41, 41))
        self.crossbowB.setFocusPolicy(Qt.NoFocus)
        icon11 = QIcon()
        icon11.addFile(u":/range/crossbow.webp", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.crossbowB.setIcon(icon11)
        self.crossbowB.setIconSize(QSize(32, 32))
        self.crossbowB.setProperty(u"chosenOne", False)
        self.bowB = QPushButton(self.newEquFrame)
        self.bowB.setObjectName(u"bowB")
        self.bowB.setGeometry(QRect(60, 260, 41, 41))
        self.bowB.setFocusPolicy(Qt.NoFocus)
        icon12 = QIcon()
        icon12.addFile(u":/range/bow.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.bowB.setIcon(icon12)
        self.bowB.setIconSize(QSize(32, 32))
        self.bowB.setProperty(u"chosenOne", False)
        self.hoeB = QPushButton(self.newEquFrame)
        self.hoeB.setObjectName(u"hoeB")
        self.hoeB.setGeometry(QRect(160, 350, 41, 41))
        self.hoeB.setFocusPolicy(Qt.NoFocus)
        icon13 = QIcon()
        icon13.addFile(u":/tools/hoe.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.hoeB.setIcon(icon13)
        self.hoeB.setIconSize(QSize(32, 32))
        self.hoeB.setProperty(u"chosenOne", False)
        self.shearsB = QPushButton(self.newEquFrame)
        self.shearsB.setObjectName(u"shearsB")
        self.shearsB.setGeometry(QRect(210, 350, 41, 41))
        self.shearsB.setFocusPolicy(Qt.NoFocus)
        icon14 = QIcon()
        icon14.addFile(u":/tools/shear.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.shearsB.setIcon(icon14)
        self.shearsB.setIconSize(QSize(32, 32))
        self.shearsB.setProperty(u"chosenOne", False)
        self.pickaxeB = QPushButton(self.newEquFrame)
        self.pickaxeB.setObjectName(u"pickaxeB")
        self.pickaxeB.setGeometry(QRect(10, 350, 41, 41))
        self.pickaxeB.setFocusPolicy(Qt.NoFocus)
        icon15 = QIcon()
        icon15.addFile(u":/tools/pickaxe.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pickaxeB.setIcon(icon15)
        self.pickaxeB.setIconSize(QSize(32, 32))
        self.pickaxeB.setProperty(u"chosenOne", False)
        self.flientSteelB = QPushButton(self.newEquFrame)
        self.flientSteelB.setObjectName(u"flientSteelB")
        self.flientSteelB.setGeometry(QRect(260, 350, 41, 41))
        self.flientSteelB.setFocusPolicy(Qt.NoFocus)
        icon16 = QIcon()
        icon16.addFile(u":/tools/F&C.webp", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.flientSteelB.setIcon(icon16)
        self.flientSteelB.setIconSize(QSize(32, 32))
        self.flientSteelB.setProperty(u"chosenOne", False)
        self.shovelB = QPushButton(self.newEquFrame)
        self.shovelB.setObjectName(u"shovelB")
        self.shovelB.setGeometry(QRect(110, 350, 41, 41))
        self.shovelB.setFocusPolicy(Qt.NoFocus)
        icon17 = QIcon()
        icon17.addFile(u":/tools/shovel.webp", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.shovelB.setIcon(icon17)
        self.shovelB.setIconSize(QSize(32, 32))
        self.shovelB.setProperty(u"chosenOne", False)
        self.axeB2 = QPushButton(self.newEquFrame)
        self.axeB2.setObjectName(u"axeB2")
        self.axeB2.setGeometry(QRect(60, 350, 41, 41))
        self.axeB2.setFocusPolicy(Qt.NoFocus)
        icon18 = QIcon()
        icon18.addFile(u":/tools/axe.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.axeB2.setIcon(icon18)
        self.axeB2.setIconSize(QSize(32, 32))
        self.axeB2.setProperty(u"chosenOne", False)
        self.saveFrame = QFrame(self.centralWidget)
        self.saveFrame.setObjectName(u"saveFrame")
        self.saveFrame.setGeometry(QRect(10, 60, 271, 351))
        self.saveFrame.setStyleSheet(u"")
        self.saveFrame.setFrameShape(QFrame.StyledPanel)
        self.saveFrame.setFrameShadow(QFrame.Raised)
        self.savedItemButton = QPushButton(self.saveFrame)
        self.savedItemButton.setObjectName(u"savedItemButton")
        self.savedItemButton.setGeometry(QRect(10, 3, 71, 20))
        font1 = QFont()
        font1.setPointSize(8)
        self.savedItemButton.setFont(font1)
        self.savedItemButton.setFocusPolicy(Qt.NoFocus)
        self.savedItemButton.setStyleSheet(u"QPushButton{\n"
"	background-color: #131313;\n"
"	border-radius:0px;\n"
"	border: 2px solid #505050;\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: #676767;\n"
"	border: 2px solid #878787;\n"
"}")
        self.savedInstructionButton = QPushButton(self.saveFrame)
        self.savedInstructionButton.setObjectName(u"savedInstructionButton")
        self.savedInstructionButton.setGeometry(QRect(80, 3, 91, 20))
        self.savedInstructionButton.setFont(font1)
        self.savedInstructionButton.setFocusPolicy(Qt.NoFocus)
        self.savedInstructionButton.setStyleSheet(u"QPushButton{\n"
"	background-color: #131313;\n"
"	border-radius:0px;\n"
"	border: 2px solid #505050;\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: #676767;\n"
"	border: 2px solid #878787;\n"
"}")
        self.saveDeleteButton = QPushButton(self.saveFrame)
        self.saveDeleteButton.setObjectName(u"saveDeleteButton")
        self.saveDeleteButton.setGeometry(QRect(12, 314, 71, 31))
        font2 = QFont()
        font2.setPointSize(12)
        self.saveDeleteButton.setFont(font2)
        self.saveDeleteButton.setFocusPolicy(Qt.NoFocus)
        self.saveTable = QTableWidget(self.saveFrame)
        if (self.saveTable.columnCount() < 3):
            self.saveTable.setColumnCount(3)
        __qtablewidgetitem = QTableWidgetItem()
        self.saveTable.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.saveTable.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.saveTable.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        self.saveTable.setObjectName(u"saveTable")
        self.saveTable.setGeometry(QRect(10, 20, 251, 288))
        self.saveTable.setStyleSheet(u"")
        self.saveTable.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.saveTable.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.saveTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.saveTable.setProperty(u"showDropIndicator", False)
        self.saveTable.setDragEnabled(True)
        self.saveTable.setDragDropOverwriteMode(False)
        self.saveTable.setAlternatingRowColors(True)
        self.saveTable.setSelectionMode(QAbstractItemView.SingleSelection)
        self.saveTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.saveTable.setRowCount(0)
        self.saveTable.horizontalHeader().setVisible(True)
        self.saveTable.horizontalHeader().setCascadingSectionResizes(False)
        self.saveTable.horizontalHeader().setDefaultSectionSize(76)
        self.saveTable.verticalHeader().setVisible(False)
        self.saveLoadButton = QPushButton(self.saveFrame)
        self.saveLoadButton.setObjectName(u"saveLoadButton")
        self.saveLoadButton.setGeometry(QRect(88, 314, 171, 31))
        self.saveLoadButton.setFont(font2)
        self.saveLoadButton.setFocusPolicy(Qt.NoFocus)
        self.enchSelFrame = QFrame(self.centralWidget)
        self.enchSelFrame.setObjectName(u"enchSelFrame")
        self.enchSelFrame.setEnabled(True)
        self.enchSelFrame.setGeometry(QRect(610, 10, 291, 821))
        self.enchSelFrame.setStyleSheet(u"")
        self.enchSelFrame.setFrameShape(QFrame.StyledPanel)
        self.enchSelFrame.setFrameShadow(QFrame.Raised)
        self.enchSelTitleLabel = QLabel(self.enchSelFrame)
        self.enchSelTitleLabel.setObjectName(u"enchSelTitleLabel")
        self.enchSelTitleLabel.setEnabled(True)
        self.enchSelTitleLabel.setGeometry(QRect(10, 10, 111, 23))
        self.enchTable = QTableView(self.enchSelFrame)
        self.enchTable.setObjectName(u"enchTable")
        self.enchTable.setGeometry(QRect(10, 38, 271, 736))
        font3 = QFont()
        font3.setFamilies([u"Noto Serif"])
        font3.setPointSize(12)
        font3.setBold(False)
        font3.setItalic(False)
        self.enchTable.setFont(font3)
        self.enchTable.setFocusPolicy(Qt.NoFocus)
        self.enchTable.setStyleSheet(u"QTableView{\n"
"	font: 12pt \"Noto Serif\";\n"
"}QTableView::item{\n"
"	padding: 2px 0px 1px 0px;\n"
"}")
        self.enchTable.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.enchTable.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.enchTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.enchTable.setProperty(u"showDropIndicator", False)
        self.enchTable.setDragEnabled(False)
        self.enchTable.setDragDropOverwriteMode(False)
        self.enchTable.setAlternatingRowColors(False)
        self.enchTable.setSelectionMode(QAbstractItemView.NoSelection)
        self.enchTable.setGridStyle(Qt.SolidLine)
        self.enchTable.verticalHeader().setVisible(False)
        self.theOneTheOriTHEONETHEORITOTOtotoTOTALtoto = QPushButton(self.enchSelFrame)
        self.theOneTheOriTHEONETHEORITOTOtotoTOTALtoto.setObjectName(u"theOneTheOriTHEONETHEORITOTOtotoTOTALtoto")
        self.theOneTheOriTHEONETHEORITOTOtotoTOTALtoto.setGeometry(QRect(120, 780, 161, 31))
        self.theOneTheOriTHEONETHEORITOTOtotoTOTALtoto.setFont(font2)
        self.theOneTheOriTHEONETHEORITOTOtotoTOTALtoto.setFocusPolicy(Qt.NoFocus)
        self.theOneTheOriTHEONETHEORITOTOtotoTOTALtoto.setStyleSheet(u"QPushButton{\n"
"	background-color: #131313;\n"
"	border-radius:4px;\n"
"	border: 2px solid #b87700;\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: #565656;\n"
"	border: 2px solid #c89723;\n"
"}\n"
"QPushButton:disabled{\n"
"	border: 2px solid #2f2f2f;\n"
"	color: #333333;\n"
"}")
        self.enchSelHighlightCheckBox = QCheckBox(self.enchSelFrame)
        self.enchSelHighlightCheckBox.setObjectName(u"enchSelHighlightCheckBox")
        self.enchSelHighlightCheckBox.setEnabled(True)
        self.enchSelHighlightCheckBox.setGeometry(QRect(12, 786, 101, 21))
        font4 = QFont()
        self.enchSelHighlightCheckBox.setFont(font4)
        self.enchSelHighlightCheckBox.setFocusPolicy(Qt.NoFocus)
        self.enchSelHighlightCheckBox.setStyleSheet(u"")
        self.enchSelHighlightCheckBox.setChecked(True)
        self.pendingBookFram = QFrame(self.centralWidget)
        self.pendingBookFram.setObjectName(u"pendingBookFram")
        self.pendingBookFram.setEnabled(True)
        self.pendingBookFram.setGeometry(QRect(10, 420, 591, 411))
        self.pendingBookFram.setStyleSheet(u"")
        self.pendingBookFram.setFrameShape(QFrame.StyledPanel)
        self.pendingBookFram.setFrameShadow(QFrame.Raised)
        self.pendingBookTitleLabel = QLabel(self.pendingBookFram)
        self.pendingBookTitleLabel.setObjectName(u"pendingBookTitleLabel")
        self.pendingBookTitleLabel.setGeometry(QRect(10, 10, 111, 23))
        self.pendingBookTable = QTableView(self.pendingBookFram)
        self.pendingBookTable.setObjectName(u"pendingBookTable")
        self.pendingBookTable.setGeometry(QRect(10, 38, 571, 326))
        self.pendingBookTable.setStyleSheet(u"")
        self.pendingBookTable.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.pendingBookTable.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.pendingBookTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.pendingBookTable.setProperty(u"showDropIndicator", False)
        self.pendingBookTable.setDragEnabled(False)
        self.pendingBookTable.setDragDropOverwriteMode(False)
        self.pendingBookTable.setAlternatingRowColors(True)
        self.pendingBookTable.setSelectionMode(QAbstractItemView.NoSelection)
        self.pendingBookTable.horizontalHeader().setMinimumSectionSize(0)
        self.pendingBookTable.horizontalHeader().setDefaultSectionSize(183)
        self.pendingBookTable.horizontalHeader().setHighlightSections(False)
        self.pendingBookTable.verticalHeader().setVisible(False)
        self.pendingBookTable.verticalHeader().setDefaultSectionSize(0)
        self.pendingBookCustomItemButton = QPushButton(self.pendingBookFram)
        self.pendingBookCustomItemButton.setObjectName(u"pendingBookCustomItemButton")
        self.pendingBookCustomItemButton.setGeometry(QRect(430, 370, 151, 31))
        self.pendingBookCustomItemButton.setFont(font2)
        self.pendingBookCustomItemButton.setFocusPolicy(Qt.NoFocus)
        self.pendingBookCustomItemButton.setStyleSheet(u"QPushButton{\n"
"	background-color: #131313;\n"
"	border-radius:4px;\n"
"	border: 2px solid #b87700;\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: #565656;\n"
"	border: 2px solid #c89723;\n"
"}\n"
"QPushButton:disabled{\n"
"	border: 2px solid #2f2f2f;\n"
"	color: #333333;\n"
"}")
        self.saveButton = QPushButton(self.pendingBookFram)
        self.saveButton.setObjectName(u"saveButton")
        self.saveButton.setGeometry(QRect(320, 370, 101, 31))
        self.saveButton.setFont(font2)
        self.saveButton.setFocusPolicy(Qt.NoFocus)
        self.saveButton.setStyleSheet(u"")
        self.saveNameInputBox = QPlainTextEdit(self.pendingBookFram)
        self.saveNameInputBox.setObjectName(u"saveNameInputBox")
        self.saveNameInputBox.setGeometry(QRect(10, 370, 301, 31))
        font5 = QFont()
        font5.setFamilies([u"Segoe UI"])
        font5.setPointSize(12)
        self.saveNameInputBox.setFont(font5)
        self.saveNameInputBox.setStyleSheet(u"")
        self.saveNameInputBox.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.saveNameInputBox.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.saveNameInputBox.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.pendingBookSlotDisplayLabel = QLabel(self.pendingBookFram)
        self.pendingBookSlotDisplayLabel.setObjectName(u"pendingBookSlotDisplayLabel")
        self.pendingBookSlotDisplayLabel.setGeometry(QRect(130, 11, 451, 21))
        font6 = QFont()
        font6.setPointSize(9)
        self.pendingBookSlotDisplayLabel.setFont(font6)
        self.pendingBookSlotDisplayLabel.setStyleSheet(u"QLabel{\n"
"	color: #FF0000;\n"
"	border-radius:0px;\n"
"	border: 0px solid #b87700;\n"
"}Label")
        MainWindow.setCentralWidget(self.centralWidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 910, 21))
        self.manual = QMenu(self.menubar)
        self.manual.setObjectName(u"manual")
        self.menu = QMenu(self.menubar)
        self.menu.setObjectName(u"menu")
        MainWindow.setMenuBar(self.menubar)

        self.menubar.addAction(self.manual.menuAction())
        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"\u9644\u9b54\u8a08\u7b97\u73a9\u610f(Free)", None))
        self.titleLabel.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p align=\"center\"><span style=\" font-size:20pt;\">\u9435\u7827\u6572\u88dd\u8a08\u7b97\u6a5f</span></p></body></html>", None))
        self.armorAndWingLabel.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:16pt;\">\u88dd\u7532&amp;\u7fc5\u8180</span></p></body></html>", None))
        self.newEquTitleLabel.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:12pt;\">\u9078\u64c7\u76ee\u6a19\u88dd\u5099</span></p></body></html>", None))
        self.meleeLabel.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:16pt;\">\u8fd1\u6230\u5de5\u5177</span></p></body></html>", None))
        self.rangeLabel.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:16pt;\">\u9060\u6230\u5de5\u5177</span></p></body></html>", None))
        self.miningToolLabel.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:16pt;\">\u74b0\u5883\u7834\u58de\u5de5\u5177</span></p></body></html>", None))
#if QT_CONFIG(tooltip)
        self.hatB.setToolTip(QCoreApplication.translate("MainWindow", u"\u5e3d\u5b50\u7d66\u6211\u597d\u55ce?", None))
#endif // QT_CONFIG(tooltip)
        self.hatB.setText("")
#if QT_CONFIG(tooltip)
        self.clothB.setToolTip(QCoreApplication.translate("MainWindow", u"\u7532(\u7532)", None))
#endif // QT_CONFIG(tooltip)
        self.clothB.setText("")
#if QT_CONFIG(tooltip)
        self.pantsB.setToolTip(QCoreApplication.translate("MainWindow", u"\u592a\u8932\u4e86!", None))
#endif // QT_CONFIG(tooltip)
        self.pantsB.setText("")
#if QT_CONFIG(tooltip)
        self.shoesB.setToolTip(QCoreApplication.translate("MainWindow", u"\u9019\u5565\u978b\u9580\u73a9\u610f", None))
#endif // QT_CONFIG(tooltip)
        self.shoesB.setText("")
#if QT_CONFIG(tooltip)
        self.wingB.setToolTip(QCoreApplication.translate("MainWindow", u"\u770b\u8d77\u4f86\u50cf\u87d1\u8782\u7fc5\u8180...", None))
#endif // QT_CONFIG(tooltip)
        self.wingB.setText("")
#if QT_CONFIG(tooltip)
        self.maceB.setToolTip(QCoreApplication.translate("MainWindow", u"\u6e6f\u683c\u65af\u7279\u584a\u5728\u68cd\u5b50\u4e0a!", None))
#endif // QT_CONFIG(tooltip)
        self.maceB.setText("")
#if QT_CONFIG(tooltip)
        self.tridentB.setToolTip(QCoreApplication.translate("MainWindow", u"\u9019\u9ebc\u5927\u7684\u53c9\u5b50\u662f\u8981\u7528\u4f86\u5403\u4ec0\u9ebc...", None))
#endif // QT_CONFIG(tooltip)
        self.tridentB.setText("")
#if QT_CONFIG(tooltip)
        self.swordB.setToolTip(QCoreApplication.translate("MainWindow", u"\u8fd1\u6230\u7528\u7684\u3107 \u597d\u50cf\u662f", None))
#endif // QT_CONFIG(tooltip)
        self.swordB.setText("")
#if QT_CONFIG(tooltip)
        self.shieldB.setToolTip(QCoreApplication.translate("MainWindow", u"\u4e0d\u652f\u63f4\u76fe\u64ca, \u5dee\u8a55", None))
#endif // QT_CONFIG(tooltip)
        self.shieldB.setText("")
#if QT_CONFIG(tooltip)
        self.spearB.setToolTip(QCoreApplication.translate("MainWindow", u"\u62ff\u68cd\u5b50\u6233\u4eba\u53ef\u80fd\u4e0d\u662f\u592a\u65b0\u76c8\u7684\u4e3b\u610f...", None))
#endif // QT_CONFIG(tooltip)
        self.spearB.setText("")
#if QT_CONFIG(tooltip)
        self.axeB1.setToolTip(QCoreApplication.translate("MainWindow", u"\u4fd7\u8a71\u8aaa: \u4eba\u5c31\u548c\u6a39\u4e00\u6a23", None))
#endif // QT_CONFIG(tooltip)
        self.axeB1.setText("")
#if QT_CONFIG(tooltip)
        self.crossbowB.setToolTip(QCoreApplication.translate("MainWindow", u"\u5341\u5b57\u5f13 >>>> \u5f13(No bias)", None))
#endif // QT_CONFIG(tooltip)
        self.crossbowB.setText("")
#if QT_CONFIG(tooltip)
        self.bowB.setToolTip(QCoreApplication.translate("MainWindow", u"\u5f13 <<<< \u5341\u5b57\u5f13(No bias, really)", None))
#endif // QT_CONFIG(tooltip)
        self.bowB.setText("")
#if QT_CONFIG(tooltip)
        self.hoeB.setToolTip(QCoreApplication.translate("MainWindow", u"Your mom", None))
#endif // QT_CONFIG(tooltip)
        self.hoeB.setText("")
#if QT_CONFIG(tooltip)
        self.shearsB.setToolTip(QCoreApplication.translate("MainWindow", u"(\u8a0a\u606f\u5167\u5bb9\u7d93\u5f8b\u5e2b\u5efa\u8b70\u5df2\u6d88\u9664)", None))
#endif // QT_CONFIG(tooltip)
        self.shearsB.setText("")
#if QT_CONFIG(tooltip)
        self.pickaxeB.setToolTip(QCoreApplication.translate("MainWindow", u"\u96d9\u982d\u92e4\u982d", None))
#endif // QT_CONFIG(tooltip)
        self.pickaxeB.setText("")
#if QT_CONFIG(tooltip)
        self.flientSteelB.setToolTip(QCoreApplication.translate("MainWindow", u"\u5176\u5be6\u9019\u500b\u4e5f\u4ee3\u8868\u4e86\u5237\u5b50\u4e4b\u985e\u7684(\u96dc\u9805\u985e\u5de5\u5177)", None))
#endif // QT_CONFIG(tooltip)
        self.flientSteelB.setText("")
#if QT_CONFIG(tooltip)
        self.shovelB.setToolTip(QCoreApplication.translate("MainWindow", u"\u5927\u6e6f\u5319\u61c9\u8a72\u914d\u6a13\u4e0a\u7684\u5927\u53c9\u5b50", None))
#endif // QT_CONFIG(tooltip)
        self.shovelB.setText("")
#if QT_CONFIG(tooltip)
        self.axeB2.setToolTip(QCoreApplication.translate("MainWindow", u"\u524d\u4eba\u7a2e\u6a39...", None))
#endif // QT_CONFIG(tooltip)
        self.axeB2.setText("")
        self.savedItemButton.setText(QCoreApplication.translate("MainWindow", u"\u5df2\u5132\u5b58\u7269\u54c1", None))
        self.savedInstructionButton.setText(QCoreApplication.translate("MainWindow", u"\u5df2\u5132\u5b58\u5408\u6210\u6b65\u9a5f", None))
        self.saveDeleteButton.setStyleSheet("")
        self.saveDeleteButton.setText(QCoreApplication.translate("MainWindow", u"\u522a\u9664", None))
        ___qtablewidgetitem = self.saveTable.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"\u7269\u54c1", None))
        ___qtablewidgetitem1 = self.saveTable.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"\u65e5\u671f", None))
        ___qtablewidgetitem2 = self.saveTable.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"\u540d\u5b57", None))
        self.saveLoadButton.setStyleSheet("")
        self.saveLoadButton.setText(QCoreApplication.translate("MainWindow", u"\u8f09\u5165", None))
        self.enchSelTitleLabel.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:12pt;\">\u9078\u64c7\u76ee\u6a19\u9644\u9b54</span></p></body></html>", None))
        self.theOneTheOriTHEONETHEORITOTOtotoTOTALtoto.setText(QCoreApplication.translate("MainWindow", u"\u8a08\u7b97\u9435\u7827\u7d44\u5408\u65b9\u5f0f", None))
        self.enchSelHighlightCheckBox.setText(QCoreApplication.translate("MainWindow", u"\u51f8\u986f\u5df2\u9078\u9644\u9b54", None))
        self.pendingBookTitleLabel.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:12pt;\">\u5408\u6210\u5167\u5bb9\u9810\u89bd</span></p></body></html>", None))
        self.pendingBookCustomItemButton.setText(QCoreApplication.translate("MainWindow", u"\u81ea\u5b9a\u7fa9\u5408\u6210\u5167\u5bb9", None))
        self.saveButton.setText(QCoreApplication.translate("MainWindow", u"\u5132\u5b58\u88dd\u5099", None))
        self.saveNameInputBox.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\u8f38\u5165\u7269\u54c1\u540d\u5b57...", None))
        self.pendingBookSlotDisplayLabel.setText(QCoreApplication.translate("MainWindow", u"\u9644\u9b54\u69fd\u4f4d\u4f7f\u7528: 37  (\u8b66\u544a: \u69fd\u4f4d\u4f7f\u7528\u8d85\u904e36\u57fa\u672c\u4e0a\u7121\u89e3)", None))
        self.manual.setTitle(QCoreApplication.translate("MainWindow", u"\u4f7f\u7528\u8aaa\u660e(Please notice meeeeee)", None))
        self.menu.setTitle(QCoreApplication.translate("MainWindow", u"\u95dc\u65bc", None))
    # retranslateUi

