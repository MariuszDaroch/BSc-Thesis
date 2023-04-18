# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'StaticRoutingCreatorRouter.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
import ipaddress
from PyQt5 import QtCore, QtWidgets

from Error import Ui_Error


def cidr_to_netmask(netmask):
    cidr = int(netmask)
    mask = (0xffffffff >> (32 - cidr)) << (32 - cidr)

    res = (str((0xff000000 & mask) >> 24) + '.' +
           str((0x00ff0000 & mask) >> 16) + '.' +
           str((0x0000ff00 & mask) >> 8) + '.' +
           str((0x000000ff & mask)))
    return res


class Ui_StaticRoutingCreatorRouter:
    router = None
    data = None
    PrevWindow = None
    row = None
    data_result = []


    def reload(self):
        _translate = QtCore.QCoreApplication.translate
        self.NetworkEdit.setText(
            _translate("StaticRoutingCreatorFirewall", self.data[self.row][0] + "/" + self.data[self.row][1]))
        self.NextHopEdit.setText(_translate("StaticRoutingCreatorFirewall", self.data[self.row][2]))

    def valid(self):
        try:
            ipaddress.ip_network(self.NetworkEdit.text())
            ipaddress.ip_address(self.NextHopEdit.text())
            tmp = self.NetworkEdit.text().split("/")

            self.data_result.append(tmp[0])
            self.data_result.append(cidr_to_netmask(tmp[1]))
            self.data_result.append(self.NextHopEdit.text())

            return True
        except Exception as e:
            self.openErrorWindow(e)
            return False

    def commit(self):
        try:
            if self.valid():
                if self.row is not None:
                    if self.NetworkEdit == self.data[self.row][0] + "/" + self.data[self.row][1] and self.NextHopEdit == self.data[self.row][2]:
                        self.exit()
                    else:
                        self.router.load_merge_candidate(
                            config="no ip route " + self.data[self.row][0] + " " + str(cidr_to_netmask(self.data[self.row][1])) + " " +
                                   self.data[self.row][2] + "\n")
                        self.router.commit_config()
                self.router.load_merge_candidate(
                    config="ip route " + self.data_result[0] + " " + self.data_result[1] + " " + self.data_result[2] + "\n")
                self.router.commit_config()
                self.exit()
        except Exception as e:
            self.openErrorWindow(e)

    def exit(self):
        self.PrevWindow.show()
        self.centralwidget.window().close()

    def openErrorWindow(self, txt):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_Error()
        self.ui.setupUi(self.window, self.StaticRoutingCreatorRouter)
        self.ui.reload(txt)
        self.window.show()

    def setupUi(self, StaticRoutingCreatorRouter, PrevWindow):
        self.PrevWindow = PrevWindow
        self.PrevWindow.hide()
        self.StaticRoutingCreatorRouter = StaticRoutingCreatorRouter

        StaticRoutingCreatorRouter.setObjectName("StaticRoutingCreatorRouter")
        StaticRoutingCreatorRouter.resize(350, 220)
        StaticRoutingCreatorRouter.setMinimumSize(QtCore.QSize(350, 220))
        StaticRoutingCreatorRouter.setMaximumSize(QtCore.QSize(350, 220))
        self.centralwidget = QtWidgets.QWidget(StaticRoutingCreatorRouter)
        self.centralwidget.setObjectName("centralwidget")
        self.NetworkLabel = QtWidgets.QLabel(self.centralwidget)
        self.NetworkLabel.setGeometry(QtCore.QRect(20, 20, 61, 16))
        self.NetworkLabel.setObjectName("NetworkLabel")
        self.NetworkEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.NetworkEdit.setGeometry(QtCore.QRect(20, 40, 171, 20))
        self.NetworkEdit.setObjectName("NetworkEdit")
        """ self.MaskEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.MaskEdit.setGeometry(QtCore.QRect(20, 90, 171, 20))
        self.MaskEdit.setText("")
        self.MaskEdit.setObjectName("MaskEdit")
        self.MaskLabel = QtWidgets.QLabel(self.centralwidget)
        self.MaskLabel.setGeometry(QtCore.QRect(20, 70, 91, 16))
        self.MaskLabel.setObjectName("MaskLabel")"""
        self.NextHopEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.NextHopEdit.setGeometry(QtCore.QRect(20, 90, 171, 20))
        self.NextHopEdit.setText("")
        self.NextHopEdit.setObjectName("NextHopEdit")
        self.nextHopLabel = QtWidgets.QLabel(self.centralwidget)
        self.nextHopLabel.setGeometry(QtCore.QRect(20, 70, 91, 16))
        self.nextHopLabel.setObjectName("nextHopLabel")
        self.commitBtn = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: self.commit())
        self.commitBtn.setGeometry(QtCore.QRect(230, 110, 75, 23))
        self.commitBtn.setObjectName("commitBtn")
        self.exitBtn = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: self.exit())
        self.exitBtn.setGeometry(QtCore.QRect(230, 80, 75, 23))
        self.exitBtn.setObjectName("exitBtn")
        StaticRoutingCreatorRouter.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(StaticRoutingCreatorRouter)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 350, 21))
        self.menubar.setObjectName("menubar")
        StaticRoutingCreatorRouter.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(StaticRoutingCreatorRouter)
        self.statusbar.setObjectName("statusbar")
        StaticRoutingCreatorRouter.setStatusBar(self.statusbar)

        self.retranslateUi(StaticRoutingCreatorRouter)
        QtCore.QMetaObject.connectSlotsByName(StaticRoutingCreatorRouter)

    def retranslateUi(self, StaticRoutingCreatorRouter):
        _translate = QtCore.QCoreApplication.translate
        StaticRoutingCreatorRouter.setWindowTitle(_translate("StaticRoutingCreatorRouter", "PyNet"))
        self.NetworkLabel.setText(_translate("StaticRoutingCreatorRouter", "Network"))
        self.nextHopLabel.setText(_translate("StaticRoutingCreatorRouter", "Next-Hop"))
        self.commitBtn.setText(_translate("StaticRoutingCreatorRouter", "Commit"))
        self.exitBtn.setText(_translate("StaticRoutingCreatorRouter", "Exit"))
