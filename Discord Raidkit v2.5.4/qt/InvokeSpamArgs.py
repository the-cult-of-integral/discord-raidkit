# Form implementation generated from reading ui file 'InvokeSpamArgs.ui'
#
# Created by: PyQt6 UI code generator 6.7.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_dlgInvokeSpamArgs(object):
    def setupUi(self, dlgInvokeSpamArgs):
        dlgInvokeSpamArgs.setObjectName("dlgInvokeSpamArgs")
        dlgInvokeSpamArgs.resize(320, 150)
        dlgInvokeSpamArgs.setMinimumSize(QtCore.QSize(320, 150))
        dlgInvokeSpamArgs.setMaximumSize(QtCore.QSize(320, 150))
        self.btnBox = QtWidgets.QDialogButtonBox(parent=dlgInvokeSpamArgs)
        self.btnBox.setGeometry(QtCore.QRect(10, 110, 301, 32))
        self.btnBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.btnBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.btnBox.setObjectName("btnBox")
        self.leMessage = QtWidgets.QLineEdit(parent=dlgInvokeSpamArgs)
        self.leMessage.setGeometry(QtCore.QRect(20, 65, 280, 20))
        self.leMessage.setObjectName("leMessage")
        self.lblMessage = QtWidgets.QLabel(parent=dlgInvokeSpamArgs)
        self.lblMessage.setGeometry(QtCore.QRect(20, 30, 281, 16))
        self.lblMessage.setObjectName("lblMessage")

        self.retranslateUi(dlgInvokeSpamArgs)
        self.btnBox.accepted.connect(dlgInvokeSpamArgs.accept) # type: ignore
        self.btnBox.rejected.connect(dlgInvokeSpamArgs.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(dlgInvokeSpamArgs)

    def retranslateUi(self, dlgInvokeSpamArgs):
        _translate = QtCore.QCoreApplication.translate
        dlgInvokeSpamArgs.setWindowTitle(_translate("dlgInvokeSpamArgs", "Spam Arguments"))
        self.lblMessage.setText(_translate("dlgInvokeSpamArgs", "Enter the message to spam to all channels"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    dlgInvokeSpamArgs = QtWidgets.QDialog()
    ui = Ui_dlgInvokeSpamArgs()
    ui.setupUi(dlgInvokeSpamArgs)
    dlgInvokeSpamArgs.show()
    sys.exit(app.exec())
