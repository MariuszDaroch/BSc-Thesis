# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'EditInterface.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
import ipaddress
from netaddr import IPAddress

from Error import Ui_Error


def netmask_to_cidr(netmask):
    return sum([bin(int(x)).count('1') for x in netmask.split('.')])


class Ui_EditInterfaces():
    ui_interfaces = None
    router = None
    interface = None
    data = None
    interface_number = None
    ip_address = None
    subnet_mask = None
    enable = None
    PreviousWindow = None

    def reload(self):
        try:
            for i in self.data:
                if i[0] == self.interface:
                    _translate = QtCore.QCoreApplication.translate
                    self.ip_address = i[1]
                    self.subnet_mask = i[2]
                    self.enable = i[3]
                    self.IpEdit.setText(_translate("MainWindow", self.ip_address))
                    self.MaskEdit.setText(_translate("MainWindow", self.subnet_mask))
                    self.checkbox.setChecked(self.enable)

            if self.IpEdit.text() != self.ip_address:
                _translate = QtCore.QCoreApplication.translate
                self.IpEdit.setText(_translate("MainWindow", "No data"))
                self.MaskEdit.setText(_translate("MainWindow", "No data"))
                self.checkbox.setChecked(False)
        except Exception as e:
            self.openErrorWindow(e)

    def commit(self):
        try:

            if self.IpEdit.text() == "":
                self.router.load_merge_candidate(
                    config="default interface gigabitEthernet" + self.interface + "\n interface gigabitEthernet" + self.interface + "\n shutdown\nend\n")
                self.router.commit_config()
            else:
                if self.valid():
                    if self.ip_address == self.IpEdit.text() and self.subnet_mask == self.MaskEdit.text() and self.enable == self.checkbox.checkState():
                        self.exit()
                    else:
                        if self.checkbox.checkState():
                            self.router.load_merge_candidate(
                                config="interface GigabitEthernet" + self.interface + "\n ip address " + self.IpEdit.text() + " " + self.MaskEdit.text() + "\n no shutdown\n end\n")
                            self.router.commit_config()
                        else:
                            self.router.load_merge_candidate(
                                config="interface GigabitEthernet" + self.interface + "\n ip address " + self.IpEdit.text() + " " + self.MaskEdit.text() + "\n shutdown\n end\n")
                            self.router.commit_config()
                        self.exit()
                else:
                    self.openErrorWindow("Wrong data")
        except Exception as e:
            self.openErrorWindow(e)

    def exit(self):
        self.PreviousWindow.show()
        self.centralwidget.window().close()

    def valid(self):
        try:
            IPAddress(self.MaskEdit.text()).netmask_bits()
            ipaddress.ip_address(self.IpEdit.text())
            return True
        except Exception as e:
            self.openErrorWindow(e)
            return False

    def openErrorWindow(self, txt):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_Error()
        self.ui.setupUi(self.window, self.MainWindow)
        self.ui.reload(txt)
        self.window.show()

    def setupUi(self, MainWindow, PreviousWindow):
        self.PreviousWindow = PreviousWindow
        self.PreviousWindow.hide()
        self.MainWindow = MainWindow

        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(389, 218)
        MainWindow.setMinimumSize(QtCore.QSize(389, 218))
        MainWindow.setMaximumSize(QtCore.QSize(389, 218))

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.intMASK = QtWidgets.QLabel(self.centralwidget)
        self.intMASK.setGeometry(QtCore.QRect(60, 70, 121, 23))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding,
                                           QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.intMASK.sizePolicy().hasHeightForWidth())
        self.intMASK.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.intMASK.setFont(font)
        self.intMASK.setObjectName("intMASK")

        self.CommitIntEdit = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: self.commit())
        self.CommitIntEdit.setGeometry(QtCore.QRect(220, 150, 75, 23))
        self.CommitIntEdit.setObjectName("CommitIntEdit")

        self.MaskEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.MaskEdit.setGeometry(QtCore.QRect(210, 70, 131, 20))
        self.MaskEdit.setObjectName("MaskEdit")

        self.intIP = QtWidgets.QLabel(self.centralwidget)
        self.intIP.setGeometry(QtCore.QRect(60, 40, 110, 23))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding,
                                           QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.intIP.sizePolicy().hasHeightForWidth())
        self.intIP.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.intIP.setFont(font)
        self.intIP.setObjectName("intIP")
        self.IpEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.IpEdit.setGeometry(QtCore.QRect(210, 40, 131, 20))
        self.IpEdit.setObjectName("IpEdit")

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 389, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.checkbox = QtWidgets.QCheckBox(MainWindow)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.checkbox.setFont(font)
        self.checkbox.setGeometry(QtCore.QRect(210, 100, 150, 20))

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        MainWindow.setCentralWidget(self.centralwidget)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "PyNet"))
        self.intMASK.setText(_translate("MainWindow", "Subnet Mask"))
        self.CommitIntEdit.setText(_translate("MainWindow", "Commit"))
        self.checkbox.setText(_translate("MainWindow", "No Shutdown"))
        self.intIP.setText(_translate("MainWindow", "IP Address"))