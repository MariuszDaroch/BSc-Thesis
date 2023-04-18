from PyQt5 import QtCore, QtGui, QtWidgets

from Error import Ui_Error


class Ui_ZonesInterfaces:
    PrevWindow = None
    firewall = None
    data = None
    zone_name = None
    tmp = []
    row = None
    empty = None
    noInterface = None
    selected = None

    def reload(self):
        try:
            self.tmp.clear()
            if len(self.data[-1])>0:
                self.noInterface = False
                for i in self.data[-1]:
                    self.interfacesAvailable.addItem(i)

            if len(self.data[-1]) == 0:
                self.noInterface = True

            if self.data[self.row][2][0] != 0:
                self.empty = False
                for i in self.data[self.row][2]:
                    self.interfacesSelected.addItem(i)
                    self.tmp.append(i)
            else:
                self.empty = True
        except Exception as e:
            self.openErrorWindow(e)

    def commit(self):
        try:
            if self.empty and self.noInterface:
                self.exit()
            if self.empty and not self.noInterface:
                if self.interfacesSelected.count() == 0:
                    self.exit()
                else:
                    for i in self.tmp:
                        self.firewall.load_merge_candidate(
                            config="set security zones security-zone " + str(
                                self.zone_name) + " interfaces " + i)
            if not self.empty and self.noInterface:
                if self.interfacesAvailable.count() == 0:
                    self.exit()
                else:
                    self.firewall.load_merge_candidate(
                        config="delete security zones security-zone " + str(
                            self.zone_name) + " interfaces ")
                    for i in self.tmp:
                        self.firewall.load_merge_candidate(
                            config="set security zones security-zone " + str(
                                self.zone_name) + " interfaces " + i)
            if not self.empty and not self.noInterface:
                if self.tmp == self.data[self.row][2]:
                    self.exit()
                else:
                    self.firewall.load_merge_candidate(
                        config="delete security zones security-zone " + str(
                            self.zone_name) + " interfaces")
                    for i in self.tmp:
                        self.firewall.load_merge_candidate(
                            config="set security zones security-zone " + str(
                                self.zone_name) + " interfaces " + i)
            self.firewall.commit_config()
            self.exit()
        except Exception as e:
            self.openErrorWindow(e)

    def exit(self):
        self.PrevWindow.show()
        self.centralwidget.window().close()

    def dragAllRight(self):
        try:
            for i in range(self.interfacesAvailable.count()):
                interface = self.interfacesAvailable.takeItem(0)
                self.interfacesSelected.addItem(interface)
                self.tmp.append(interface.text())
        except Exception as e:
            self.openErrorWindow(e)

    def dragOneRight(self):
        if len(self.interfacesAvailable) > 0:
            try:
                row = self.interfacesAvailable.currentRow()
                rowItem = self.interfacesAvailable.takeItem(row)
                self.interfacesSelected.addItem(rowItem)
                self.tmp.append(rowItem.text())
            except Exception as e:
                self.openErrorWindow(e)

    def dragOneLeft(self):
        if len(self.interfacesSelected) > 0:
            try:
                row = self.interfacesSelected.currentRow()
                rowItem = self.interfacesSelected.takeItem(row)
                self.interfacesAvailable.addItem(rowItem)
                self.tmp.remove(rowItem.text())
            except Exception as e:
                self.openErrorWindow(e)

    def dragAllLeft(self):
        try:
            for i in range(self.interfacesSelected.count()):
                self.interfacesAvailable.addItem(self.interfacesSelected.takeItem(0))
            self.tmp.clear()
        except Exception as e:
            self.openErrorWindow(e)

    def openErrorWindow(self, txt):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_Error()
        self.ui.setupUi(self.window, self.MainWindow)
        self.ui.reload(txt)
        self.window.show()

    def setupUi(self, MainWindow, PrevWindow):
        self.PrevWindow = PrevWindow
        self.PrevWindow.hide()
        self.MainWindow = MainWindow

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(618, 605)
        MainWindow.setMinimumSize(QtCore.QSize(618, 605))
        MainWindow.setMaximumSize(QtCore.QSize(618, 605))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.interfacesAvailable = QtWidgets.QListWidget(self.centralwidget)
        self.interfacesAvailable.setGeometry(QtCore.QRect(50, 20, 201, 511))
        self.interfacesAvailable.setMinimumSize(QtCore.QSize(201, 511))
        self.interfacesAvailable.setMaximumSize(QtCore.QSize(201, 511))
        self.interfacesAvailable.setObjectName("interfacesAvailable")

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

        self.interfacesSelected = QtWidgets.QListWidget(self.centralwidget)
        self.interfacesSelected.setGeometry(QtCore.QRect(370, 20, 201, 511))
        self.interfacesSelected.setObjectName("interfacesSelected")

        self.commitBtn = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: self.commit())
        self.commitBtn.setGeometry(QtCore.QRect(270, 500, 75, 23))
        self.commitBtn.setObjectName("commit")

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 618, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "PyNet"))
        self.dragAllRightBtn.setText(_translate("MainWindow", ">>"))
        self.dragOneRightBtn.setText(_translate("MainWindow", ">"))
        self.dragOneLeftBtn.setText(_translate("MainWindow", "<"))
        self.dragAllLeftBtn.setText(_translate("MainWindow", "<<"))
        self.commitBtn.setText(_translate("MainWindow", "Commit"))
