# Form implementation generated from reading ui file 'InvokeMsgAllArgs.ui'
#
# Created by: PyQt6 UI code generator 6.7.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_dlgInvokeMsgAllArgs(object):
    def setupUi(self, dlgInvokeMsgAllArgs):
        dlgInvokeMsgAllArgs.setObjectName("dlgInvokeMsgAllArgs")
        dlgInvokeMsgAllArgs.resize(320, 150)
        dlgInvokeMsgAllArgs.setMinimumSize(QtCore.QSize(320, 150))
        dlgInvokeMsgAllArgs.setMaximumSize(QtCore.QSize(320, 150))
        self.btnBox = QtWidgets.QDialogButtonBox(parent=dlgInvokeMsgAllArgs)
        self.btnBox.setGeometry(QtCore.QRect(10, 110, 301, 32))
        self.btnBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.btnBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.btnBox.setObjectName("btnBox")
        self.leMessage = QtWidgets.QLineEdit(parent=dlgInvokeMsgAllArgs)
        self.leMessage.setGeometry(QtCore.QRect(20, 65, 280, 20))
        self.leMessage.setObjectName("leMessage")
        self.lblMessage = QtWidgets.QLabel(parent=dlgInvokeMsgAllArgs)
        self.lblMessage.setGeometry(QtCore.QRect(20, 30, 281, 16))
        self.lblMessage.setObjectName("lblMessage")

        self.retranslateUi(dlgInvokeMsgAllArgs)
        self.btnBox.accepted.connect(dlgInvokeMsgAllArgs.accept) # type: ignore
        self.btnBox.rejected.connect(dlgInvokeMsgAllArgs.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(dlgInvokeMsgAllArgs)

    def retranslateUi(self, dlgInvokeMsgAllArgs):
        _translate = QtCore.QCoreApplication.translate
        dlgInvokeMsgAllArgs.setWindowTitle(_translate("dlgInvokeMsgAllArgs", "Msg All Arguments"))
        self.lblMessage.setText(_translate("dlgInvokeMsgAllArgs", "Enter the message to message all members"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    dlgInvokeMsgAllArgs = QtWidgets.QDialog()
    ui = Ui_dlgInvokeMsgAllArgs()
    ui.setupUi(dlgInvokeMsgAllArgs)
    dlgInvokeMsgAllArgs.show()
    sys.exit(app.exec())
