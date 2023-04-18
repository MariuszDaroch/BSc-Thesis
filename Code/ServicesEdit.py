from PyQt5 import QtGui, QtCore, QtWidgets

from Error import Ui_Error


class Ui_ServicesEdit():
    PrevWindow = None
    firewall = None
    data = None
    zone_name = None
    tmp = []
    row = None
    services_tmp = []
    empty = None
    services = ['dhcp', 'dhcpv6', 'dns', 'ftp', 'http', 'https', 'netconf', 'ntp', 'ping', 'snmp', 'snmp-trap', 'ssh',
                'telnet']

    def reload(self):
        if self.data[self.row][1][0] != 0:
            self.empty = False
            if self.data[self.row][1][0] == "all":
                self.tmp = self.services.copy()
                for i in self.tmp:
                    self.servicesSelected.addItem(i)
            else:
                self.tmp = self.data[self.row][1].copy()
                self.servicesSelected.addItems(self.tmp)
                self.servicesList.addItems(set(self.services) - set(self.tmp))
        else:
            self.empty = True
            self.servicesList.addItems(self.services)

    def exit(self):
        self.PreviousWindow.show()
        self.centralwidget.window().close()

    def commit(self):
        try:
            if self.servicesList.count() == 0:
                if self.empty:
                    self.firewall.load_merge_candidate(
                            config="set security zones security-zone " + str(self.zone_name) + " host-inbound-traffic system-services all")
                else:
                    self.firewall.load_merge_candidate(
                        config="delete security zones security-zone " + str(self.zone_name) + " host-inbound-traffic system-services ")
                    self.firewall.load_merge_candidate(
                        config="set security zones security-zone " + str(self.zone_name) + " host-inbound-traffic system-services all")
            if self.servicesSelected.count() == 0:
                if not self.empty:
                    self.firewall.load_merge_candidate(
                        config="delete security zones security-zone " + str(self.zone_name) + " host-inbound-traffic system-services ")
            else:
                if self.empty:
                    for i in self.tmp:
                        self.firewall.load_merge_candidate(
                            config="set security zones security-zone " + str(self.zone_name) + " host-inbound-traffic system-services " + i)
                else:
                    self.firewall.load_merge_candidate(
                        config="delete security zones security-zone " + str(self.zone_name) + " host-inbound-traffic system-services ")
                    for i in self.tmp:
                        self.firewall.load_merge_candidate(
                            config="set security zones security-zone " + str(self.zone_name) + " host-inbound-traffic system-services " + i)
            self.firewall.commit_config()
            self.exit()
        except Exception as e:
            self.openErrorWindow(e)

    def dragAllRight(self):
        try:
            for i in range(self.servicesList.count()):
                interface = self.servicesList.takeItem(0)
                self.servicesSelected.addItem(interface)
                self.tmp.append(interface.text())
        except Exception as e:
            self.openErrorWindow(e)

    def dragOneRight(self):
        if len(self.servicesList) > 0:
            try:
                row = self.servicesList.currentRow()
                rowItem = self.servicesList.takeItem(row)
                self.servicesSelected.addItem(rowItem)
                self.tmp.append(rowItem.text())
            except Exception as e:
                self.openErrorWindow(e)

    def dragOneLeft(self):
        if len(self.servicesSelected) > 0:
            try:
                row = self.servicesSelected.currentRow()
                rowItem = self.servicesSelected.takeItem(row)
                self.servicesList.addItem(rowItem)
                self.tmp.remove(rowItem.text())
            except Exception as e:
                self.openErrorWindow(e)

    def dragAllLeft(self):
        try:
            for i in range(self.servicesSelected.count()):
                self.servicesList.addItem(self.servicesSelected.takeItem(0))
            self.tmp.clear()
        except Exception as e:
            self.openErrorWindow(e)

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
        MainWindow.resize(618, 605)
        MainWindow.setMinimumSize(QtCore.QSize(618, 605))
        MainWindow.setMaximumSize(QtCore.QSize(618, 605))

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.servicesList = QtWidgets.QListWidget(self.centralwidget)
        self.servicesList.setGeometry(QtCore.QRect(50, 20, 201, 511))
        self.servicesList.setMinimumSize(QtCore.QSize(201, 511))
        self.servicesList.setMaximumSize(QtCore.QSize(201, 511))
        self.servicesList.setObjectName("servicesList")

        self.servicesSelected = QtWidgets.QListWidget(self.centralwidget)
        self.servicesSelected.setGeometry(QtCore.QRect(370, 20, 201, 511))
        self.servicesSelected.setMinimumSize(QtCore.QSize(201, 511))
        self.servicesSelected.setMaximumSize(QtCore.QSize(201, 511))
        self.servicesSelected.setObjectName("servicesSelected")

        self.dragAllRightBtn = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: self.dragAllRight())
        self.dragAllRightBtn.setGeometry(QtCore.QRect(270, 180, 75, 23))
        self.dragAllRightBtn.setObjectName("dragAllRight")

        self.dragOneRightBtn = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: self.dragOneRight())
        self.dragOneRightBtn.setGeometry(QtCore.QRect(270, 220, 75, 23))
        self.dragOneRightBtn.setObjectName("dragOneRight")

        self.dragOneLeftBtn = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: self.dragOneLeft())
        self.dragOneLeftBtn.setGeometry(QtCore.QRect(270, 260, 75, 23))
        self.dragOneLeftBtn.setObjectName("dragOneLeft")

        self.dragAllLeftBtn = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: self.dragAllLeft())
        self.dragAllLeftBtn.setGeometry(QtCore.QRect(270, 300, 75, 23))
        self.dragAllLeftBtn.setObjectName("dragAllLeft")

        self.commitBtn = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: self.commit())
        self.commitBtn.setGeometry(QtCore.QRect(270, 500, 75, 23))
        self.commitBtn.setObjectName("commit")

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 618, 21))
        self.menubar.setObjectName("menubar")

        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setCentralWidget(self.centralwidget)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "PyNet"))
        self.dragAllRightBtn.setText(_translate("MainWindow", ">>"))
        self.dragOneRightBtn.setText(_translate("MainWindow", ">"))
        self.dragOneLeftBtn.setText(_translate("MainWindow", "<"))
        self.dragAllLeftBtn.setText(_translate("MainWindow", "<<"))
        self.commitBtn.setText(_translate("MainWindow", "Commit"))
