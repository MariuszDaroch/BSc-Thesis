from PyQt5 import QtCore, QtWidgets
from netmiko import ConnectHandler

from Error import Ui_Error
from RoutingCreatorRouter import Ui_StaticRoutingCreatorRouter

def cidr_to_netmask(netmask):
    cidr = int(netmask)
    mask = (0xffffffff >> (32 - cidr)) << (32 - cidr)

    res = (str((0xff000000 & mask) >> 24) + '.' +
           str((0x00ff0000 & mask) >> 16) + '.' +
           str((0x0000ff00 & mask) >> 8) + '.' +
           str((0x000000ff & mask)))
    return res


class Ui_RoutingRouter(object):
    router = None
    PrevWindow = None
    RoutingRouter = None
    data = []
    def reload(self):
        self.data.clear()
        self.RoutingList.clear()

        device = ["10.0.1.2", "ios", "router", "admin", "Cisco"]
        try:
            router = {
                'device_type': 'cisco_ios',
                'host': device[0],
                'username': device[3],
                'password': device[4],
                'secret': 'secret',
            }

            router_tmp = ConnectHandler(**router)
            txt = router_tmp.send_command('show ip route', use_textfsm=True)
            print(txt)
            for i in txt:
                # noinspection PyTypeChecker
                if i["protocol"] == "S":
                    # noinspection PyTypeChecker
                    self.data.append([i["network"],
                                      i["mask"],
                                      i["nexthop_ip"]])
                    self.RoutingList.addItem(self.data[-1][0]+"/"+self.data[-1][1] + " | " + self.data[-1][2])
        except Exception as e:
            self.openErrorWindow(e)

    def add(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_StaticRoutingCreatorRouter()
        self.ui.setupUi(self.window, self.RoutingRouter)
        self.ui.router = self.router
        self.window.show()

    def delete(self):
        try:
            row = self.RoutingList.currentRow()
            self.router.load_merge_candidate(
                config="no ip route " + self.data[row][0] + " " + cidr_to_netmask(self.data[row][1]) + " " + self.data[row][2])
            self.router.commit_config()
            self.reload()
        except Exception as e:
            self.openErrorWindow(e)

    def edit(self):
        try:
            row = self.RoutingList.currentRow()
            self.window = QtWidgets.QMainWindow()
            self.ui = Ui_StaticRoutingCreatorRouter()
            self.ui.setupUi(self.window, self.RoutingRouter)
            self.ui.router = self.router
            self.ui.data = self.data
            self.ui.row = row
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
        self.ui.setupUi(self.window, self.RoutingRouter)
        self.ui.reload(txt)
        self.window.show()

    def setupUi(self, RoutingRouter, PrevWindow):
        self.PrevWindow = PrevWindow
        self.PrevWindow.hide()
        self.RoutingRouter = RoutingRouter

        RoutingRouter.setObjectName("Routing")
        RoutingRouter.resize(390, 475)
        RoutingRouter.setMinimumSize(QtCore.QSize(390, 475))
        RoutingRouter.setMaximumSize(QtCore.QSize(390, 475))
        self.centralwidget = QtWidgets.QWidget(RoutingRouter)
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
        RoutingRouter.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(RoutingRouter)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 390, 21))
        self.menubar.setObjectName("menubar")
        RoutingRouter.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(RoutingRouter)
        self.statusbar.setObjectName("statusbar")
        RoutingRouter.setStatusBar(self.statusbar)

        self.retranslateUi(RoutingRouter)
        QtCore.QMetaObject.connectSlotsByName(RoutingRouter)

    def retranslateUi(self, RoutingRouter):
        _translate = QtCore.QCoreApplication.translate
        RoutingRouter.setWindowTitle(_translate("RoutingRouter", "PyNet"))
        self.SelectBtn.setText(_translate("RoutingRouter", "Select"))
        self.DeleteBtn.setText(_translate("RoutingRouter", "Delete"))
        self.AddBtn.setText(_translate("RoutingRouter", "Add"))
        self.ReloadBtn.setText(_translate("RoutingRouter", "Reload"))
        self.ExitBtn.setText(_translate("RoutingRouter", "Back"))


