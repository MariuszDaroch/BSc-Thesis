import re

from PyQt5 import QtCore, QtWidgets
from jnpr.junos import Device

from Error import Ui_Error
from ServicesEdit import Ui_ServicesEdit
from ZonesInterfaces import Ui_ZonesInterfaces


class Ui_Zones(object):
    firewall = None
    zones = None
    data = []
    idx = 0
    dev = None

    def reload(self):
        self.data.clear()
        self.ZoneList.clear()
        self.idx = 0
        try:
            self.dev = Device(host='13.0.0.1',
                              user='root',
                              password='Juniper')
            self.dev.open()
            data = self.dev.rpc.get_config(filter_xml='security',
                                           options={'format': 'json'})

            self.zones = data['configuration']['security']['zones']['security-zone']

            for zones in self.zones:
                self.data.append([zones['name']])
                self.ZoneList.addItem(self.data[self.idx][0])
                try:
                    self.data[self.idx].append([])
                    services = zones['host-inbound-traffic']['system-services']
                    for sys_serv in services:
                        self.data[self.idx][1].append(sys_serv["name"])
                except Exception as e:
                    self.data[self.idx][1].append(0)

                try:
                    self.data[self.idx].append([])
                    interfaces = zones['interfaces']
                    for sys_serv in interfaces:
                        self.data[self.idx][2].append(sys_serv["name"])
                except Exception as e:
                    self.data[self.idx][2].append(0)
                self.idx = self.idx + 1
        except Exception as e:
            self.openErrorWindow(e)

        self.allInterfaces()
        self.availableInterfaces()

    def allInterfaces(self):
        try:
            interface = self.dev.rpc.get_config(filter_xml='interfaces',
                                                options={'format': 'json'})
            self.data.append([])
            for i in interface['configuration']['interfaces']['interface']:
                address = i["name"]
                for j in i['unit']:
                    mask = j["name"]
                    self.data[self.idx].append(str(address) + "." + str(mask))
        except Exception as e:
            self.openErrorWindow(e)

    def availableInterfaces(self):
        try:
            tmp = []
            for i in self.data[:-1]:
                for j in i[2]:
                    if j != 0:
                        tmp.append(j)
            self.data.append(set(self.data[-1]) - set(tmp))
        except Exception as e:
            self.openErrorWindow(e)

    def add(self):
        regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
        error = True
        if len(self.AddEdit.text()) > 0:
            if not regex.search(self.AddEdit.text()):
                for i in self.data[:-2]:
                    if i[0] == self.AddEdit.text():
                        error = False
                if error:
                    self.firewall.load_merge_candidate(
                        config="set security zones security-zone " + self.AddEdit.text())
                    self.firewall.commit_config()
                    self.reload()
                else:
                    self.openErrorWindow("Data Error")

    def delete(self):
        try:
            row = self.ZoneList.currentRow()
            name = self.ZoneList.takeItem(row)
            self.firewall.load_merge_candidate(
                config="delete security zones security-zone " + name.text())
            self.firewall.commit_config()
            self.reload()
        except Exception as e:
            self.openErrorWindow(e)

    def openErrorWindow(self, txt):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_Error()
        self.ui.setupUi(self.window, self.Zones)
        self.ui.reload(txt)
        self.window.show()

    def exit(self):
        try:
            if self.dev:
                self.dev.close()
        except Exception as e:
            print(e)

        self.PrevWindow.show()
        self.centralwidget.window().close()

    def openServicesInterface(self):
        row = self.ZoneList.currentRow()
        name = self.ZoneList.item(row).text()
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_ServicesEdit()
        self.ui.zone_name = name
        self.ui.row = row
        self.ui.firewall = self.firewall
        self.ui.data = self.data
        self.ui.setupUi(self.window, self.Zones)
        self.ui.reload()
        self.window.show()

    def openZoneInterface(self):
        row = self.ZoneList.currentRow()
        name = self.ZoneList.item(row).text()
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_ZonesInterfaces()
        self.ui.zone_name = name
        self.ui.row = row
        self.ui.firewall = self.firewall
        self.ui.data = self.data
        self.ui.setupUi(self.window, self.Zones)
        self.ui.reload()
        self.window.show()

    def setupUi(self, Zones, PrevWindow):
        self.PrevWindow = PrevWindow
        self.PrevWindow.hide()
        self.Zones = Zones

        Zones.setObjectName("Zones")
        Zones.resize(390, 475)
        Zones.setMinimumSize(QtCore.QSize(390, 475))
        Zones.setMaximumSize(QtCore.QSize(390, 475))
        self.centralwidget = QtWidgets.QWidget(Zones)
        self.centralwidget.setObjectName("centralwidget")
        self.ZoneList = QtWidgets.QListWidget(self.centralwidget)
        self.ZoneList.setGeometry(QtCore.QRect(40, 30, 131, 301))
        self.ZoneList.setObjectName("ZoneList")
        self.ServicesBtn = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: self.openServicesInterface())
        self.ServicesBtn.setGeometry(QtCore.QRect(190, 140, 75, 23))
        self.ServicesBtn.setObjectName("ServicesBtn")
        self.DeleteBtn = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: self.delete())
        self.DeleteBtn.setGeometry(QtCore.QRect(190, 100, 75, 23))
        self.DeleteBtn.setObjectName("DeleteBtn")
        self.AddBtn = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: self.add())
        self.AddBtn.setGeometry(QtCore.QRect(190, 360, 75, 23))
        self.AddBtn.setObjectName("AddBtn")
        self.ReloadBtn = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: self.reload())
        self.ReloadBtn.setGeometry(QtCore.QRect(190, 400, 75, 23))
        self.ReloadBtn.setObjectName("ReloadBtn")
        self.ExitBtn = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: self.exit())
        self.ExitBtn.setGeometry(QtCore.QRect(290, 400, 75, 23))
        self.ExitBtn.setObjectName("CommitBtn")
        self.InterfacesBtn = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: self.openZoneInterface())
        self.InterfacesBtn.setGeometry(QtCore.QRect(190, 180, 75, 23))
        self.InterfacesBtn.setObjectName("InterfacesBtn")
        self.AddEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.AddEdit.setGeometry(QtCore.QRect(40, 360, 131, 20))
        self.AddEdit.setObjectName("lineEdit")
        Zones.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Zones)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 390, 21))
        self.menubar.setObjectName("menubar")
        Zones.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Zones)
        self.statusbar.setObjectName("statusbar")
        Zones.setStatusBar(self.statusbar)

        self.retranslateUi(Zones)
        QtCore.QMetaObject.connectSlotsByName(Zones)

    def retranslateUi(self, Zones):
        _translate = QtCore.QCoreApplication.translate
        Zones.setWindowTitle(_translate("Zones", "PyNet"))
        self.ServicesBtn.setText(_translate("Zones", "Services"))
        self.DeleteBtn.setText(_translate("Zones", "Delete"))
        self.AddBtn.setText(_translate("Zones", "Add"))
        self.ReloadBtn.setText(_translate("Zones", "Reload"))
        self.ExitBtn.setText(_translate("Zones", "Back"))
        self.InterfacesBtn.setText(_translate("Zones", "Interfaces"))
