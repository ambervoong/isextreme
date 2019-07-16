import relaydata
import visual
import scrape
import sys
import re
import logging
import pandas

from PyQt5.QtWidgets import (
        QWidget,
        QMainWindow,
        QPushButton,
        QApplication,
        QGridLayout,
        QLabel,
        QTabWidget,
        QTableWidget,
        QVBoxLayout,
        QHBoxLayout,
        QLineEdit,
        QPlainTextEdit,
        QDialog,
        QFileDialog,
        QToolButton,
        QProgressBar,
        QComboBox
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

        #self._trial= QPushButton(self)
        #self._trial.setText('Placeholder Button for ?')
        savebutton = QPushButton("Save to CSV")

        layout = QVBoxLayout()
        # Add the new logging box widget to the layout
        layout.addWidget(logTextBox.widget)
        #layout.addWidget(self._trial)
        self.setLayout(layout)
        layout.addWidget(savebutton)

        #test
        self.maxTerm = -1 

        # Connect signal to slot
        #self._trial.clicked.connect(self.trial)
        savebutton.clicked.connect(self.saveFileDialog)


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
        ret_dic["predicted"] = csvVar["predicted"].iloc[row]
        try:
            if (int(ret_dic["predicted"]) == 0):
                ret_dic["customlabel"] = "Not Pro-ISIS"
            else:
                ret_dic["customlabel"] = "Pro-ISIS"
        except ValueError as e:
            print("Labelling Error: row " + str(row) +" " + str(e));
            ret_dic["customlabel"] = "ERROR"
        return ret_dic

    def setMaxTerm(self, maxT):
        self.maxTerm = maxT

    def test(self, maxTerm, searchTerm, pbarData):
        if len(searchTerm) <= 0: return
        PATHFILE = "./outputs/results/results.csv"
        #csvBook = pandas.read_csv(PATHFILE, encoding = "ISO-8859-1")

        pbarData.reset()
        try:
            scrape.start(maxTerm, searchTerm, pbarData)
            csvBook = pandas.read_csv(PATHFILE, encoding="utf-8-sig")
        except:
            print("ERROR")
            logging.error("READ ERROR, unable to read the csv file, likely an error has occured with scraping")
            return

        row = 0
        max_row = len(csvBook["predicted"]) # BUG-FIX for index error
        logging.error("Hashtag: " + searchTerm + "\n")
        rowVar = self.packageRow(csvBook, 0)
        while len(rowVar["tweet"]) != 0:
            if row == maxTerm: break
            if row >= max_row - 1: break # BUG-FIX for index error
            print(row)
            logging.error(str(row) + ". Detection: " + rowVar["customlabel"])
            logging.error("User: " + rowVar["username"] + ", " + rowVar["date"] + ", " + rowVar["time"])
            logging.info("Original: " + rowVar["tweet"])
            logging.error("Translated: " + rowVar["translated"] + "\n")
            row = row + 1
            rowVar = self.packageRow(csvBook, row)
        pbarData.complete()

    def saveFileDialog(self):

        PATHFILE = "./outputs/results/results.csv"
        try:
            csvBook = pandas.read_csv(PATHFILE, encoding="utf-8-sig")
        except Exception as e:
            logging.error(e)

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, extension = QFileDialog.getSaveFileName(self, "Save to File", "",
                        "CSV UTF-8 (*.csv);;All Files (*);;Text Files (*.txt)",
                                                  options=options)
        # Save results.csv to any folder the user chooses
        try:
            extension = re.search('\(([^)]+)', extension).group(1)
            extension = extension.split('*')[1]

            save_to = fileName + extension
            csvBook.to_csv(save_to, encoding='utf-8-sig')
            logging.error("File successfully saved")
        except:
            pass


# note: socketing is not implemented
# no idea how the stuff that goes into the boxes
# and the buttons would work yet since stub isnt ready
class Tab1(QWidget):
    def __init__(self, pbarData):
        super().__init__()
        pbarData.registerObserver(self)
        self.pbarData = pbarData
        self.initUI();

    def initUI(self):
        # Create first tab
        layout = QVBoxLayout(self)
        hbox1 = QHBoxLayout()
        hbox2 = QHBoxLayout()
        hbox3 = QHBoxLayout()
        hbox4 = QHBoxLayout()
        hbox5 = QHBoxLayout()
        layout.addLayout(hbox1)
        layout.addLayout(hbox2)
        layout.addLayout(hbox3)
        layout.addLayout(hbox4)
        layout.addLayout(hbox5)

        # first component

        vbox1 = QHBoxLayout()
        #buttonLabel = QLabel("Scrape & Analyse")
        execBtn = QPushButton("Search")
        #execBtn.setStyleSheet(  "background-position: bottom;");

        #        execBtn.clicked.connect(self.dlg.test)
        execBtn.clicked.connect(self.exect)
        #vbox1.addWidget(buttonLabel)
        vbox1.addWidget(execBtn)

        # search term to be used as search term here
        vbox2 = QHBoxLayout()
        hashLabel = QLabel("Enter Search Term")
        self.hashInput = QLineEdit()
        self.hashInput.setPlaceholderText("#_____")
        vbox2.addWidget(hashLabel)
        vbox2.addWidget(self.hashInput)

        # optional: like the max number of
        # twitter tweets to take from API
        vbox3 = QHBoxLayout()
        limitLabel = QLabel("Max Searches")
        self.limitInput = QLineEdit()
#        limitInput.resize(500,300)
        onlyInt = QIntValidator(1, 9999)
        self.limitInput.setValidator(onlyInt)
        self.limitInput.setPlaceholderText("20")
        vbox3.addWidget(limitLabel)
        vbox3.addWidget(self.limitInput)

        #vbox5 = QVBoxLayout()

        # this is the output display
        # to show what tweets
        vbox4 = QVBoxLayout()
        bufferLabel = QLabel("")
        dlgLabel = QLabel("Readout")
        self.dlg = MyDialog()
        vbox4.addWidget(bufferLabel)
        vbox4.addWidget(dlgLabel)
        vbox4.addWidget(self.dlg)

        self.pbar = QProgressBar(self)
        self.step = 0
        hbox5.addWidget(self.pbar)

        hbox2.addLayout(vbox2)
        hbox2.addLayout(vbox3)
        hbox2.addLayout(vbox1)
        hbox4.addLayout(vbox4)

        self.setLayout(layout)

    # calls logger with parameters
    def exect(self):
        inputVal = self.limitInput.text()
        maxTerm = int(self.limitInput.text())
        if len(inputVal) > 0:
            maxTerm = int(inputVal)
        self.dlg.test(maxTerm, self.hashInput.text(), self.pbarData)

    def update(self, pbarData):
        self.step = pbarData.progressReport()
        self.pbar.setValue(self.step)

class Tab2(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI();

    def initUI(self):
        # Create first tab
        layout = QVBoxLayout(self)
        hbox1 = QHBoxLayout()
        #layout.addLayout(hbox1)

        vbox1 = QHBoxLayout()
        vbox2 = QVBoxLayout()
        vbox3 = QVBoxLayout()

        # buttonLabel = QLabel("Scrape & Analyse")
        self.mcBox = QComboBox() # Multiple Choice Box
        self.mcBox.addItem("WordCloud")
        self.mcBox.addItem("Generic Graph")

        execBtn = QPushButton("Generate")
        execBtn.clicked.connect(self.generate)

        #saveBtn = QPushButton("Save Plot")
        #saveBtn.clicked.connect(self.savePlot)
        vbox1.addWidget(self.mcBox)
        vbox1.addWidget(execBtn)

        self.canvas = visual.PlotCanvas(self, width=5, height=4)
        vbox2.addWidget(self.canvas)
        #vbox3.addWidget(saveBtn)
        layout.addLayout(vbox1)
        layout.addLayout(vbox2)
        layout.addLayout(vbox3)
        self.setLayout(layout)

    def generate(self):
        type = int(self.mcBox.currentIndex())
        # Ensures that the previous plot is removed
        self.canvas.figure.clear()

        if type == 0: # WordCloud
            self.canvas.plotWord()
        elif type == 1:
            self.canvas.plotFreq()
        self.show()

    def savePlot(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, extension = QFileDialog.getSaveFileName(self, "Save to File", "",
                                                          "PNG (*.png);;All Files (*);;Text Files (*.txt)",
                                                          options=options)
        # Save plot to any folder the user chooses
        try:
            extension = re.search('\(([^)]+)', extension).group(1)
            extension = extension.split('*')[1]

            save_to = fileName + extension

            self.canvas.figure.savefig(save_to, facecolor='k', bbox_inches='tight')
            logging.error("Plot successfully saved")
        except:
            pass

class Tab3(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI();

    def initUI(self):
        # Create first tab
        layout = QVBoxLayout(self)
        hbox1 = QHBoxLayout()


        vbox1 = QHBoxLayout()


        tableBox = QTableWidget(5,7, self)

        #saveBtn = QPushButton("Save Plot")
        #saveBtn.clicked.connect(self.savePlot)
        vbox1.addWidget(tableBox)


        layout.addLayout(vbox1)

        self.setLayout(layout)


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI();

    def initUI(self):

        self.layout = QVBoxLayout(self)

        # Initialize tab screen
        self.tabs = QTabWidget()

        # a separate widget extracted out for neatness
        pbarData = relaydata.ProgressRelay()
        self.tab1 = Tab1(pbarData)
        self.tab2 = Tab2()
        #self.tab3 = Tab3()
        self.tabs.resize(700,600)

        # Add tabs
        self.tabs.addTab(self.tab1, "Search")
        self.tabs.addTab(self.tab2, "Graphs")
        #self.tabs.addTab(self.tab3, "QuickView")

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

        self.setGeometry(600, 200, 870, 975)
        self.setWindowTitle('Nyarlathotep Alpha Test')
        # disables resizing
        self.setFixedSize(self.sizeHint())
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

# https://pythonspot.com/pyqt5-tabs/
