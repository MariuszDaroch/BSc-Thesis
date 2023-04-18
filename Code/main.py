import json

import napalm

from PyQt5 import QtCore, QtGui, QtWidgets
from jnpr.junos import Device

from Error import Ui_Error
from Interfaces import Ui_Interfaces
from InterfacesVlan import Ui_InterfacesVlan
from Policies import Ui_Policies
from RoutingFirewall import Ui_RoutingFirewall
from RoutingRouter import Ui_RoutingRouter
from RoutingSwitch import Ui_RoutingSwitch
from Services import Ui_Services
from Users import Ui_Users
from VLANsWindow import Ui_VLANsWindow
from Zones import Ui_Zones


class Ui_MainWindow():
    def __init__(self):
        self.router = None
        self.switch = None
        self.firewall = None
        self.routerNCC = None

    def reload(self):
    # Cisco
        self.routerUserNameLabelEdit.setText(self.router.username)
        try:
            self.routerHostNameLabelEdit.setText(self.router.get_facts()["hostname"])
        except:
            pass

    # Juniper
        self.firewallUserlabelEdit.setText(self.firewall.username)
        try:
             self.firewallHostlabelEdit.setText(self.firewall.get_facts()["hostname"])
        except:
             pass

        self.switchUserNameLabelEdit.setText(self.switch.username)
        try:
             self.switchHostNameLabelEdit.setText(self.switch.get_facts()["hostname"])
        except:
            pass

    def initDevice(self):
        driver_junos = napalm.get_network_driver("junos")
        driver_ios = napalm.get_network_driver("ios")
        self.userFirwallBtn.setEnabled(True)
        self.servicesBtn.setEnabled(True)
        self.zonesBtn.setEnabled(True)
        self.policyFirewallBtn.setEnabled(True)
        self.RoutingBtnFirewall.setEnabled(True)

        self.usersSwitchBtn.setEnabled(True)
        self.VLANsBtn.setEnabled(True)
        self.RoutingBtnSwitch.setEnabled(True)
        self.InterfacesBtn_2.setEnabled(True)

        self.userRouterBtn.setEnabled(True)
        self.RoutingBtnRouter.setEnabled(True)
        self.InterfacesBtn.setEnabled(True)

        try:
             self.firewall = driver_junos(hostname="13.0.0.1",
                                          username="root",
                                          password="Juniper")
             self.firewall.open()
        except:
            self.userFirwallBtn.setEnabled(False)
            self.servicesBtn.setEnabled(False)
            self.zonesBtn.setEnabled(False)
            self.policyFirewallBtn.setEnabled(False)
            self.RoutingBtnFirewall.setEnabled(False)

        try:
             self.switch = driver_junos(hostname="14.0.0.2",
                                        username="root",
                                        password="Juniper")
             self.switch.open()
        except:
            self.usersSwitchBtn.setEnabled(False)
            self.VLANsBtn.setEnabled(False)
            self.RoutingBtnSwitch.setEnabled(False)
            self.InterfacesBtn_2.setEnabled(False)

        device = ["10.0.1.2", "ios", "router", "admin", "Cisco"]
        try:
             self.router = driver_ios(hostname=device[0],
                                      username=device[3],
                                      password=device[4])
             self.router.open()
        except:
            self.userRouterBtn.setEnabled(False)
            self.RoutingBtnRouter.setEnabled(False)
            self.InterfacesBtn.setEnabled(False)


    #   open ruter's button
    def openUsersRouter(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_Users()
        self.ui.vendor = 1
        self.ui.dev = self.router
        self.ui.setupUi(self.window, MainWindow)
        self.ui.reload()
        self.window.show()

    def openRoutingRouter(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_RoutingRouter()
        self.ui.setupUi(self.window, MainWindow)
        self.ui.router = self.router
        self.ui.reload()
        self.window.show()

    def openInterfacesWindow(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_Interfaces()
        self.ui.router = self.router
        self.ui.setupUi(self.window, MainWindow)
        self.ui.reload()
        self.window.show()

    #   open Firewall buttons
    def openUserSFirewall(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_Users()
        self.ui.vendor = 0
        self.ui.dev = self.firewall
        self.ui.setupUi(self.window, MainWindow)
        self.ui.reload()
        self.window.show()

    def openServicesWindow(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_Services()
        self.ui.firewall = self.firewall
        self.ui.setupUi(self.window, MainWindow)
        self.ui.reload()
        self.window.show()

    def openRoutingFirewall(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_RoutingFirewall()
        self.ui.setupUi(self.window, MainWindow)
        self.ui.firewall = self.firewall
        self.ui.reload()
        self.window.show()

    def openZonesWindow(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_Zones()
        self.ui.firewall = self.firewall
        self.ui.setupUi(self.window, MainWindow)
        self.ui.reload()
        self.window.show()

    def openPolicyWindow(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_Policies()
        self.ui.firewall = self.firewall
        self.ui.setupUi(self.window, MainWindow)
        self.ui.reload()
        self.window.show()

    #   Open Switch buttons
    def openUsersSwitch(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_Users()
        self.ui.vendor = 0
        self.ui.dev = self.switch
        self.ui.setupUi(self.window, MainWindow)
        self.ui.reload()
        self.window.show()

    def openVlansWindow(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_VLANsWindow()
        self.ui.setupUi(self.window, MainWindow)
        self.ui.switch = self.switch
        self.ui.reload()
        self.window.show()

    def openVlansInterfaces(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_InterfacesVlan()
        self.ui.setupUi(self.window, MainWindow)
        self.ui.switch = self.switch
        self.ui.reload()
        self.window.show()

    def openRoutingSwitch(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_RoutingSwitch()
        self.ui.setupUi(self.window, MainWindow)
        self.ui.switch = self.switch
        self.ui.reload()
        self.window.show()

    def openErrorWindow(self, txt):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_Error()
        self.ui.setupUi(self.window, MainWindow)
        self.ui.reload(txt)
        self.window.show()

    def setupUi(self, MainWindow):

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(720, 600)
        MainWindow.setMinimumSize(QtCore.QSize(1280, 720))
        MainWindow.setMaximumSize(QtCore.QSize(1280, 720))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")


        self.userRouterBtn = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: self.openUsersRouter())
        self.userRouterBtn.setGeometry(QtCore.QRect(300, 20, 161, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.userRouterBtn.setFont(font)
        self.userRouterBtn.setObjectName("userRouterBtn")

        self.RoutingBtnRouter = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: self.openRoutingRouter())
        self.RoutingBtnRouter.setGeometry(QtCore.QRect(470, 80, 151, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.RoutingBtnRouter.setFont(font)
        self.RoutingBtnRouter.setObjectName("RoutingBtnRouter")

        self.InterfacesBtn = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: self.openInterfacesWindow())
        self.InterfacesBtn.setGeometry(QtCore.QRect(300, 80, 161, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.InterfacesBtn.setFont(font)
        self.InterfacesBtn.setObjectName("InterfacesBtn")

        # host name 1
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setEnabled(True)
        self.label.setGeometry(QtCore.QRect(10, 20, 161, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setAcceptDrops(False)
        self.label.setScaledContents(False)
        self.label.setWordWrap(False)
        self.label.setObjectName("label")

        # host name 1 txt
        self.routerHostNameLabelEdit = QtWidgets.QLabel(self.centralwidget)
        self.routerHostNameLabelEdit.setGeometry(QtCore.QRect(160, 20, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.routerHostNameLabelEdit.setFont(font)
        self.routerHostNameLabelEdit.setObjectName("routerHostNameLabelEdit")

        # user name 1
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setEnabled(True)
        self.label_4.setGeometry(QtCore.QRect(10, 60, 161, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_4.setFont(font)
        self.label_4.setAcceptDrops(False)
        self.label_4.setScaledContents(False)
        self.label_4.setWordWrap(False)
        self.label_4.setObjectName("label_4")

        # user name 1 txt
        self.routerUserNameLabelEdit = QtWidgets.QLabel(self.centralwidget)
        self.routerUserNameLabelEdit.setGeometry(QtCore.QRect(160, 60, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.routerUserNameLabelEdit.setFont(font)
        self.routerUserNameLabelEdit.setObjectName("routerUserNameLabelEdit")

        # Switch
        self.usersSwitchBtn = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: self.openUsersSwitch())
        self.usersSwitchBtn.setGeometry(QtCore.QRect(300, 220, 161, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.usersSwitchBtn.setFont(font)
        self.usersSwitchBtn.setObjectName("usersSwitchBtn")

        self.VLANsBtn = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: self.openVlansWindow())
        self.VLANsBtn.setGeometry(QtCore.QRect(470, 220, 161, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.VLANsBtn.setFont(font)
        self.VLANsBtn.setObjectName("VLANsBtn")

        self.RoutingBtnSwitch = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: self.openRoutingSwitch())
        self.RoutingBtnSwitch.setGeometry(QtCore.QRect(470, 280, 161, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.RoutingBtnSwitch.setFont(font)
        self.RoutingBtnSwitch.setObjectName("RoutingBtnSwitch")

        self.InterfacesBtn_2 = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: self.openVlansInterfaces())
        self.InterfacesBtn_2.setGeometry(QtCore.QRect(300, 280, 161, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.InterfacesBtn_2.setFont(font)
        self.InterfacesBtn_2.setObjectName("InterfacesBtn_2")


        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setEnabled(True)
        self.label_7.setGeometry(QtCore.QRect(10, 260, 161, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_7.setFont(font)
        self.label_7.setAcceptDrops(False)
        self.label_7.setScaledContents(False)
        self.label_7.setWordWrap(False)
        self.label_7.setObjectName("label_7")

        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setEnabled(True)
        self.label_8.setGeometry(QtCore.QRect(10, 220, 161, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_8.setFont(font)
        self.label_8.setAcceptDrops(False)
        self.label_8.setScaledContents(False)
        self.label_8.setWordWrap(False)
        self.label_8.setObjectName("label_8")

        self.switchHostNameLabelEdit = QtWidgets.QLabel(self.centralwidget)
        self.switchHostNameLabelEdit.setGeometry(QtCore.QRect(160, 220, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.switchHostNameLabelEdit.setFont(font)
        self.switchHostNameLabelEdit.setObjectName("switchHostNameLabelEdit")

        self.switchUserNameLabelEdit = QtWidgets.QLabel(self.centralwidget)
        self.switchUserNameLabelEdit.setGeometry(QtCore.QRect(160, 260, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.switchUserNameLabelEdit.setFont(font)
        self.switchUserNameLabelEdit.setObjectName("switchUserNameLabelEdit")


        # Firewall
        self.firewallHostlabel = QtWidgets.QLabel(self.centralwidget)
        self.firewallHostlabel.setEnabled(True)
        self.firewallHostlabel.setGeometry(QtCore.QRect(10, 420, 161, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.firewallHostlabel.setFont(font)
        self.firewallHostlabel.setAcceptDrops(False)
        self.firewallHostlabel.setScaledContents(False)
        self.firewallHostlabel.setWordWrap(False)
        self.firewallHostlabel.setObjectName("firewallHostlabel")

        self.firewallUserlabel = QtWidgets.QLabel(self.centralwidget)
        self.firewallUserlabel.setEnabled(True)
        self.firewallUserlabel.setGeometry(QtCore.QRect(10, 460, 161, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.firewallUserlabel.setFont(font)
        self.firewallUserlabel.setAcceptDrops(False)
        self.firewallUserlabel.setScaledContents(False)
        self.firewallUserlabel.setWordWrap(False)
        self.firewallUserlabel.setObjectName("firewallUserlabel")

        self.firewallHostlabelEdit = QtWidgets.QLabel(self.centralwidget)
        self.firewallHostlabelEdit.setGeometry(QtCore.QRect(160, 420, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.firewallHostlabelEdit.setFont(font)
        self.firewallHostlabelEdit.setObjectName("firewallHostlabelEdit")

        self.firewallUserlabelEdit = QtWidgets.QLabel(self.centralwidget)
        self.firewallUserlabelEdit.setGeometry(QtCore.QRect(160, 460, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.firewallUserlabelEdit.setFont(font)
        self.firewallUserlabelEdit.setObjectName("firewallUserlabelEdit")

        self.userFirwallBtn = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: self.openUserSFirewall())
        self.userFirwallBtn.setGeometry(QtCore.QRect(300, 420, 161, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.userFirwallBtn.setFont(font)
        self.userFirwallBtn.setObjectName("userFirwallBtn")

        self.servicesBtn = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: self.openServicesWindow())
        self.servicesBtn.setGeometry(QtCore.QRect(300, 480, 161, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.servicesBtn.setFont(font)
        self.servicesBtn.setObjectName("servicesBtn")

        self.zonesBtn = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: self.openZonesWindow())
        self.zonesBtn.setGeometry(QtCore.QRect(470, 420, 161, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.zonesBtn.setFont(font)
        self.zonesBtn.setObjectName("zonesBtn")

        self.policyFirewallBtn = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: self.openPolicyWindow())
        self.policyFirewallBtn.setGeometry(QtCore.QRect(640, 420, 161, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.policyFirewallBtn.setFont(font)
        self.policyFirewallBtn.setObjectName("policyFirewallBtn")

        self.RoutingBtnFirewall = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: self.openRoutingFirewall())
        self.RoutingBtnFirewall.setGeometry(QtCore.QRect(470, 480, 161, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.RoutingBtnFirewall.setFont(font)
        self.RoutingBtnFirewall.setObjectName("RoutingBtnFirewall")

        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "PyNet"))
        self.userRouterBtn.setText(_translate("MainWindow", "General settings"))
        self.label.setText(_translate("MainWindow", "Host Name"))
        self.routerHostNameLabelEdit.setText(_translate("MainWindow", ""))
        self.routerUserNameLabelEdit.setText(_translate("MainWindow", ""))
        self.label_4.setText(_translate("MainWindow", "User"))

        self.InterfacesBtn.setText(_translate("MainWindow", "Interface"))
        self.VLANsBtn.setText(_translate("MainWindow", "VLANs"))
        self.RoutingBtnRouter.setText(_translate("MainWindow", "Routing"))
        self.usersSwitchBtn.setText(_translate("MainWindow", "Users"))
        self.userRouterBtn.setText(_translate("MainWindow", "Users"))
        self.userFirwallBtn.setText(_translate("MainWindow", "Users"))

        self.label_7.setText(_translate("MainWindow", "User"))
        self.label_8.setText(_translate("MainWindow", "Host Name"))
        self.switchHostNameLabelEdit.setText(_translate("MainWindow", ""))
        self.switchUserNameLabelEdit.setText(_translate("MainWindow", ""))

        self.policyFirewallBtn.setText(_translate("MainWindow", "Policy"))
        self.zonesBtn.setText(_translate("MainWindow", "Zones"))
        self.RoutingBtnSwitch.setText(_translate("MainWindow", "Routing"))
        self.firewallHostlabel.setText(_translate("MainWindow", "Host Name"))
        self.firewallHostlabelEdit.setText(_translate("MainWindow", ""))
        self.firewallUserlabel.setText(_translate("MainWindow", "User"))
        self.firewallUserlabelEdit.setText(_translate("MainWindow", ""))
        self.servicesBtn.setText(_translate("Main Window", "Interfaces"))
        self.RoutingBtnFirewall.setText(_translate("Main Window", "Routing"))
        self.InterfacesBtn_2.setText(_translate("MainWindow", "Intefaces"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.__init__()
    ui.setupUi(MainWindow)
    ui.initDevice()
    ui.reload()
    MainWindow.show()
    sys.exit(app.exec_())