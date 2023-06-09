# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'VlansOnInterface.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets

from EditInterfaceJuniper import Ui_EditInterfacesJuniper
from Error import Ui_Error


def cidr_to_netmask(netmask):
    cidr = int(netmask)
    mask = (0xffffffff >> (32 - cidr)) << (32 - cidr)

    res = (str((0xff000000 & mask) >> 24) + '.' +
           str((0x00ff0000 & mask) >> 16) + '.' +
           str((0x0000ff00 & mask) >> 8) + '.' +
           str((0x000000ff & mask)))
    return res

class Ui_VlansOnInterface(object):
    PrevWindow = None

    data = []
    firewall = None
    interface = None
    interface_name = None

    def reload(self):
        device_interfaces = self.firewall.get_interfaces()
        self.VlanList.clear()
        self.data.clear()
        self.interface_name = "ge-0/0/" + str(self.interface)
        unit0 = False
        for interface in device_interfaces:
            if len(interface) > 9:
                if self.interface_name == interface[0:8]:
                    if unit0:
                        self.VlanList.clear()
                        self.data.clear()
                        unit0 = False
                    try:
                        int_vlan = interface.split(".")
                        ip_address = list(self.firewall.get_interfaces_ip()[interface]['ipv4'].keys())[0]
                        mask = self.firewall.get_interfaces_ip()[interface]['ipv4'][ip_address]['prefix_length']
                        self.data.append([int_vlan[1],
                                         ip_address,
                                         cidr_to_netmask(mask)])
                        self.VlanList.addItem(int_vlan[1])
                    except:
                        int_vlan = interface.split(".")
                        if int_vlan[1] != "32767" and  int_vlan[1] != "16383":
                            self.data.append([int_vlan[1],
                                             "No data",
                                             "No data"])
                            self.VlanList.addItem(int_vlan[1])
                        continue

            if self.interface_name == interface and device_interfaces[interface]['is_up']:
                unit0 = True
                try:
                    ip_address = list(self.firewall.get_interfaces_ip()[interface]['ipv4'].keys())[0]
                    mask = self.firewall.get_interfaces_ip()[interface]['ipv4'][ip_address]['prefix_length']
                    self.data.append([0,
                                    ip_address,
                                    cidr_to_netmask(mask)])
                except:
                    self.data.append([0,
                                      "No data",
                                      "No data"])
                    self.VlanList.addItem("0")
                    continue

    def add(self):

        if self.AddVlanEdit.text().isnumeric():
            if len(self.data) == 0:
                if self.AddVlanEdit.text() != "0":
                    self.firewall.load_merge_candidate(
                        config="set interfaces " + str(self.interface_name) + " vlan-tagging unit " + self.AddVlanEdit.text() + " vlan-id " + self.AddVlanEdit.text())
                    self.firewall.commit_config()
                else:
                    self.firewall.load_merge_candidate(
                        config="set interfaces " + str(self.interface_name) + " unit " + self.AddVlanEdit.text())
                    self.firewall.commit_config()
            else:
                if self.data[0][0] != "0":
                    if self.AddVlanEdit.text() != "0":
                        self.firewall.load_merge_candidate(
                            config="set interfaces " + str(
                                self.interface_name) + " vlan-tagging unit " + self.AddVlanEdit.text() + " vlan-id " + self.AddVlanEdit.text())
                        self.firewall.commit_config()
                    else:
                        self.openErrorWindow("Błąd nie można dodać vlanu o")
                else:
                    self.openErrorWindow("Błąd nie można dodać żadnego VLAN przy unit 0")
            self.reload()

    def delete(self):
        try:
            if self.VlanList.count() == 1:
                self.firewall.load_merge_candidate(
                    config="delete interfaces " + str(self.interface_name))
                self.firewall.commit_config()
            else:
                row = self.VlanList.currentRow()
                name = self.VlanList.item(row).text()

                self.firewall.load_merge_candidate(
                    config="delete interfaces " + str(self.interface_name) + " unit " + name)
                self.firewall.commit_config()
            self.reload()
        except Exception as e:
            self.openErrorWindow(e)

    def select(self):
        row = self.VlanList.currentRow()
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_EditInterfacesJuniper()
        self.ui.data = self.data[row]
        self.ui.interface = self.interface
        self.ui.firewall = self.firewall
        self.ui.setupUi(self.window, self.VlansOnInterface)
        self.ui.reload()
        self.window.show()

    def exit(self):
        self.PrevWindow.show()
        self.centralwidget.window().close()

    def openErrorWindow(self, txt):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_Error()
        self.ui.setupUi(self.window, self.VlansOnInterface)
        self.ui.reload(txt)
        self.window.show()

    def setupUi(self, VlansOnInterface, PrevWindow):
        self.PrevWindow = PrevWindow
        self.PrevWindow.hide()
        self.VlansOnInterface = VlansOnInterface

        VlansOnInterface.setObjectName("VlansOnInterface")
        VlansOnInterface.resize(390, 475)
        VlansOnInterface.setMinimumSize(QtCore.QSize(390, 475))
        VlansOnInterface.setMaximumSize(QtCore.QSize(390, 475))
        self.centralwidget = QtWidgets.QWidget(VlansOnInterface)
        self.centralwidget.setObjectName("centralwidget")
        self.VlanList = QtWidgets.QListWidget(self.centralwidget)
        self.VlanList.setGeometry(QtCore.QRect(40, 30, 131, 301))
        self.VlanList.setObjectName("VlanList")
        self.SelectBtn = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: self.select())
        self.SelectBtn.setGeometry(QtCore.QRect(190, 100, 75, 23))
        self.SelectBtn.setObjectName("SelectBtn")
        self.DeleteBtn = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: self.delete())
        self.DeleteBtn.setGeometry(QtCore.QRect(190, 140, 75, 23))
        self.DeleteBtn.setObjectName("DeleteBtn")
        self.AddVlanButton = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: self.add())
        self.AddVlanButton.setGeometry(QtCore.QRect(200, 360, 75, 23))
        self.AddVlanButton.setObjectName("AddVlanButton")
        self.AddVlanEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.AddVlanEdit.setGeometry(QtCore.QRect(40, 360, 131, 20))
        self.AddVlanEdit.setObjectName("AddVlanEdit")
        self.AddVlanText = QtWidgets.QLabel(self.centralwidget)
        self.AddVlanText.setGeometry(QtCore.QRect(70, 340, 47, 13))
        self.AddVlanText.setObjectName("AddVlanText")
        self.ReloadBtn = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: self.reload())
        self.ReloadBtn.setGeometry(QtCore.QRect(200, 400, 75, 23))
        self.ReloadBtn.setObjectName("ReloadBtn")
        self.ExitBtn = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: self.exit())
        self.ExitBtn.setGeometry(QtCore.QRect(290, 400, 75, 23))
        self.ExitBtn.setObjectName("CommitBtn")
        VlansOnInterface.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(VlansOnInterface)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 390, 21))
        self.menubar.setObjectName("menubar")
        VlansOnInterface.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(VlansOnInterface)
        self.statusbar.setObjectName("statusbar")
        VlansOnInterface.setStatusBar(self.statusbar)

        self.retranslateUi(VlansOnInterface)
        QtCore.QMetaObject.connectSlotsByName(VlansOnInterface)

    def retranslateUi(self, VlansOnInterface):
        _translate = QtCore.QCoreApplication.translate
        VlansOnInterface.setWindowTitle(_translate("VlansOnInterface", "PyNet"))
        self.SelectBtn.setText(_translate("VlansOnInterface", "Select"))
        self.DeleteBtn.setText(_translate("VlansOnInterface", "Delete"))
        self.AddVlanButton.setText(_translate("VlansOnInterface", "Add"))
        self.AddVlanText.setText(_translate("VlansOnInterface", "Add VLAN"))
        self.ReloadBtn.setText(_translate("VlansOnInterface", "Reload"))
        self.ExitBtn.setText(_translate("VlansOnInterface", "Exit"))
