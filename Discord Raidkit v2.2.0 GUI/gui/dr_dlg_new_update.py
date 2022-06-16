# Form implementation generated from reading ui file 'dr_dlg_new_update.ui'
#
# Created by: PyQt6 UI code generator 6.3.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_dlgNewUpdate(object):
    def setupUi(self, dlgNewUpdate):
        dlgNewUpdate.setObjectName("dlgNewUpdate")
        dlgNewUpdate.resize(362, 188)
        dlgNewUpdate.setMinimumSize(QtCore.QSize(362, 188))
        dlgNewUpdate.setMaximumSize(QtCore.QSize(362, 188))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        dlgNewUpdate.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("images/icon.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        dlgNewUpdate.setWindowIcon(icon)
        self.gridLayout = QtWidgets.QGridLayout(dlgNewUpdate)
        self.gridLayout.setObjectName("gridLayout")
        self.lblNewUpdateTitle = QtWidgets.QLabel(dlgNewUpdate)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        self.lblNewUpdateTitle.setFont(font)
        self.lblNewUpdateTitle.setObjectName("lblNewUpdateTitle")
        self.gridLayout.addWidget(self.lblNewUpdateTitle, 0, 0, 1, 1)
        self.lblNewUpdateDesc1 = QtWidgets.QLabel(dlgNewUpdate)
        self.lblNewUpdateDesc1.setObjectName("lblNewUpdateDesc1")
        self.gridLayout.addWidget(self.lblNewUpdateDesc1, 2, 0, 1, 1)
        self.dlgNewUpdateBtnBox = QtWidgets.QDialogButtonBox(dlgNewUpdate)
        self.dlgNewUpdateBtnBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.dlgNewUpdateBtnBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.No|QtWidgets.QDialogButtonBox.StandardButton.Yes)
        self.dlgNewUpdateBtnBox.setObjectName("dlgNewUpdateBtnBox")
        self.gridLayout.addWidget(self.dlgNewUpdateBtnBox, 7, 0, 1, 1)
        self.lblNewUpdateDesc2 = QtWidgets.QLabel(dlgNewUpdate)
        self.lblNewUpdateDesc2.setObjectName("lblNewUpdateDesc2")
        self.gridLayout.addWidget(self.lblNewUpdateDesc2, 3, 0, 1, 1)
        self.cbOpenDR = QtWidgets.QCheckBox(dlgNewUpdate)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(8)
        self.cbOpenDR.setFont(font)
        self.cbOpenDR.setChecked(False)
        self.cbOpenDR.setObjectName("cbOpenDR")
        self.gridLayout.addWidget(self.cbOpenDR, 5, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.gridLayout.addItem(spacerItem1, 4, 0, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.gridLayout.addItem(spacerItem2, 6, 0, 1, 1)

        self.retranslateUi(dlgNewUpdate)
        self.dlgNewUpdateBtnBox.accepted.connect(dlgNewUpdate.accept) # type: ignore
        self.dlgNewUpdateBtnBox.rejected.connect(dlgNewUpdate.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(dlgNewUpdate)

    def retranslateUi(self, dlgNewUpdate):
        _translate = QtCore.QCoreApplication.translate
        dlgNewUpdate.setWindowTitle(_translate("dlgNewUpdate", "Update Discord Raidkit"))
        self.lblNewUpdateTitle.setText(_translate("dlgNewUpdate", "New Discord Raidkit Update!"))
        self.lblNewUpdateDesc1.setText(_translate("dlgNewUpdate", "There has been a new release of Discord Raidkit"))
        self.lblNewUpdateDesc2.setText(_translate("dlgNewUpdate", "Would you like to view the release page?"))
        self.cbOpenDR.setText(_translate("dlgNewUpdate", "If yes, continue with program?"))