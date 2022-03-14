from PyQt5 import QtGui
from  PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys
import os
import mainParser
import shared
#import textarea

from parserInterface import Ui_MainWindow
#from PyQt5.uic import loadUiType
#MainUI,_ = loadUiType('compilers.ui')


class TextEditDemo(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Input Text")
        self.resize(500, 500)

        self.textEdit = QTextEdit()
        self.btnPress1 = QPushButton("Input data")
        self.clr_btn = QPushButton('Clear')

        layout = QVBoxLayout()
        layout.addWidget(self.textEdit)
        layout.addWidget(self.btnPress1)
        layout.addWidget(self.clr_btn)
        self.clr_btn.clicked.connect(self.clear_text)
        self.setLayout(layout)
        self.btnPress1.clicked.connect(self.btnPress1_Clicked)

    def btnPress1_Clicked(self):
        mytext = self.textEdit.toPlainText()
        if(not mytext):
            QMessageBox.about(self, "information message", "please enter data!")
        else:
            with open('textEditData.txt', 'w') as yourFile:
                yourFile.write(str(mytext))
            global line
            line=mainParser.scannerMain("textEditData.txt")
            QMessageBox.about(self,"information message", "your data has been saved to scan")

    def clear_text(self):
        self.textEdit.clear()
        #self.textEdit.setPlainText("Hello PyQt5!\nfrom pythonpyqt.com")

class Main(QMainWindow,Ui_MainWindow):

    def __init__(self,parent=None):

        super(Main, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.setWindowTitle("Scanner and Parser Application")
        #self.setFixedSize(QSize(1000, 500))

        self.generateScannerOutput.setEnabled(False)
        self.startScanningButton.setEnabled(False)
        self.startParsing.setEnabled(False)
        self.showTree.setEnabled(False)
        self.recursive.setCheckable(False)
        self.ll.setCheckable(False)
        self.insertButton.clicked.connect(self.import_file)
        self.writeStatment.clicked.connect(self.openTextArea)
        #self.generateScannerOutput.connect(self.import_output_file)
        #self.d = self.addressLineEdit.text()
        self.generateScannerOutput.clicked.connect(self.importOutputFile)
        self.startScanningButton.clicked.connect(self.behavior)
        self.showTree.clicked.connect(self.showPicture) #draw tree button
        self.startParsing.clicked.connect(self.parse) #parsing button
        self.clearButton.clicked.connect(self.clearAll)


    def openTextArea(self):
        self.w = TextEditDemo()
        self.w.show()
        self.startScanningButton.setEnabled(True)

    def clearAll(self):
        self.generateScannerOutput.setEnabled(False)
        self.startScanningButton.setEnabled(False)
        self.startParsing.setEnabled(False)
        self.showTree.setEnabled(False)
        self.recursive.setCheckable(False)
        self.ll.setCheckable(False)
        self.parserLineEdit.setText("")
        self.alertLineEdit.setText("")
        self.tokensLineEdit.setText("")
        self.addressLineEdit.setText("")
        self.picture_2.setPixmap(QtGui.QPixmap(""))
        shared.parserErrorMessage=''

    def parse(self):
        if(self.recursive.isChecked()):
            print ("recursive descent")
            try:
                tree = mainParser.program()
                print("inparser")
                tree.DrawTree()
                self.parserLineEdit.setText("Statement accepted")
                self.showTree.setEnabled(True)
            except Exception:
                self.parserLineEdit.setText("Statement not accepted,  " + shared.parserErrorMessage)

        elif(self.ll.isChecked()):
            print("ll1")
            try:
                tree = mainParser.LL1parser()
                print("inparser")
                tree.DrawTree()
                self.parserLineEdit.setText("Statement accepted")
                self.showTree.setEnabled(True)
            except Exception:
                self.parserLineEdit.setText("Statement not accepted," + shared.parserErrorMessage)


    def showPicture(self):
        self.picture_2.setPixmap(QtGui.QPixmap("test4.png"))
        self.picture_2.setScaledContents(True)


    def behavior(self):
        self.alertLineEdit.setText("The file is being scanned......")
        loop = QEventLoop()
        QTimer.singleShot(2000, loop.quit)
        loop.exec_()
        self.alertLineEdit.setText("File is finished !")
        self.generateScannerOutput.setEnabled(True)

    def import_file(self):
        global line
        file_filter='Data File(*.txt)'

        response = QFileDialog.getOpenFileNames(
            parent=self,
            caption='select a data file',
            directory=os.getcwd(),
            filter=file_filter,
            initialFilter='Data File(*.txt)'
        )
        print(response[0])
        word_url =str(response[0]).replace('[','')
        word_url = word_url.replace(']', '')
        word_url = word_url.replace("'", '')
        self.addressLineEdit.setText(word_url)
        self.startScanningButton.setEnabled(True)
        #file_name = re.split('/', word_url)
        #print(file_name[-1])
        #os.startfile(word_url)
        print("word_url")
        if word_url:
            line = mainParser.scannerMain(word_url)
        else:
            self.alertLineEdit.setText("")
            self.tokensLineEdit.setText("")
        #compilers.getUrl(word_url)
        #return word_url


    def importOutputFile(self):
        #compilers.scannerMain(self.import_file())
        #output=compilers.scannerMain(self.import_file())
        os.startfile("outputTokens.txt")
        error=mainParser.getScannerError()
        #print(error)
        if error is False:
            #print("in")
            self.tokensLineEdit.setText(line)
            self.startParsing.setEnabled(True)
            self.recursive.setCheckable(True)
            self.ll.setCheckable(True)
        else:
            self.tokensLineEdit.setText(line)


def main():
    app=QApplication(sys.argv)
    window = Main()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()