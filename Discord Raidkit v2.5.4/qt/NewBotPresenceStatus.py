# Form implementation generated from reading ui file 'NewBotPresenceStatus.ui'
#
# Created by: PyQt6 UI code generator 6.7.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_DlgNewBotPresenceStatus(object):
    def setupUi(self, DlgNewBotPresenceStatus):
        DlgNewBotPresenceStatus.setObjectName("DlgNewBotPresenceStatus")
        DlgNewBotPresenceStatus.resize(320, 320)
        DlgNewBotPresenceStatus.setMinimumSize(QtCore.QSize(320, 320))
        DlgNewBotPresenceStatus.setMaximumSize(QtCore.QSize(320, 320))
        self.buttonBox = QtWidgets.QDialogButtonBox(parent=DlgNewBotPresenceStatus)
        self.buttonBox.setGeometry(QtCore.QRect(10, 270, 301, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.lblNewBotPresenceStatus = QtWidgets.QLabel(parent=DlgNewBotPresenceStatus)
        self.lblNewBotPresenceStatus.setGeometry(QtCore.QRect(20, 0, 281, 41))
        self.lblNewBotPresenceStatus.setObjectName("lblNewBotPresenceStatus")
        self.lblNewBotPresenceStatus2 = QtWidgets.QLabel(parent=DlgNewBotPresenceStatus)
        self.lblNewBotPresenceStatus2.setGeometry(QtCore.QRect(20, 40, 271, 31))
        self.lblNewBotPresenceStatus2.setObjectName("lblNewBotPresenceStatus2")
        self.lblNewBotPresenceStatus3 = QtWidgets.QLabel(parent=DlgNewBotPresenceStatus)
        self.lblNewBotPresenceStatus3.setGeometry(QtCore.QRect(20, 60, 291, 31))
        self.lblNewBotPresenceStatus3.setObjectName("lblNewBotPresenceStatus3")
        self.rdOnline = QtWidgets.QRadioButton(parent=DlgNewBotPresenceStatus)
        self.rdOnline.setGeometry(QtCore.QRect(20, 100, 171, 21))
        self.rdOnline.setObjectName("rdOnline")
        self.rdIdle = QtWidgets.QRadioButton(parent=DlgNewBotPresenceStatus)
        self.rdIdle.setGeometry(QtCore.QRect(20, 120, 151, 21))
        self.rdIdle.setObjectName("rdIdle")
        self.rdDnd = QtWidgets.QRadioButton(parent=DlgNewBotPresenceStatus)
        self.rdDnd.setGeometry(QtCore.QRect(20, 140, 151, 21))
        self.rdDnd.setObjectName("rdDnd")
        self.rdInvisible = QtWidgets.QRadioButton(parent=DlgNewBotPresenceStatus)
        self.rdInvisible.setGeometry(QtCore.QRect(20, 160, 151, 21))
        self.rdInvisible.setObjectName("rdInvisible")
        self.label = QtWidgets.QLabel(parent=DlgNewBotPresenceStatus)
        self.label.setGeometry(QtCore.QRect(20, 210, 71, 16))
        self.label.setObjectName("label")
        self.leStatus = QtWidgets.QLineEdit(parent=DlgNewBotPresenceStatus)
        self.leStatus.setGeometry(QtCore.QRect(100, 207, 191, 20))
        self.leStatus.setObjectName("leStatus")

        self.retranslateUi(DlgNewBotPresenceStatus)
        self.buttonBox.accepted.connect(DlgNewBotPresenceStatus.accept) # type: ignore
        self.buttonBox.rejected.connect(DlgNewBotPresenceStatus.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(DlgNewBotPresenceStatus)

    def retranslateUi(self, DlgNewBotPresenceStatus):
        _translate = QtCore.QCoreApplication.translate
        DlgNewBotPresenceStatus.setWindowTitle(_translate("DlgNewBotPresenceStatus", "Select Status"))
        self.lblNewBotPresenceStatus.setText(_translate("DlgNewBotPresenceStatus", "Select a new bot status."))
        self.lblNewBotPresenceStatus2.setText(_translate("DlgNewBotPresenceStatus", "Note that this will be overriden by the"))
        self.lblNewBotPresenceStatus3.setText(_translate("DlgNewBotPresenceStatus", "status cycle if you have provided statuses."))
        self.rdOnline.setText(_translate("DlgNewBotPresenceStatus", "Online"))
        self.rdIdle.setText(_translate("DlgNewBotPresenceStatus", "Idle"))
        self.rdDnd.setText(_translate("DlgNewBotPresenceStatus", "Do Not Disturb"))
        self.rdInvisible.setText(_translate("DlgNewBotPresenceStatus", "Invisible"))
        self.label.setText(_translate("DlgNewBotPresenceStatus", "Status"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DlgNewBotPresenceStatus = QtWidgets.QDialog()
    ui = Ui_DlgNewBotPresenceStatus()
    ui.setupUi(DlgNewBotPresenceStatus)
    DlgNewBotPresenceStatus.show()
    sys.exit(app.exec())
