import re
import platform
import os
import winreg
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QApplication, QTextEdit
from PyQt5.QtGui import QIcon

class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()


    def initUI(self):
        self.setGeometry(300, 300, 300, 220)
        self.setWindowTitle('Icon')
        self.setWindowIcon(QIcon('web.png'))
        # Buttons
        find_usb = QPushButton('Find usb ')
        del_usb = QPushButton('Delete USB Log')

        # textarea
        self.output_mon = QTextEdit()


        # Grid layout and position
        grid = QGridLayout()
        grid.addWidget(self.output_mon,0,0)
        grid.addWidget(find_usb, 1,0)
        grid.addWidget(del_usb, 2,0)


        # Connect signal to slot:
        find_usb.clicked.connect(self.check_usb)
        del_usb.clicked.connect(self.del_usb_log)


        self.setLayout(grid)
        self.show()

    def check_usb(self):
        self.output_mon.setText('History of connected usb devices:\n')
        i = 0
        l = 0
        self.enum_list1 = []
        self.enum_list2 = []
        aReg = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
        self.key_usb1 = winreg.OpenKey(aReg, r"SYSTEM\\CurrentControlSet\\Enum\\USBSTOR", 0, winreg.KEY_ALL_ACCESS )
        self.key_usb2 = winreg.OpenKey(aReg, r"SYSTEM\\ControlSet001\\Enum\\USBSTOR", 0, winreg.KEY_ALL_ACCESS )
        try:
            usb_enum1 = winreg.EnumKey(self.key_usb1, i)
            usb_enum2 = winreg.EnumKey(self.key_usb2, l)
            for k in usb_enum1:
                for m in usb_enum2:
                    if re.findall("Disk&Ven_", usb_enum1):
                        self.enum_list1.append(usb_enum1)
                    usb_enum1 = winreg.EnumKey(self.key_usb1, i)
                    if re.findall("Disk&Ven_", usb_enum2):
                        self.enum_list2.append(usb_enum2)
                    usb_enum2 = winreg.EnumKey(self.key_usb2, l)
                    i += 1
                    l += 1
        except Exception as err:
                print(err)
        self.output_mon.append(str(self.enum_list1))
        self.output_mon.append(str(self.enum_list2))

    def del_usb_log(self):
        self.check_usb()
        try:
            for item in self.enum_list1:
                winreg.DeleteKey(self.key_usb1, str(self.enum_list1))
            for item2 in self.enum_list2:
                winreg.DeleteKey(self.key_usb2, str(self.enum_list2))
        except Exception as err:
            self.output_mon.setText("A error was ocured %s" % err)
        self.output_mon.setText("The USB log was deleted:")
        winreg.DeleteKey(self.key_usb1, r"Disk&Ven_Generic&Prod_Flash_Disk&Rev_8.07")
        winreg.CloseKey(self.key_usb1)
        winreg.CloseKey(self.key_usb2)
        winreg.CloseKey()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())