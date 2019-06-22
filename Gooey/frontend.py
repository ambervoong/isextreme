import scrape; #here i dunno how to import
import sys;
import logging;
import pandas;

from PyQt5.QtWidgets import (
        QWidget,
        QMainWindow,
        QPushButton,
        QApplication,
        QGridLayout,
        QLabel,
        QTabWidget,
        QVBoxLayout,
        QHBoxLayout,
        QLineEdit,
        QPlainTextEdit,
        QDialog,
        QFileDialog,
        QToolButton,
        )

from PyQt5.QtCore import *

from PyQt5.QtGui import (
        QIntValidator,
        )
class QTextEditLogger(logging.Handler):
    def __init__(self, parent):
        super().__init__()
        self.widget = QPlainTextEdit(parent)
        self.widget.setReadOnly(True)

    def emit(self, record):
        msg = self.format(record)
        self.widget.appendPlainText(msg)

# copied this from stackoverflow i dunno how this works
# need to get the stub ready before i can
# test to see if this bit works
class MyDialog(QDialog, QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)

        logTextBox = QTextEditLogger(self)
        # You can format what is printed to text box
        logTextBox.setFormatter(logging.Formatter('%(message)s'))
        logging.getLogger().addHandler(logTextBox)
        # You can control the logging level
        logging.getLogger().setLevel(logging.DEBUG)

        self._button = QPushButton(self)
        self._button.setText('Test Me')
        self._trial= QPushButton(self)
        self._trial.setText('Add Me')

        layout = QVBoxLayout()
        # Add the new logging box widget to the layout
        layout.addWidget(logTextBox.widget)
        layout.addWidget(self._button)
        layout.addWidget(self._trial)
        self.setLayout(layout)

        #test
        self.maxTerm = -1 

        # Connect signal to slot
        self._button.clicked.connect(self.test)
        self._trial.clicked.connect(self.trial)

    def trial(self):
        logging.error("Trial Testrun Alpha")

    # packs the row into a dictonary
    def packageRow(self, csvVar, row):
        ret_dic = {}
        ret_dic["tweet"] = csvVar["tweet"].iloc[row]
        ret_dic["translated"] = csvVar["translated"].iloc[row]
        ret_dic["date"] = csvVar["date"].iloc[row]
        ret_dic["time"] = csvVar["time"].iloc[row]
        ret_dic["username"] = csvVar["username"].iloc[row]
        ret_dic["label"] = csvVar["label"].iloc[row]
        try:
            if (int(ret_dic["label"]) == 0):
                ret_dic["customlabel"] = "No Threat"
            else:
                ret_dic["customlabel"] = "Pro-ISIS"
        except ValueError as e:
            print("Labelling Error: row " + str(row) +" " + str(e));
            ret_dic["customlabel"] = "ERROR"
        return ret_dic

    def setMaxTerm(self, maxT):
        self.maxTerm = maxT

    def test(self, maxTerm, searchTerm):

        PATHFILE = "./translated2_test.csv"
        #PATHFILE = "./outputs/results/results.csv"
        #csvBook = pandas.read_csv(PATHFILE, encoding = "ISO-8859-1")

        try:
        #here uncomment this bit
            #scrape.start(searchTerm)
            csvBook = pandas.read_csv(PATHFILE, encoding = "utf-8")
        except:
            print("ERROR")
            logging.error("READ ERROR, unable to read the csv file, likely an error has occured with scraping")
            return

        row = 0
        logging.error("Hashtag: " + searchTerm + "\n")
        rowVar = self.packageRow(csvBook, 0)
        while len(rowVar["tweet"]) != 0:
            if row == maxTerm: break
            print(row)
            logging.error(str(row) + ". Status: " + rowVar["customlabel"])
            logging.error("User: " + rowVar["username"])
            logging.info(rowVar["date"] + ", " + rowVar["time"])
            logging.info("Tweet: " + rowVar["tweet"])
            logging.error("Translated: " + rowVar["translated"] + "\n")
            row = row + 1
            rowVar = self.packageRow(csvBook, row)

# note: socketing is not implemented
# no idea how the stuff that goes into the boxes
# and the buttons would work yet since stub isnt ready
class Tab1(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI();

    def initUI(self):
        # Create first tab
        layout = QVBoxLayout(self)
        hbox1 = QHBoxLayout()
        hbox2 = QHBoxLayout()
        hbox3 = QHBoxLayout()
        hbox4 = QHBoxLayout()
        layout.addLayout(hbox1)
        layout.addLayout(hbox2)
        layout.addLayout(hbox3)
        layout.addLayout(hbox4)

        # first component
        # placeholder component, will find a use for this
        vbox1 = QVBoxLayout()
        buttonLabel = QLabel("Summon")
        execBtn = QPushButton("PyQt5 button")
#        execBtn.clicked.connect(self.dlg.test)
        execBtn.clicked.connect(self.exect)
        vbox1.addWidget(buttonLabel)
        vbox1.addWidget(execBtn)

        # hash tag to be used as search term here
        vbox2 = QVBoxLayout()
        hashLabel = QLabel("Enter Hashtag")
        self.hashInput = QLineEdit()
        self.hashInput.setPlaceholderText("@who")
        vbox2.addWidget(hashLabel)
        vbox2.addWidget(self.hashInput)

        # optional: like the max number of
        # twitter tweets to take from API
        # i assume the API has this option
        vbox3 = QVBoxLayout()
        limitLabel = QLabel("Max Search Term")
        self.limitInput = QLineEdit()
#        limitInput.resize(500,300)
        onlyInt = QIntValidator(1, 9999)
        self.limitInput.setValidator(onlyInt)
        vbox3.addWidget(limitLabel)
        vbox3.addWidget(self.limitInput)


# this is the output display
# to show what tweets are extremis
        vbox4 = QVBoxLayout()
        bufferLabel = QLabel("")
        dlgLabel = QLabel("Readout")
        self.dlg = MyDialog()
        vbox4.addWidget(bufferLabel)
        vbox4.addWidget(dlgLabel)
        vbox4.addWidget(self.dlg)

        hbox2.addLayout(vbox1)
        hbox2.addLayout(vbox2)
        hbox2.addLayout(vbox3)
        hbox4.addLayout(vbox4)

        self.setLayout(layout)

    # calls logger with parameters
    def exect(self):
        inputVal = self.limitInput.text()
        maxTerm = -1
        if len(inputVal) > 0:
            maxTerm = int(inputVal)
        self.dlg.test(maxTerm, self.hashInput.text())


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI();

    def initUI(self):

        self.layout = QVBoxLayout(self)

        # Initialize tab screen
        self.tabs = QTabWidget()

        # a separate widget extracted out for neatness
        self.tab1 = Tab1()
        self.tab2 = QWidget()
        self.tabs.resize(300,200)

        # Add tabs
        self.tabs.addTab(self.tab1, "Search")
        self.tabs.addTab(self.tab2, "Bells")

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

        self.setGeometry(300, 300,470,575)
        self.setWindowTitle('Nyarlathotep Alpha Test')
        # disables resizing
        self.setFixedSize(self.sizeHint())
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

# https://pythonspot.com/pyqt5-tabs/
