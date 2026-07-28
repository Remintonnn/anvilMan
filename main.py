from calc.enchantments import Enchantment as Ench
from calc.enchantments import enchantments as enchs # not cap cuz it's an instance
from calc.enchantments import EnchantmentId as EnchId
from calc.enchantments import EnchantmentTags as EnchTag
import ui.mainWindow as mainWindow
import sys
from PySide6.QtCore import Qt
from PySide6.QtWidgets import * # QApplication, QStyleFactory, QHeaderView, QTableWidgetItem
from PySide6.QtUiTools import * # QUiLoader
from PySide6.QtGui import * # QIcon

def main():
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create("Fusion"))
    # window = QUiLoader().load("ui/mainMenu.ui")
    window = mainWindow.MainWindow()
    window.show()
    sys.exit(app.exec())
    


main()

# TODO: enchTable data obj
# TODO: ebchTable data update
# TODO: equ select enchTable population
# TODO: ench conflict logic
# TODO: enchTable lvl scroll edit
# TODO:
# TODO:
# TODO:
# TODO: imp pendingTable.addItem()