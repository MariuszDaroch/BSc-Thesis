# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'VLANsWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtWidgets
from jnpr.junos import Device
from pyqt5_plugins.examplebuttonplugin import QtGui

from Error import Ui_Error


class Ui_VLANsWindow:
    VLANsWindow = None
    PrevWindow = None
    dev = None
    switch = None
    """
    [0]-vlan list by name
    [x][0]-Vlan name
    [x][1]-Vlan ID
    """
    Vlans = []

    def reload(self):
        self.Vlans.clear()
        self.vlanList.clear()
        try:
            if not self.dev:
                self.dev = Device(host='14.0.0.2',
                                  user='root',
                                  password='Juniper')
                self.dev.open()
            data = self.dev.rpc.get_config(filter_xml='vlans',
                                           options={'format': 'json'})
            vlansData = data['configuration']['vlans']['vlan']
            self.Vlans = [[]]
            for i in vlansData:
                self.Vlans[0].append(i["name"])
                self.Vlans.append([i["name"],
                                   i["vlan-id"]])
                self.vlanList.addItem(self.Vlans[-1][0] + "|" + str(self.Vlans[-1][1]))
        except Exception as e:
            self.openErrorWindow(e)

    def add(self):
        try:
            data = self.inputVlan.text().split("|")

            if len(data[0]) > 0 and data[1].isnumeric():
                self.switch.load_merge_candidate(
                    config="set vlans " + data[0] + " vlan-id " + str(data[1]))
                self.vlanList.addItem(data[0] + "|" + str(data[1]))
                self.switch.commit_config()
                self.Vlans.append([data[0],
                                   data[1]])
                self.reload()
            self.inputVlan.clear()
        except Exception as e:
            self.openErrorWindow(e)

    def delete(self):
        try:
            row = self.vlanList.currentRow()
            name = self.vlanList.item(row).text()
            name = name.split("|")
            self.switch.load_merge_candidate(
                config="delete vlans " + name[0])
            self.vlanList.takeItem(row)
            self.switch.commit_config()
            self.reload()
        except Exception as e:
            self.openErrorWindow(e)

    def openErrorWindow(self, txt):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_Error()
        self.ui.setupUi(self.window, self.VLANsWindow)
        self.ui.reload(txt)
        self.window.show()

    def exit(self):
        self.PrevWindow.show()
        self.centralwidget.window().close()

    def setupUi(self, VLANsWindow, PrevWindow):
        self.PrevWindow = PrevWindow
        self.PrevWindow.hide()
        self.MainWindow = VLANsWindow

        VLANsWindow.setObjectName("VLANsWindow")
        VLANsWindow.resize(340, 430)
        VLANsWindow.setMinimumSize(QtCore.QSize(340, 430))
        VLANsWindow.setMaximumSize(QtCore.QSize(340, 430))
        self.centralwidget = QtWidgets.QWidget(VLANsWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.addVLAN = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: self.add())
        self.addVLAN.setGeometry(QtCore.QRect(160, 360, 75, 23))
        self.addVLAN.setObjectName("addVLAN")
        self.removeVLAN = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: self.delete())
        self.removeVLAN.setGeometry(QtCore.QRect(160, 300, 75, 23))
        self.removeVLAN.setObjectName("removeVLAN")
        self.inputVlan = QtWidgets.QLineEdit(self.centralwidget)
        self.inputVlan.setGeometry(QtCore.QRect(10, 360, 141, 20))
        self.inputVlan.setObjectName("inputVlan")
        self.vlanList = QtWidgets.QListWidget(self.centralwidget)
        self.vlanList.setGeometry(QtCore.QRect(10, 10, 141, 311))
        self.vlanList.setObjectName("vlanList")
        self.exitBtn = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: self.exit())
        self.exitBtn.setGeometry(QtCore.QRect(250, 360, 75, 23))
        self.exitBtn.setObjectName("exitBtn")
        VLANsWindow.setCentralWidget(self.centralwidget)

        self.addlabel = QtWidgets.QLabel(self.centralwidget)
        self.addlabel.setEnabled(True)
        self.addlabel.setGeometry(QtCore.QRect(10, 330, 75, 23))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.addlabel.setFont(font)
        self.addlabel.setAcceptDrops(False)
        self.addlabel.setScaledContents(False)
        self.addlabel.setWordWrap(False)
        self.addlabel.setObjectName("label")

        self.retranslateUi(VLANsWindow)
        QtCore.QMetaObject.connectSlotsByName(VLANsWindow)

    def retranslateUi(self, VLANsWindow):
        _translate = QtCore.QCoreApplication.translate
        VLANsWindow.setWindowTitle(_translate("VLANsWindow", "PyNet"))
        self.addVLAN.setText(_translate("VLANsWindow", "Add"))
        self.removeVLAN.setText(_translate("VLANsWindow", "Delete"))
        self.exitBtn.setText(_translate("VLANsWindow", "Exit"))
        self.addlabel.setText(_translate("VLANsWindow", "XYZ|123"))



