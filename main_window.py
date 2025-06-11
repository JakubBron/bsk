import os

from PyQt5 import QtCore, QtWidgets
from psutil import disk_partitions

from config import FILENAMES
from pdf import PDF_Signer, PDF_Verifier
from pendrive import Pendrive


class Ui_MainWindow(object):
    privkey_status_msg = "Private key storage device"
    pubkey_status_msg = "Public key storage directory"
    pen = None
    keys_present = [False, False]

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(737, 445)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setDocumentMode(False)
        MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        MainWindow.setDockOptions(QtWidgets.QMainWindow.AllowTabbedDocks | QtWidgets.QMainWindow.AnimatedDocks)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setObjectName("groupBox")
        self.formLayout_2 = QtWidgets.QFormLayout(self.groupBox)
        self.formLayout_2.setObjectName("formLayout_2")
        self.driveLabel = QtWidgets.QLabel(self.groupBox)
        self.driveLabel.setObjectName("driveLabel")
        self.driveLabel.setStyleSheet("color: red;")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.driveLabel)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.deviceSelector = QtWidgets.QComboBox(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.deviceSelector.sizePolicy().hasHeightForWidth())
        self.deviceSelector.setSizePolicy(sizePolicy)
        self.deviceSelector.setObjectName("deviceSelector")
        self.deviceSelector.currentTextChanged.connect(self.checkKeysPresence)
        self.horizontalLayout.addWidget(self.deviceSelector)
        self.deviceSelectorRefresh = QtWidgets.QPushButton(self.groupBox)
        self.deviceSelectorRefresh.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.deviceSelectorRefresh.sizePolicy().hasHeightForWidth())
        self.deviceSelectorRefresh.setSizePolicy(sizePolicy)
        self.deviceSelectorRefresh.setObjectName("deviceSelectorRefresh")
        self.deviceSelectorRefresh.clicked.connect(self.fetchAvailablePendrives)
        self.horizontalLayout.addWidget(self.deviceSelectorRefresh)
        self.formLayout_2.setLayout(2, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout)
        self.pubkeyLabel = QtWidgets.QLabel(self.groupBox)
        self.pubkeyLabel.setObjectName("pubkeyLabel")
        self.formLayout_2.setWidget(7, QtWidgets.QFormLayout.LabelRole, self.pubkeyLabel)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.publicKeyPath = QtWidgets.QLineEdit(self.groupBox)
        self.publicKeyPath.setObjectName("publicKeyPath")
        self.horizontalLayout_2.addWidget(self.publicKeyPath)
        self.publicKeyBrowse = QtWidgets.QPushButton(self.groupBox)
        self.publicKeyBrowse.setObjectName("publicKeyBrowse")
        self.publicKeyBrowse.clicked.connect(self.browseForPublicKey)
        self.horizontalLayout_2.addWidget(self.publicKeyBrowse)
        self.formLayout_2.setLayout(7, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_2)
        self.commandLinkButton = QtWidgets.QCommandLinkButton(self.groupBox)
        self.commandLinkButton.setObjectName("commandLinkButton")
        self.commandLinkButton.clicked.connect(self.generateKeyPair)
        self.formLayout_2.setWidget(12, QtWidgets.QFormLayout.LabelRole, self.commandLinkButton)
        self.keysStatus = QtWidgets.QLabel(self.groupBox)
        self.keysStatus.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.keysStatus.setObjectName("keysStatus")
        self.formLayout_2.setWidget(12, QtWidgets.QFormLayout.FieldRole, self.keysStatus)
        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 1)
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.formLayout = QtWidgets.QFormLayout(self.tab)
        self.formLayout.setObjectName("formLayout")
        self.label_5 = QtWidgets.QLabel(self.tab)
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.signDocumentPath = QtWidgets.QLineEdit(self.tab)
        self.signDocumentPath.setObjectName("signDocumentPath")
        self.horizontalLayout_3.addWidget(self.signDocumentPath)
        self.signDocumentBrowse = QtWidgets.QPushButton(self.tab)
        self.signDocumentBrowse.setObjectName("signDocumentBrowse")
        self.signDocumentBrowse.clicked.connect(self.browseForDocument)
        self.horizontalLayout_3.addWidget(self.signDocumentBrowse)
        self.formLayout.setLayout(1, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.signTargetPath = QtWidgets.QLineEdit(self.tab)
        self.signTargetPath.setObjectName("signTargetPath")
        self.horizontalLayout_4.addWidget(self.signTargetPath)
        self.signTargetBrowse = QtWidgets.QPushButton(self.tab)
        self.signTargetBrowse.setObjectName("signTargetBrowse")
        self.signTargetBrowse.clicked.connect(self.browseForTarget)
        self.horizontalLayout_4.addWidget(self.signTargetBrowse)
        self.formLayout.setLayout(3, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_4)
        self.label_6 = QtWidgets.QLabel(self.tab)
        self.label_6.setObjectName("label_6")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_6)
        self.signButton = QtWidgets.QCommandLinkButton(self.tab)
        self.signButton.setObjectName("signButton")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.signButton)
        self.signButton.clicked.connect(self.signDocument)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.label_7 = QtWidgets.QLabel(self.tab_2)
        self.label_7.setGeometry(QtCore.QRect(10, 10, 101, 16))
        self.label_7.setObjectName("label_7")
        self.commandLinkButton_2 = QtWidgets.QCommandLinkButton(self.tab_2)
        self.commandLinkButton_2.setGeometry(QtCore.QRect(90, 40, 661, 41))
        self.commandLinkButton_2.setObjectName("commandLinkButton_2")
        self.commandLinkButton_2.clicked.connect(self.verifySignature)
        self.horizontalLayoutWidget_5 = QtWidgets.QWidget(self.tab_2)
        self.horizontalLayoutWidget_5.setGeometry(QtCore.QRect(90, 0, 611, 31))
        self.horizontalLayoutWidget_5.setObjectName("horizontalLayoutWidget_5")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_5)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.validatePath = QtWidgets.QLineEdit(self.horizontalLayoutWidget_5)
        self.validatePath.setObjectName("validatePath")
        self.horizontalLayout_5.addWidget(self.validatePath)
        self.pushButton_5 = QtWidgets.QPushButton(self.horizontalLayoutWidget_5)
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_5.clicked.connect(self.browseForSignature)
        self.horizontalLayout_5.addWidget(self.pushButton_5)
        self.tabWidget.addTab(self.tab_2, "")
        self.gridLayout.addWidget(self.tabWidget, 1, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 737, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        self.fetchAvailablePendrives()
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "B.R.O.N.O.A. file signer"))
        self.groupBox.setTitle(_translate("MainWindow", "Key management"))
        self.driveLabel.setText(_translate("MainWindow", self.privkey_status_msg))
        self.deviceSelectorRefresh.setText(_translate("MainWindow", "Refresh list"))
        self.pubkeyLabel.setText(_translate("MainWindow", self.pubkey_status_msg))
        self.publicKeyBrowse.setText(_translate("MainWindow", "Browse"))
        self.commandLinkButton.setText(_translate("MainWindow", "Generate new key pair"))
        self.keysStatus.setText(_translate("MainWindow", ""))
        self.label_5.setText(_translate("MainWindow", "Document path"))
        self.signDocumentBrowse.setText(_translate("MainWindow", "Browse"))
        self.signTargetBrowse.setText(_translate("MainWindow", "Browse"))
        self.label_6.setText(_translate("MainWindow", "Target path"))
        self.signButton.setText(_translate("MainWindow", "Sign document"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Sign Document"))
        self.label_7.setText(_translate("MainWindow", "Document path"))
        self.commandLinkButton_2.setText(_translate("MainWindow", "Verify signature"))
        self.pushButton_5.setText(_translate("MainWindow", "Browse"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Verify Signature"))

    def fetchAvailablePendrives(self):
        self.deviceSelector.clear()
        partitions = disk_partitions()
        print(partitions)
        for partition in partitions:
            if "removable" in partition.opts:
                self.deviceSelector.addItem(partition.device)

    def browseFor(self, fileType: str, lineEdit: QtWidgets.QLineEdit,
                  filter: str = "All Files (*);;Text Files (*.txt)"):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(None, f"Select {fileType} File", "", filter,
                                                            options=options)
        if fileName:
            lineEdit.setText(fileName)

    def browseForPublicKey(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName = QtWidgets.QFileDialog.getExistingDirectory(None, "Select Public Key Directory", "", options=options)
        if fileName:
            self.publicKeyPath.setText(fileName)
            self.checkKeysPresence()

    def browseForDocument(self):
        self.browseFor("Document", self.signDocumentPath, "PDF Files (*.pdf);;All Files (*)")

    def browseForTarget(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getSaveFileName(None, "Select Target File", "",
                                                            "PDF Files (*.pdf);;All Files (*)", options=options)
        if fileName:
            self.signTargetPath.setText(fileName)

    def browseForSignature(self):
        self.browseFor("Signature", self.validatePath, "PDF Files (*.pdf);;All Files (*)")

    def checkKeysPresence(self):
        drive = self.deviceSelector.currentText()
        public_key_path = self.publicKeyPath.text()

        if drive == "":
            self.driveLabel.setStyleSheet("color: red;")
            self.driveLabel.setText(f"❓{self.privkey_status_msg}")
        elif os.path.isfile(drive+FILENAMES.PRIVATE_KEY_ENCRYPTED):
            self.driveLabel.setStyleSheet("color: green;")
            self.driveLabel.setText(f"✔{self.privkey_status_msg}")
            self.keysStatus.setText("")
            self.keys_present[0] = True
        else:
            self.driveLabel.setStyleSheet("color: gray;")
            self.driveLabel.setText(f"X {self.privkey_status_msg}")

        if public_key_path == "":
            self.pubkeyLabel.setStyleSheet("color: red;")
            self.pubkeyLabel.setText(f"❓{self.pubkey_status_msg}")
        elif os.path.isfile(public_key_path+"/"+FILENAMES.PUBLIC_KEY):
            self.pubkeyLabel.setStyleSheet("color: green;")
            self.keys_present[1] = True
        else:
            self.pubkeyLabel.setStyleSheet("color: gray;")
            self.pubkeyLabel.setText(f"X {self.pubkey_status_msg}")

        if self.keys_present[0] and self.keys_present[1]:
            while self.pen is None:
                pin = QtWidgets.QInputDialog.getText(None, "Enter PIN", "PIN:", QtWidgets.QLineEdit.Password)
                if pin[1]:
                    self.pen = Pendrive(drive, public_key_path, pin[0])
                    self.pen.set_pin(pin[0])
                    if self.pen.check_if_RSA_keys_exist():
                        self.keysStatus.setText("Keys are present")
                        self.keysStatus.setStyleSheet("color: green;")
                    else:
                        self.keysStatus.setText("Keys are LOST")
                        self.keysStatus.setStyleSheet("color: red;")

                    if "UNABLE TO READ" not in self.pen.get_RSA_private_key():
                        self.keysStatus.setText("Keys are present and valid")
                        self.keysStatus.setStyleSheet("color: green;")
                        break
                    self.pen = None
                else:
                    break

    def generateKeyPair(self):
        drive = self.deviceSelector.currentText()
        public_key_path = self.publicKeyPath.text()
        if drive == "" or public_key_path == "":
            QtWidgets.QMessageBox.warning(None, "Error", "Please select drive and directory for keys")
            return
        pin = QtWidgets.QInputDialog.getText(None, "Enter PIN", "PIN:", QtWidgets.QLineEdit.Password)
        if pin[1]:
            self.pen = Pendrive(drive, public_key_path, pin[0])
            msg_box = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Information, "Keys are being generated", "Please wait, keys are being generated.")
            msg_box.setStandardButtons(QtWidgets.QMessageBox.NoButton)
            msg_box.setWindowModality(QtCore.Qt.ApplicationModal)
            msg_box.show()
            
            QtCore.QCoreApplication.processEvents()  # Ensure the UI updates immediately
            
            result = self.pen.save_RSA_keys()
            
            msg_box.close()
            QtWidgets.QMessageBox.information(None, "Result", result)
            self.checkKeysPresence()

    def signDocument(self):
        if self.pen is None:
            QtWidgets.QMessageBox.warning(None, "Error", "Please select drive and directory for keys")
            return
        document_path = self.signDocumentPath.text()
        target_path = self.signTargetPath.text()
        if document_path == "" or target_path == "":
            QtWidgets.QMessageBox.warning(None, "Error", "Please select document and target path")
            return
        if not os.path.isfile(document_path):
            QtWidgets.QMessageBox.warning(None, "Error", "Document does not exist")
            return
        if not os.path.isdir(os.path.dirname(target_path)):
            QtWidgets.QMessageBox.warning(None, "Error", "Target directory does not exist")
            return
        pdf = PDF_Signer(self.pen.get_RSA_private_key(), document_path, target_path)
        result = pdf.sign_pdf()
        QtWidgets.QMessageBox.information(None, "Result", result)
        
    def verifySignature(self):
        if self.pen is None:
            QtWidgets.QMessageBox.warning(None, "Error", "Please select drive and directory for keys")
            return
        document_path = self.validatePath.text()
        if document_path == "":
            QtWidgets.QMessageBox.warning(None, "Error", "Please select document")
            return
        print(self.pen.get_RSA_public_key())
        pdf = PDF_Verifier(self.pen.get_RSA_public_key(), document_path)
        print(document_path)
        result = pdf.validate_signature()
        QtWidgets.QMessageBox.information(None, "Result", result)




if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(window)
    window.show()
    app.exec()
