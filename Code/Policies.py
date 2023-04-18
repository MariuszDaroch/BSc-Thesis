from PyQt5 import QtCore, QtWidgets
from jnpr.junos import Device

from Error import Ui_Error
from PolicyCreator import Ui_PolicyCreator


class Ui_Policies(object):
    firewall = None
    """
    [x][0] - from zone
    [x][1] - to zone
    [x][2] - policy name
    [x][3][] - soruce address
    [x][4][] - destination address
    [x][5] - then (permit/deny)
    """
    data = []
    zonesList = []
    dev = None
    Policies = None
    policies = None
    def reload(self):
        self.zonesList.clear()
        self.data.clear()
        self.PolicyList.clear()
        try:
            self.dev = Device(host='13.0.0.1',
                              user='root',
                              password='Juniper')
            self.dev.open()
            data = self.dev.rpc.get_config(filter_xml='security',
                                           options={'format': 'json'})

            self.policies = data['configuration']['security']['policies']['policy']
            for i in self.policies:
                self.data.append([i['from-zone-name'],
                                  i['to-zone-name'],
                                  i['policy'][0]['name'],
                                  i['policy'][0]['match']['source-address'],
                                  i['policy'][0]['match']['destination-address'],
                                  list(i['policy'][0]['then'].keys())[0]])
                self.PolicyList.addItem("FROM: " + self.data[-1][0] + " TO: " + self.data[-1][1])

            zones = data['configuration']['security']['zones']['security-zone']
            for z in zones:
                self.zonesList.append(z['name'])
        except Exception as e:
            self.openErrorWindow(e)

    def edit(self):
        try:
            row = self.PolicyList.currentRow()
            self.window = QtWidgets.QMainWindow()
            self.ui = Ui_PolicyCreator()
            self.ui.isItEdit = True
            self.ui.setupUi(self.window, self.Policies)
            self.ui.firewall = self.firewall
            self.ui.zonesList = self.zonesList
            self.ui.row = row
            self.ui.data = self.data
            self.ui.reload()
            self.window.show()
        except Exception as e:
            self.openErrorWindow(e)

    def add(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_PolicyCreator()
        self.ui.data = self.data
        self.ui.setupUi(self.window, self.Policies)
        self.ui.zonesList = self.zonesList
        self.ui.firewall = self.firewall
        self.ui.reload()
        self.window.show()

    def delete(self):
        try:
            row = self.PolicyList.currentRow()
            self.firewall.load_merge_candidate(
                config="delete security policies from-zone " + self.data[row][0] + " to-zone " + self.data[row][1])
            self.firewall.commit_config()
            self.reload()
        except Exception as e:
            self.openErrorWindow(e)
    def exit(self):
        self.PrevWindow.show()
        self.centralwidget.window().close()

    def openErrorWindow(self, txt):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_Error()
        self.ui.setupUi(self.window, self.Policies)
        self.ui.reload(txt)
        self.window.show()

    def setupUi(self, Policies, PrevWindow):
        self.PrevWindow = PrevWindow
        self.PrevWindow.hide()
        self.Policies = Policies

        Policies.setObjectName("Policies")
        Policies.resize(390, 475)
        Policies.setMinimumSize(QtCore.QSize(390, 475))
        Policies.setMaximumSize(QtCore.QSize(390, 475))
        self.centralwidget = QtWidgets.QWidget(Policies)
        self.centralwidget.setObjectName("centralwidget")
        self.PolicyList = QtWidgets.QListWidget(self.centralwidget)
        self.PolicyList.setGeometry(QtCore.QRect(20, 30, 205, 301))
        self.PolicyList.setObjectName("PolicyList")
        self.SelectBtn = QtWidgets.QPushButton(self.centralwidget, clicked= lambda: self.edit())
        self.SelectBtn.setGeometry(QtCore.QRect(250, 110, 75, 23))
        self.SelectBtn.setObjectName("SelectBtn")
        self.DeleteBtn = QtWidgets.QPushButton(self.centralwidget, clicked= lambda: self.delete())
        self.DeleteBtn.setGeometry(QtCore.QRect(250, 150, 75, 23))
        self.DeleteBtn.setObjectName("DeleteBtn")
        self.AddBtn = QtWidgets.QPushButton(self.centralwidget, clicked= lambda: self.add())
        self.AddBtn.setGeometry(QtCore.QRect(250, 70, 75, 23))
        self.AddBtn.setObjectName("AddBtn")
        self.ReloadBtn = QtWidgets.QPushButton(self.centralwidget, clicked= lambda: self.reload())
        self.ReloadBtn.setGeometry(QtCore.QRect(200, 400, 75, 23))
        self.ReloadBtn.setObjectName("ReloadBtn")
        self.exitBtn = QtWidgets.QPushButton(self.centralwidget, clicked= lambda: self.exit())
        self.exitBtn.setGeometry(QtCore.QRect(290, 400, 75, 23))
        self.exitBtn.setObjectName("exitBtn")
        Policies.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Policies)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 390, 21))
        self.menubar.setObjectName("menubar")
        Policies.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Policies)
        self.statusbar.setObjectName("statusbar")
        Policies.setStatusBar(self.statusbar)

        self.retranslateUi(Policies)
        QtCore.QMetaObject.connectSlotsByName(Policies)

    def retranslateUi(self, Policies):
        _translate = QtCore.QCoreApplication.translate
        Policies.setWindowTitle(_translate("Policies", "PyNet"))
        self.SelectBtn.setText(_translate("Policies", "Select"))
        self.DeleteBtn.setText(_translate("Policies", "Delete"))
        self.AddBtn.setText(_translate("Policies", "Add"))
        self.ReloadBtn.setText(_translate("Policies", "Reload"))
        self.exitBtn.setText(_translate("Policies", "Back"))


