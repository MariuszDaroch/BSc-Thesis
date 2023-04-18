from PyQt5 import QtCore, QtGui, QtWidgets
from jnpr.junos import Device

from Error import Ui_Error
from InterfacesVlanEdit import Ui_InterfacesVlanEdit


class Ui_InterfacesVlan(object):
    PrevWindow = None
    switchInterfaces = None
    dev = None
    switch = None
    intList = []
    intLabel = []
    intName = []

    """[0]-vlan list by name
       [x][0]-Vlan name
       [x][1]-Vlan ID
    """
    Vlans = []

    """
    [x][0]-name
    [x][1]-interface-mode
    [x][2][]=members
    """
    data = []

    def reload(self):
        _translate = QtCore.QCoreApplication.translate
        try:
            for i in self.intList:
                i.clear()
            self.data.clear()
            self.Vlans.clear()
            if not self.dev:
                self.dev = Device(host='14.0.0.2',
                                  user='root',
                                  password='Juniper')
                self.dev.open()
            data = self.dev.rpc.get_config(filter_xml='vlans',
                                           options={'format': 'json'})
            vlansData = data['configuration']['vlans']['vlan']
            self.Vlans = [[]]
            for i in vlansData:
                self.Vlans[0].append(i["name"])
                self.Vlans.append([i["name"],
                                   i["vlan-id"]])
            dataInterfaces = self.dev.rpc.get_config(filter_xml='interfaces',
                                                     options={'format': 'json'})
            interfaces = dataInterfaces['configuration']['interfaces']['interface']
            for i in interfaces:
                tmp2 = False
                try:
                    if i["name"][0:2] == "ge":
                        if i['unit'][0]['family']['ethernet-switching']['interface-mode'] != "None":
                            tmp2 = True
                        if i['unit'][0]['family']['ethernet-switching']['vlan']['members'] != "None":
                            self.data.append([i["name"],
                                              i['unit'][0]['family']['ethernet-switching']['interface-mode'],
                                              i['unit'][0]['family']['ethernet-switching']['vlan']['members']])


                except:
                    if tmp2:
                        self.data.append([i["name"],
                                          i['unit'][0]['family']['ethernet-switching']['interface-mode'],
                                          ["None"]])
                    else:
                        self.data.append([i["name"],
                                          "None",
                                          ["None"]])

            self.data.pop(len(self.data) - 1)
        except Exception as e:
            self.openErrorWindow(e)
        for i in range(0, len(self.data)):
            self.intName[i].setText(_translate("switchInterfaces", self.data[i][0]))
            self.intLabel[i].setText(_translate("switchInterfaces", self.data[i][1]))
            for j in self.data[i][2]:
                if j == "all":
                    for vlans in self.Vlans[0]:
                        self.intList[i].addItem(vlans)
                else:
                    self.intList[i].addItem(j)


    def edit(self, interface):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_InterfacesVlanEdit()
        self.ui.data = self.data
        self.ui.vlans = self.Vlans
        self.ui.switch = self.switch
        self.ui.interface = interface
        self.ui.setupUi(self.window, self.switchInterfaces)
        self.ui.reload()
        self.window.show()

    def exit(self):
        self.PrevWindow.show()
        self.centralwidget.window().close()

    def openErrorWindow(self, txt):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_Error()
        self.ui.setupUi(self.window, self.switchInterfaces)
        self.ui.reload(txt)
        self.window.show()

    def setupUi(self, switchInterfaces, PrevWindow):
        self.PrevWindow = PrevWindow
        self.PrevWindow.hide()
        self.switchInterfaces = switchInterfaces

        switchInterfaces.setObjectName("switchInterfaces")
        switchInterfaces.resize(600, 431)
        switchInterfaces.setMinimumSize(QtCore.QSize(600, 431))
        switchInterfaces.setMaximumSize(QtCore.QSize(600, 431))
        self.centralwidget = QtWidgets.QWidget(switchInterfaces)
        self.centralwidget.setObjectName("centralwidget")

        self.reloadBtn = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: self.reload())
        self.reloadBtn.setGeometry(QtCore.QRect(350, 360, 75, 23))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.reloadBtn.setFont(font)
        self.reloadBtn.setObjectName("reloadBtn")

        self.exitBtn = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: self.exit())
        self.exitBtn.setGeometry(QtCore.QRect(450, 360, 75, 23))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.exitBtn.setFont(font)
        self.exitBtn.setObjectName("exit")

        self.int0List = QtWidgets.QListWidget(self.centralwidget)
        self.int0List.setGeometry(QtCore.QRect(150, 20, 101, 141))
        self.int0List.setObjectName("int0List")

        self.int1List = QtWidgets.QListWidget(self.centralwidget)
        self.int1List.setGeometry(QtCore.QRect(150, 180, 101, 141))
        self.int1List.setObjectName("int1List")

        self.int2List = QtWidgets.QListWidget(self.centralwidget)
        self.int2List.setGeometry(QtCore.QRect(450, 20, 101, 141))
        self.int2List.setObjectName("int2List")

        self.int3List = QtWidgets.QListWidget(self.centralwidget)
        self.int3List.setGeometry(QtCore.QRect(450, 180, 101, 141))
        self.int3List.setObjectName("int3List")

        self.int0ModeLabel = QtWidgets.QLabel(self.centralwidget)
        self.int0ModeLabel.setGeometry(QtCore.QRect(30, 50, 71, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.int0ModeLabel.setFont(font)
        self.int0ModeLabel.setObjectName("int0ModeLabel")

        self.int1ModeLabel = QtWidgets.QLabel(self.centralwidget)
        self.int1ModeLabel.setGeometry(QtCore.QRect(30, 210, 71, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.int1ModeLabel.setFont(font)
        self.int1ModeLabel.setObjectName("int1ModeLabel")

        self.int2ModeLabel = QtWidgets.QLabel(self.centralwidget)
        self.int2ModeLabel.setGeometry(QtCore.QRect(330, 50, 71, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.int2ModeLabel.setFont(font)

        self.int2ModeLabel.setObjectName("int2ModeLabel")
        self.int3ModeLabel = QtWidgets.QLabel(self.centralwidget)
        self.int3ModeLabel.setGeometry(QtCore.QRect(330, 210, 71, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.int3ModeLabel.setFont(font)
        self.int3ModeLabel.setObjectName("int3ModeLabel")

        self.int0NameLabel = QtWidgets.QLabel(self.centralwidget)
        self.int0NameLabel.setGeometry(QtCore.QRect(10, 10, 131, 23))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding,
                                           QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.int0NameLabel.sizePolicy().hasHeightForWidth())
        self.int0NameLabel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.int0NameLabel.setFont(font)
        self.int0NameLabel.setObjectName("int0NameLabel")

        self.int1NameLabel = QtWidgets.QLabel(self.centralwidget)
        self.int1NameLabel.setGeometry(QtCore.QRect(10, 170, 131, 23))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding,
                                           QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.int1NameLabel.sizePolicy().hasHeightForWidth())
        self.int1NameLabel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.int1NameLabel.setFont(font)
        self.int1NameLabel.setObjectName("int1NameLabel")

        self.int2NameLabel = QtWidgets.QLabel(self.centralwidget)
        self.int2NameLabel.setGeometry(QtCore.QRect(310, 10, 131, 23))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding,
                                           QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.int2NameLabel.sizePolicy().hasHeightForWidth())
        self.int2NameLabel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.int2NameLabel.setFont(font)
        self.int2NameLabel.setObjectName("int2NameLabel")

        self.int3NameLabel = QtWidgets.QLabel(self.centralwidget)
        self.int3NameLabel.setGeometry(QtCore.QRect(310, 170, 131, 23))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding,
                                           QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.int3NameLabel.sizePolicy().hasHeightForWidth())
        self.int3NameLabel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.int3NameLabel.setFont(font)
        self.int3NameLabel.setObjectName("int3NameLabel")

        self.int0Edit = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: self.edit("0"))
        self.int0Edit.setGeometry(QtCore.QRect(30, 120, 75, 23))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.int0Edit.setFont(font)
        self.int0Edit.setObjectName("int0Edit")

        self.int1Edit = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: self.edit("1"))
        self.int1Edit.setGeometry(QtCore.QRect(30, 280, 75, 23))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.int1Edit.setFont(font)
        self.int1Edit.setObjectName("int1Edit")

        self.int2Edit = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: self.edit("2"))
        self.int2Edit.setGeometry(QtCore.QRect(330, 120, 75, 23))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.int2Edit.setFont(font)
        self.int2Edit.setObjectName("int2Edit")

        self.int3Edit = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: self.edit("3"))
        self.int3Edit.setGeometry(QtCore.QRect(330, 280, 75, 23))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.int3Edit.setFont(font)
        self.int3Edit.setObjectName("int3Edit")

        self.intList.clear()
        self.intList.append(self.int0List)
        self.intList.append(self.int1List)
        self.intList.append(self.int2List)
        self.intList.append(self.int3List)

        self.intLabel.clear()
        self.intLabel.append(self.int0ModeLabel)
        self.intLabel.append(self.int1ModeLabel)
        self.intLabel.append(self.int2ModeLabel)
        self.intLabel.append(self.int3ModeLabel)

        self.intName.clear()
        self.intName.append(self.int0NameLabel)
        self.intName.append(self.int1NameLabel)
        self.intName.append(self.int2NameLabel)
        self.intName.append(self.int3NameLabel)

        switchInterfaces.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(switchInterfaces)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 600, 21))
        self.menubar.setObjectName("menubar")
        switchInterfaces.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(switchInterfaces)
        self.statusbar.setObjectName("statusbar")
        switchInterfaces.setStatusBar(self.statusbar)

        self.retranslateUi(switchInterfaces)
        QtCore.QMetaObject.connectSlotsByName(switchInterfaces)

    def retranslateUi(self, switchInterfaces):
        _translate = QtCore.QCoreApplication.translate
        switchInterfaces.setWindowTitle(_translate("switchInterfaces", "PyNet"))
        self.reloadBtn.setText(_translate("switchInterfaces", "Reload"))
        self.exitBtn.setText(_translate("switchInterfaces", "Exit"))
        self.int0ModeLabel.setText(_translate("switchInterfaces", "TextLabel"))
        self.int1ModeLabel.setText(_translate("switchInterfaces", "TextLabel"))
        self.int2ModeLabel.setText(_translate("switchInterfaces", "TextLabel"))
        self.int3ModeLabel.setText(_translate("switchInterfaces", "TextLabel"))
        self.int0NameLabel.setText(_translate("switchInterfaces", "Interface 0/0/0"))
        self.int1NameLabel.setText(_translate("switchInterfaces", "Interface 0/0/0"))
        self.int2NameLabel.setText(_translate("switchInterfaces", "Interface 0/0/0"))
        self.int3NameLabel.setText(_translate("switchInterfaces", "Interface 0/0/0"))
        self.int0Edit.setText(_translate("switchInterfaces", "Edit"))
        self.int1Edit.setText(_translate("switchInterfaces", "Edit"))
        self.int2Edit.setText(_translate("switchInterfaces", "Edit"))
        self.int3Edit.setText(_translate("switchInterfaces", "Edit"))
