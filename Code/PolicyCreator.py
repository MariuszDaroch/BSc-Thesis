import ipaddress

from PyQt5 import QtCore, QtWidgets

from Error import Ui_Error


def ip_valid(data):
    try:

        for i in data:
            j = i.split("/")
            if ipaddress.IPv4Address(j[0]) and 0 <= int(j[1]) <= 32:
                continue
            else:
                return False

        return True
    except Exception as e:
        print(e)
        return False


def sourceDestAddres(data):
    try:
        tmp = data.split(";")
        if len(tmp) > 1:
            for i in tmp:
                if i == "any":
                    return False
            if not ip_valid(tmp):
                return False
        if len(tmp) == 1:
            if not tmp[0] == 'any':
                if not ip_valid(tmp):
                    return False
        if len(tmp) == 0:
            return False
    except Exception as e:
        print(e)
        return False
    return True


class Ui_PolicyCreator:
    PrevWindow = None
    PolicyCreator = None
    row = None
    """
       [x][0] - from zone
       [x][1] - to zone
       [x][2] - policy name
       [x][3][] - soruce address
       [x][4][] - destination address
       [x][5] - then (permit/deny)
    """
    data = None
    firewall = None
    selectedFrom = None
    selectedTo = None
    zonesList = None
    isItEdit = False

    def reload(self):
        try:
            self.fromZoneList.clear()
            self.toZoneList.clear()
            self.fromZoneList.addItems(self.zonesList)
            self.toZoneList.addItems(self.zonesList)

            if self.isItEdit:
                self.selectedFrom = self.data[self.row][0]
                row = self.zonesList.index(self.selectedFrom)
                self.fromZoneList.setCurrentRow(row)
                self.selectedTo = self.data[self.row][1]
                row = self.zonesList.index(self.selectedTo)
                self.toZoneList.setCurrentRow(row)
                self.policyNameEdit.setText(self.data[self.row][2])

                for source in self.data[self.row][3]:
                    if not self.sourceAddressEdit.text():
                        self.sourceAddressEdit.setText(source)
                    else:
                        self.sourceAddressEdit.setText(self.sourceAddressEdit.text() + ";" + source)

                for destination in self.data[self.row][4]:
                    if not self.destinationAddressEdit.text():
                        self.destinationAddressEdit.setText(destination)
                    else:
                        self.destinationAddressEdit.setText(self.destinationAddressEdit.text() + ";" + destination)

                if self.data[self.row][5] == "permit":
                    self.thenCheckBox.setChecked(True)
        except Exception as e:
            self.openErrorWindow(e)

    def commit(self):
        try:
            if not self.valid(self.data):
                self.openErrorWindow("Data not valid")
            else:
                if self.row:
                    if self.selectedFrom == self.fromZoneList.currentItem().text() and \
                            self.selectedTo == self.toZoneList.currentItem().text() and \
                            self.policyNameEdit.text() == self.data[self.row][2] and \
                            self.data[self.row][3] == self.sourceAddressEdit.text().split(";") and \
                            self.data[self.row][4] == self.destinationAddressEdit.text().split(";") and \
                            self.thenCheckBox.checkState() == self.data[self.row][5]:
                        self.exit()

                    self.firewall.load_merge_candidate(
                        config="delete security policies from-zone " + self.data[self.row][0] + " to-zone " + \
                               self.data[self.row][1])
                tmp = self.sourceAddressEdit.text().split(";")
                for i in tmp:
                    self.firewall.load_merge_candidate(
                        config="set security policies from-zone " + self.fromZoneList.currentItem().text() + " to-zone " \
                               + self.toZoneList.currentItem().text() + " policy " + self.policyNameEdit.text() + \
                               " match source-address " + i)
                tmp = self.destinationAddressEdit.text().split(";")
                for i in tmp:
                    self.firewall.load_merge_candidate(
                        config="set security policies from-zone " + self.fromZoneList.currentItem().text() + " to-zone " \
                               + self.toZoneList.currentItem().text() + " policy " + self.policyNameEdit.text() + \
                               " match destination-address " + i)
                self.firewall.load_merge_candidate(
                    config="set security policies from-zone " + self.fromZoneList.currentItem().text() + " to-zone " \
                           + self.toZoneList.currentItem().text() + " policy " + self.policyNameEdit.text() + \
                           " match application any")
                if self.thenCheckBox.checkState():
                    self.firewall.load_merge_candidate(
                        config="set security policies from-zone " + self.fromZoneList.currentItem().text() + " to-zone " \
                               + self.toZoneList.currentItem().text() + " policy " + self.policyNameEdit.text() + \
                               " then permit")
                else:
                    self.firewall.load_merge_candidate(
                        config="set security policies from-zone " + self.fromZoneList.currentItem().text() + " to-zone " \
                               + self.toZoneList.currentItem().text() + " policy " + self.policyNameEdit.text() + \
                               " then deny")

                self.firewall.commit_config()
        except Exception as e:
            self.openErrorWindow(e)

    def valid(self, data):
        if not self.isItEdit:
            for i in data:
                if i[0] == self.fromZoneList.currentItem().text() and i[1] == self.toZoneList.currentItem().text():
                    return False
        if self.fromZoneList.currentItem() and self.toZoneList.currentItem() and self.policyNameEdit.text() and sourceDestAddres(
                self.sourceAddressEdit.text()) and sourceDestAddres(self.destinationAddressEdit.text()):
            return True
        return False

    def exit(self):
        self.PrevWindow.show()
        self.centralwidget.window().close()

    def openErrorWindow(self, txt):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_Error()
        self.ui.setupUi(self.window, self.PolicyCreator)
        self.ui.reload(txt)
        self.window.show()

    def setupUi(self, PolicyCreator, PrevWindow):
        self.PrevWindow = PrevWindow
        self.PrevWindow.hide()
        self.PolicyCreator = PolicyCreator

        PolicyCreator.setObjectName("PolicyCreator")
        PolicyCreator.resize(600, 220)
        PolicyCreator.setMinimumSize(QtCore.QSize(600, 220))
        PolicyCreator.setMaximumSize(QtCore.QSize(600, 220))
        self.centralwidget = QtWidgets.QWidget(PolicyCreator)
        self.centralwidget.setObjectName("centralwidget")
        self.fromZoneLabel = QtWidgets.QLabel(self.centralwidget)
        self.fromZoneLabel.setGeometry(QtCore.QRect(40, 30, 61, 16))
        self.fromZoneLabel.setObjectName("fromZoneLabel")
        self.toZoneLabel = QtWidgets.QLabel(self.centralwidget)
        self.toZoneLabel.setGeometry(QtCore.QRect(160, 30, 61, 16))
        self.toZoneLabel.setObjectName("toZoneLabel")
        self.fromZoneList = QtWidgets.QListWidget(self.centralwidget)
        self.fromZoneList.setGeometry(QtCore.QRect(20, 50, 91, 121))
        self.fromZoneList.setObjectName("fromZoneList")
        self.toZoneList = QtWidgets.QListWidget(self.centralwidget)
        self.toZoneList.setGeometry(QtCore.QRect(140, 50, 91, 121))
        self.toZoneList.setObjectName("toZoneList")
        self.policyNameLabel = QtWidgets.QLabel(self.centralwidget)
        self.policyNameLabel.setGeometry(QtCore.QRect(250, 30, 61, 16))
        self.policyNameLabel.setObjectName("policyNameLabel")
        self.policyNameEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.policyNameEdit.setGeometry(QtCore.QRect(250, 50, 171, 20))
        self.policyNameEdit.setObjectName("policyNameEdit")

        self.sourceAddressEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.sourceAddressEdit.setGeometry(QtCore.QRect(250, 100, 171, 20))
        self.sourceAddressEdit.setText("")
        self.sourceAddressEdit.setObjectName("sourceAddressEdit")

        self.sourceAddressLabel = QtWidgets.QLabel(self.centralwidget)
        self.sourceAddressLabel.setGeometry(QtCore.QRect(250, 80, 91, 16))
        self.sourceAddressLabel.setObjectName("sourceAddressLabel")

        self.destinationAddressEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.destinationAddressEdit.setGeometry(QtCore.QRect(250, 150, 171, 20))
        self.destinationAddressEdit.setText("")
        self.destinationAddressEdit.setObjectName("destinationAddressEdit")

        self.destinationAddressLabel = QtWidgets.QLabel(self.centralwidget)
        self.destinationAddressLabel.setGeometry(QtCore.QRect(250, 130, 101, 16))
        self.destinationAddressLabel.setObjectName("destinationAddressLabel")
        self.thenCheckBox = QtWidgets.QCheckBox(self.centralwidget)
        self.thenCheckBox.setGeometry(QtCore.QRect(460, 50, 70, 17))
        self.thenCheckBox.setObjectName("thenCheckBox")
        self.commitBtn = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: self.commit())
        self.commitBtn.setGeometry(QtCore.QRect(460, 120, 75, 23))
        self.commitBtn.setObjectName("commitBtn")
        self.exitBtn = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: self.exit())
        self.exitBtn.setGeometry(QtCore.QRect(460, 90, 75, 23))
        self.exitBtn.setObjectName("exitBtn")
        PolicyCreator.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(PolicyCreator)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 600, 21))
        self.menubar.setObjectName("menubar")
        PolicyCreator.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(PolicyCreator)
        self.statusbar.setObjectName("statusbar")
        PolicyCreator.setStatusBar(self.statusbar)

        self.retranslateUi(PolicyCreator)
        QtCore.QMetaObject.connectSlotsByName(PolicyCreator)

    def retranslateUi(self, PolicyCreator):
        _translate = QtCore.QCoreApplication.translate
        PolicyCreator.setWindowTitle(_translate("PolicyCreator", "PyNet"))
        self.fromZoneLabel.setText(_translate("PolicyCreator", "From Zone"))
        self.toZoneLabel.setText(_translate("PolicyCreator", "To Zone"))
        self.policyNameLabel.setText(_translate("PolicyCreator", "Policy Name"))
        self.sourceAddressLabel.setText(_translate("PolicyCreator", "Source Address"))
        self.destinationAddressLabel.setText(_translate("PolicyCreator", "Destination Address"))
        self.thenCheckBox.setText(_translate("PolicyCreator", "Permit"))
        self.commitBtn.setText(_translate("PolicyCreator", "Commit"))
        self.exitBtn.setText(_translate("PolicyCreator", "Exit"))
