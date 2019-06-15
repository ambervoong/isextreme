import sys;
import logging;

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
        logTextBox.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logging.getLogger().addHandler(logTextBox)
        # You can control the logging level
        logging.getLogger().setLevel(logging.DEBUG)

        self._button = QPushButton(self)
        self._button.setText('Test Me')

        layout = QVBoxLayout()
        # Add the new logging box widget to the layout
        layout.addWidget(logTextBox.widget)
        layout.addWidget(self._button)
        self.setLayout(layout)

        # Connect signal to slot
        self._button.clicked.connect(self.test)

    def test(self):
        logging.debug('damn, a bug')
        logging.info('something to remember')
        logging.warning('that\'s not right')
        logging.error('foobar')


# note: socketing is not implemented
# no idea how the stuff that goes into the boxes
# and the buttons would work yet since stub isnt ready
class Tab1(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI();

    def initUI(self):
        # Create first tab
        #layout = QGridLayout(self)
        layout = QVBoxLayout(self)
        hbox1 = QHBoxLayout()
        hbox2 = QHBoxLayout()
        hbox3 = QHBoxLayout()
        layout.addLayout(hbox1)
        layout.addLayout(hbox2)
        layout.addLayout(hbox3)

        # first component
        # placeholder component, will find a use for this
        vbox1 = QVBoxLayout()
        buttonLabel = QLabel("Summon")
        execBtn = QPushButton("PyQt5 button")
        vbox1.addWidget(buttonLabel)
        vbox1.addWidget(execBtn)

        # hash tag to be used as search term here
        vbox2 = QVBoxLayout()
        hashLabel = QLabel("Enter Hashtag")
        hashInput = QLineEdit()
        hashInput.setPlaceholderText("@who")
        vbox2.addWidget(hashLabel)
        vbox2.addWidget(hashInput)

        # optional: like the max number of
        # twitter tweets to take from API
        # i assume the API has this option
        vbox3 = QVBoxLayout()
        limitLabel = QLabel("Max Search Term")
        limitInput = QLineEdit()
#        limitInput.resize(500,300)
        onlyInt = QIntValidator(1, 9999)
        limitInput.setValidator(onlyInt)
        vbox3.addWidget(limitLabel)
        vbox3.addWidget(limitInput)

# this is the output display
# to show what tweets are extremis
        vbox4 = QVBoxLayout()
        bufferLabel = QLabel("")
        dlgLabel = QLabel("Readout")
        dlg = MyDialog()
        vbox4.addWidget(bufferLabel)
        vbox4.addWidget(dlgLabel)
        vbox4.addWidget(dlg)


        hbox2.addLayout(vbox1)
        hbox2.addLayout(vbox2)
        hbox2.addLayout(vbox3)
        hbox3.addLayout(vbox4)

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
