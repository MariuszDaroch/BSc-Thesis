from PyQt5 import QtCore, QtWidgets
from jnpr.junos import Device

from Error import Ui_Error
from RoutingCreatorFirewall import Ui_StaticRoutingCreatorFirewall


class Ui_RoutingFirewall(object):
    firewall = None
    PrevWindow = None
    RoutingFirewall = None
    idx = 0
    data = []
    dev = None

    def reload(self):
        self.data.clear()
        self.RoutingList.clear()
        self.idx = 0
        try:
            if not self.dev:
                self.dev = Device(host='13.0.0.1',
                                  user='root',
                                  password='Juniper')
                self.dev.open()
            data = self.dev.rpc.get_config(filter_xml='routing-options',
                                           options={'format': 'json'})

            routing = data['configuration']['routing-options']['static']['route']
            for static in routing:
                tmp = static["next-hop"]
                for i in tmp:
                    self.data.append([static["name"], i])
                    self.RoutingList.addItem(self.data[self.idx][0] + "|" + self.data[self.idx][1])
                    self.idx = self.idx + 1
                print(self.data)
        except Exception as e:
            self.openErrorWindow(e)

    def add(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_StaticRoutingCreatorFirewall()
        self.ui.setupUi(self.window, self.RoutingFirewall)
        self.ui.firewall = self.firewall
        self.window.show()

    def delete(self):
        try:
            row = self.RoutingList.currentRow()
            self.firewall.load_merge_candidate(
                config="delete routing-options static route " + self.data[row][0] + " next-hop " + self.data[row][1])
            self.firewall.commit_config()
            self.reload()
        except Exception as e:
            self.openErrorWindow(e)

    def edit(self):
        try:
            row = self.RoutingList.currentRow()
            name = self.RoutingList.item(row).text()
            self.window = QtWidgets.QMainWindow()
            self.ui = Ui_StaticRoutingCreatorFirewall()
            self.ui.setupUi(self.window, self.RoutingFirewall)
            self.ui.firewall = self.firewall
            self.ui.data = self.data
            self.ui.row = row
            self.ui.name = name
            self.ui.reload()
            self.window.show()
        except Exception as e:
            self.openErrorWindow(e)

    def exit(self):
        self.PrevWindow.show()
        self.centralwidget.window().close()

    def openErrorWindow(self, txt):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_Error()
        self.ui.setupUi(self.window, self.RoutingFirewall)
        self.ui.reload(txt)
        self.window.show()

    def setupUi(self, RoutingFirewall, PrevWindow):
        self.PrevWindow = PrevWindow
        self.PrevWindow.hide()
        self.RoutingFirewall = RoutingFirewall

        RoutingFirewall.setObjectName("Routing")
        RoutingFirewall.resize(390, 475)
        RoutingFirewall.setMinimumSize(QtCore.QSize(390, 475))
        RoutingFirewall.setMaximumSize(QtCore.QSize(390, 475))
        self.centralwidget = QtWidgets.QWidget(RoutingFirewall)
        self.centralwidget.setObjectName("centralwidget")
        self.RoutingList = QtWidgets.QListWidget(self.centralwidget)
        self.RoutingList.setGeometry(QtCore.QRect(40, 30, 131, 301))
        self.RoutingList.setObjectName("RoutingList")
        self.SelectBtn = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: self.edit())
        self.SelectBtn.setGeometry(QtCore.QRect(190, 110, 75, 23))
        self.SelectBtn.setObjectName("SelectBtn")
        self.DeleteBtn = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: self.delete())
        self.DeleteBtn.setGeometry(QtCore.QRect(190, 150, 75, 23))
        self.DeleteBtn.setObjectName("DeleteBtn")
        self.AddBtn = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: self.add())
        self.AddBtn.setGeometry(QtCore.QRect(190, 70, 75, 23))
        self.AddBtn.setObjectName("AddBtn")
        self.ReloadBtn = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: self.reload())
        self.ReloadBtn.setGeometry(QtCore.QRect(200, 400, 75, 23))
        self.ReloadBtn.setObjectName("ReloadBtn")
        self.ExitBtn = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: self.exit())
        self.ExitBtn.setGeometry(QtCore.QRect(290, 400, 75, 23))
        self.ExitBtn.setObjectName("ExitBtn")
        RoutingFirewall.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(RoutingFirewall)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 390, 21))
        self.menubar.setObjectName("menubar")
        RoutingFirewall.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(RoutingFirewall)
        self.statusbar.setObjectName("statusbar")
        RoutingFirewall.setStatusBar(self.statusbar)

        self.retranslateUi(RoutingFirewall)
        QtCore.QMetaObject.connectSlotsByName(RoutingFirewall)

    def retranslateUi(self, RoutingFirewall):
        _translate = QtCore.QCoreApplication.translate
        RoutingFirewall.setWindowTitle(_translate("RoutingFirewall", "PyNet"))
        self.SelectBtn.setText(_translate("RoutingFirewall", "Select"))
        self.DeleteBtn.setText(_translate("RoutingFirewall", "Delete"))
        self.AddBtn.setText(_translate("RoutingFirewall", "Add"))
        self.ReloadBtn.setText(_translate("RoutingFirewall", "Reload"))
        self.ExitBtn.setText(_translate("RoutingFirewall", "Exit"))
