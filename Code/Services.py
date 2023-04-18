from PyQt5 import QtCore, QtGui, QtWidgets

from Error import Ui_Error
from ServicesEdit import Ui_ServicesEdit
from VlanOnInterface import Ui_VlansOnInterface

def cidr_to_netmask(netmask):
    cidr = int(netmask)
    mask = (0xffffffff >> (32 - cidr)) << (32 - cidr)

    res = (str((0xff000000 & mask) >> 24) + '.' +
           str((0x00ff0000 & mask) >> 16) + '.' +
           str((0x0000ff00 & mask) >> 8) + '.' +
           str((0x000000ff & mask)))
    return res


def buildTextForList(vlan, address, mask):
    txt = vlan
    if len(vlan) > 4:
        txt = txt + " | "
    elif len(vlan) > 3:
        txt = txt + "  | "
    elif len(vlan) > 2:
        txt = txt + "   | "
    elif len(vlan) > 1:
        txt = txt + "     | "
    else:
        txt = txt + "      | "
    txt = txt + str(address) + "/" + str(mask)
    return txt

class Ui_Services(object):
    firewall = None
    intIP = []
    intMASK = []
    intList = []
    intName = []
    data = []
    is_up = []
    is_connect = []
    PrevWindow = None
    Vlanlist = []
    def reload(self):

        _translate = QtCore.QCoreApplication.translate
        interfaceName = []
        for i in self.Vlanlist:
            i.clear()
        self.data.clear()
        try:
            device_interfaces = self.firewall.get_interfaces()
            for interface in device_interfaces:
                if interface[0:2] == "ge" and interface[-2] != "." and interface[-3] != "." and (len(interface) == 8 or len(interface) == 9):
                    if int(interface[-1]) < len(self.intName):
                        try:
                            self.intName[int(interface[-1])].setText(_translate("Interfaces", interface))
                            interfaceName.append(interface)
                        except:
                            self.intName[int(interface[-1])].setText(_translate("Interfaces", interface))
                            interfaceName.append(interface)
        except Exception as e:
            self.openErrorWindow(e)
        device_interfaces = self.firewall.get_interfaces()

        idx = 0
        for intName in interfaceName:
            unit0 = False
            for interface in device_interfaces:
                if len(interface) > 9:
                    if intName == interface[0:8]:
                        if unit0:
                            self.Vlanlist[idx].clear()
                            self.data.clear()
                            unit0 = False
                        try:
                            int_vlan = interface.split(".")
                            ip_address = list(self.firewall.get_interfaces_ip()[interface]['ipv4'].keys())[0]
                            mask = self.firewall.get_interfaces_ip()[interface]['ipv4'][ip_address]['prefix_length']
                            self.data.append([int_vlan[1],
                                              ip_address,
                                              cidr_to_netmask(mask)])
                            self.Vlanlist[idx].addItem(buildTextForList(self.data[-1][0],self.data[-1][1],str(mask)))

                        except:
                            int_vlan = interface.split(".")
                            if int_vlan[1] != "32767" and int_vlan[1] != "16383":
                                self.data.append([int_vlan[1],
                                                  "No data",
                                                  "No data"])
                                self.Vlanlist[idx].addItem(int_vlan[1])
                            continue

                if intName == interface and device_interfaces[interface]['is_up']:
                    unit0 = True
                    try:
                        ip_address = list(self.firewall.get_interfaces_ip()[interface]['ipv4'].keys())[0]
                        mask = self.firewall.get_interfaces_ip()[interface]['ipv4'][ip_address]['prefix_length']
                        self.data.append([0,
                                          ip_address,
                                          cidr_to_netmask(mask)])
                        self.Vlanlist[idx].addItem(buildTextForList(self.data[-1][0], self.data[-1][1], str(mask)))

                    except:
                        self.data.append([0,
                                          "No data",
                                          "No data"])
                        self.Vlanlist[idx].addItem("0")
                        continue
            idx = idx + 1
    def exit(self):
        self.PrevWindow.show()
        self.centralwidget.window().close()

    def openVlanOnInterface(self, intNumber):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_VlansOnInterface()
        self.ui.firewall = self.firewall
        self.ui.interface = intNumber
        self.ui.setupUi(self.window, self.Services)
        self.ui.reload()
        self.window.show()

    def openErrorWindow(self, txt):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_Error()
        self.ui.setupUi(self.window, self.Services)
        self.ui.reload(txt)
        self.window.show()

    def setupUi(self, Services, PrevWindow):
        self.PrevWindow = PrevWindow
        self.PrevWindow.hide()
        self.Services = Services

        Services.setObjectName("Services")
        Services.resize(610, 493)
        Services.setMinimumSize(QtCore.QSize(610, 493))
        Services.setMaximumSize(QtCore.QSize(610, 493))

        self.centralwidget = QtWidgets.QWidget(Services)
        self.centralwidget.setObjectName("centralwidget")

        # Interface name label
        self.IntName0 = QtWidgets.QLabel(self.centralwidget)
        self.IntName0.setGeometry(QtCore.QRect(20, 20, 131, 23))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding,
                                           QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.IntName0.sizePolicy().hasHeightForWidth())
        self.IntName0.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.IntName0.setFont(font)
        self.IntName0.setObjectName("IntName0")

        self.IntName1 = QtWidgets.QLabel(self.centralwidget)
        self.IntName1.setGeometry(QtCore.QRect(20, 220, 131, 23))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding,
                                           QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.IntName1.sizePolicy().hasHeightForWidth())
        self.IntName1.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.IntName1.setFont(font)
        self.IntName1.setObjectName("IntName1")

        self.IntName2 = QtWidgets.QLabel(self.centralwidget)
        self.IntName2.setGeometry(QtCore.QRect(335, 20, 131, 23))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding,
                                           QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.IntName2.sizePolicy().hasHeightForWidth())
        self.IntName2.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.IntName2.setFont(font)
        self.IntName2.setObjectName("IntName2")

        self.IntName3 = QtWidgets.QLabel(self.centralwidget)
        self.IntName3.setGeometry(QtCore.QRect(335, 220, 131, 23))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding,
                                           QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.IntName3.sizePolicy().hasHeightForWidth())
        self.IntName3.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.IntName3.setFont(font)
        self.IntName3.setObjectName("IntName3")

        self.IntEdit0 = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: self.openVlanOnInterface("0"))
        self.IntEdit0.setGeometry(QtCore.QRect(175, 100, 100, 23))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.IntEdit0.setFont(font)
        self.IntEdit0.setObjectName("IntEdit0")

        self.IntEdit1 = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: self.openVlanOnInterface("1"))
        self.IntEdit1.setGeometry(QtCore.QRect(175, 300, 100, 23))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.IntEdit1.setFont(font)
        self.IntEdit1.setObjectName("IntEdit1")

        self.IntEdit2 = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: self.openVlanOnInterface("2"))
        self.IntEdit2.setGeometry(QtCore.QRect(490, 100, 100, 23))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.IntEdit2.setFont(font)
        self.IntEdit2.setObjectName("IntEdit2")

        self.IntEdit3 = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: self.openVlanOnInterface("3"))
        self.IntEdit3.setGeometry(QtCore.QRect(490, 300, 100, 23))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.IntEdit3.setFont(font)
        self.IntEdit3.setObjectName("IntEdit3")

        self.BackBtn = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: self.exit())
        self.BackBtn.setGeometry(QtCore.QRect(510, 450, 75, 23))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.BackBtn.setFont(font)
        self.BackBtn.setObjectName("BackBtn")

        self.reloadBtn = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: self.reload())
        self.reloadBtn.setGeometry(QtCore.QRect(385, 450, 100, 23))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.reloadBtn.setFont(font)
        self.reloadBtn.setObjectName("reloadBtn")

        self.menubar = QtWidgets.QMenuBar(Services)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1000, 21))
        self.menubar.setObjectName("menubar")
        Services.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(Services)
        self.statusbar.setObjectName("statusbar")
        Services.setStatusBar(self.statusbar)

        Services.setCentralWidget(self.centralwidget)
        self.retranslateUi(Services)
        QtCore.QMetaObject.connectSlotsByName(Services)

        self.intName.clear()
        self.intName.append(self.IntName0)
        self.intName.append(self.IntName1)
        self.intName.append(self.IntName2)
        self.intName.append(self.IntName3)

        self.VList1 = QtWidgets.QListWidget(self.centralwidget)
        self.VList1.setGeometry(QtCore.QRect(20, 50, 130, 150))
        self.VList1.setObjectName("VList1")

        self.VList2 = QtWidgets.QListWidget(self.centralwidget)
        self.VList2.setGeometry(QtCore.QRect(20, 250, 130, 150))
        self.VList2.setObjectName("VList2")

        self.VList3 = QtWidgets.QListWidget(self.centralwidget)
        self.VList3.setGeometry(QtCore.QRect(335, 50, 130, 150))
        self.VList3.setObjectName("VList3")

        self.VList4 = QtWidgets.QListWidget(self.centralwidget)
        self.VList4.setGeometry(QtCore.QRect(335, 250, 130, 150))
        self.VList4.setObjectName("VList4")

        self.Vlanlist.clear()
        self.Vlanlist.append(self.VList1)
        self.Vlanlist.append(self.VList2)
        self.Vlanlist.append(self.VList3)
        self.Vlanlist.append(self.VList4)

    def retranslateUi(self, Services):
        _translate = QtCore.QCoreApplication.translate
        Services.setWindowTitle(_translate("Services", "PyNet"))

        self.IntName0.setText(_translate("Services", "Interface 0/0/0"))
        self.IntName1.setText(_translate("Services", "Interface 0/0/1"))
        self.IntName2.setText(_translate("Services", "Interface 0/0/2"))
        self.IntName3.setText(_translate("Services", "Interface 0/0/3"))

        self.IntEdit0.setText(_translate("Services", "Edit"))
        self.IntEdit1.setText(_translate("Services", "Edit"))
        self.IntEdit3.setText(_translate("Services", "Edit"))
        self.IntEdit2.setText(_translate("Services", "Edit"))
        self.BackBtn.setText(_translate("Services", "Back"))
        self.reloadBtn.setText(_translate("Services", "Reload"))
