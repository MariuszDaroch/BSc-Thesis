from PyQt5 import QtCore, QtWidgets

from Error import Ui_Error
from UserCreator import Ui_UserCreator


class Ui_Users:
    PrevWindow = None
    vendor = None  #0-Juniper 1-Cisco
    dev = None
    data = []
    """
    data[x][0] - name
    data[x][1] - level 0-unauthorized 1-read-only 15-super-user
    """
    def reload(self):
        self.data.clear()
        self.UsersList.clear()
        usersData = self.dev.get_users()
        for i in usersData:
            if i != "admin" and i != "root":
                self.data.append([i,
                                  usersData[i]['level']])
                self.UsersList.addItem(self.data[-1][0])

    def openErrorWindow(self, txt):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_Error()
        self.ui.setupUi(self.window, self.Users)
        self.ui.reload(txt)
        self.window.show()

    def delete(self):
        try:
            row = self.UsersList.currentRow()
            if self.vendor == 0:
                self.dev.load_merge_candidate(
                    config="delete system login user " + self.data[row][0])
            if self.vendor == 1:
                self.dev.load_merge_candidate(
                    config="no username " + self.data[row][0])
            self.dev.commit_config()
        except Exception as e:
            self.openErrorWindow(e)
        self.reload()

    def add(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_UserCreator()
        self.ui.setupUi(self.window, self.Users)
        self.ui.dev = self.dev
        self.ui.vendor = self.vendor
        self.ui.data = self.data
        self.ui.add = True
        self.ui.reload()
        self.window.show()

    def edit(self):
        try:
            row = self.UsersList.currentRow()
            self.window = QtWidgets.QMainWindow()
            self.ui = Ui_UserCreator()
            self.ui.setupUi(self.window, self.Users)
            self.ui.row = row
            self.ui.vendor = self.vendor
            self.ui.data = self.data
            self.ui.dev = self.dev
            self.ui.add = False
            self.ui.reload()
            self.window.show()
        except Exception as e:
            self.openErrorWindow(e)


    def exit(self):
        self.PrevWindow.show()
        self.centralwidget.window().close()

    def setupUi(self, Users, PrevWindow):
        self.PrevWindow = PrevWindow
        self.PrevWindow.hide()
        self.Users = Users

        Users.setObjectName("Users")
        Users.resize(390, 475)
        Users.setMinimumSize(QtCore.QSize(390, 475))
        Users.setMaximumSize(QtCore.QSize(390, 475))
        self.centralwidget = QtWidgets.QWidget(Users)
        self.centralwidget.setObjectName("centralwidget")
        self.UsersList = QtWidgets.QListWidget(self.centralwidget)
        self.UsersList.setGeometry(QtCore.QRect(40, 30, 131, 301))
        self.UsersList.setObjectName("UsersList")
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
        Users.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Users)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 390, 21))
        self.menubar.setObjectName("menubar")
        Users.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Users)
        self.statusbar.setObjectName("statusbar")
        Users.setStatusBar(self.statusbar)

        self.retranslateUi(Users)
        QtCore.QMetaObject.connectSlotsByName(Users)

    def retranslateUi(self, Users):
        _translate = QtCore.QCoreApplication.translate
        Users.setWindowTitle(_translate("Users", "PyNet"))
        self.SelectBtn.setText(_translate("Users", "Select"))
        self.DeleteBtn.setText(_translate("Users", "Delete"))
        self.AddBtn.setText(_translate("Users", "Add"))
        self.ReloadBtn.setText(_translate("Users", "Reload"))
        self.ExitBtn.setText(_translate("Users", "Exit"))