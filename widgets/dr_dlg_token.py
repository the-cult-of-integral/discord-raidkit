# Form implementation generated from reading ui file 'dr_dlg_token.ui'
#
# Created by: PyQt6 UI code generator 6.2.3
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_dlgToken(object):
    def setupUi(self, dlgToken):
        dlgToken.setObjectName("dlgToken")
        dlgToken.resize(362, 158)
        dlgToken.setMinimumSize(QtCore.QSize(362, 158))
        dlgToken.setMaximumSize(QtCore.QSize(362, 158))
        font = QtGui.QFont()
        font.setFamily("Arial")
        dlgToken.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icon.PNG"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        dlgToken.setWindowIcon(icon)
        self.dlgTokenBtnBox = QtWidgets.QDialogButtonBox(dlgToken)
        self.dlgTokenBtnBox.setGeometry(QtCore.QRect(150, 110, 193, 28))
        self.dlgTokenBtnBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.dlgTokenBtnBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.dlgTokenBtnBox.setObjectName("dlgTokenBtnBox")
        self.lblAuthToken = QtWidgets.QLabel(dlgToken)
        self.lblAuthToken.setGeometry(QtCore.QRect(20, 50, 91, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        self.lblAuthToken.setFont(font)
        self.lblAuthToken.setObjectName("lblAuthToken")
        self.txtAuthToken = QtWidgets.QLineEdit(dlgToken)
        self.txtAuthToken.setGeometry(QtCore.QRect(120, 50, 222, 22))
        self.txtAuthToken.setMaxLength(59)
        self.txtAuthToken.setObjectName("txtAuthToken")

        self.retranslateUi(dlgToken)
        self.dlgTokenBtnBox.accepted.connect(dlgToken.accept) # type: ignore
        self.dlgTokenBtnBox.rejected.connect(dlgToken.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(dlgToken)

    def retranslateUi(self, dlgToken):
        _translate = QtCore.QCoreApplication.translate
        dlgToken.setWindowTitle(_translate("dlgToken", "Choose Auth Token"))
        self.lblAuthToken.setText(_translate("dlgToken", "Auth Token:"))