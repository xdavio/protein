import sys
from PyQt4 import QtGui

class mainwin(QtGui.QWidget):

    def __init__(self):
        super(mainwin, self).__init__()

        self.initUI()

    def initUI(self):
        okButton = QtGui.QPushButton("Krunch")
        resetButton = QtGui.QPushButton("Reset")

        #labels
        lblfilepath = QtGui.QLabel('Excel/CSV:', self)
        lblquery = QtGui.QLabel('Query:', self)
        lblnumrange = QtGui.QLabel('Number Range:', self)
        lbldayrange = QtGui.QLabel('Day Range:', self)
        lblfirstcol = QtGui.QLabel('First Data Col:', self)
        lbllastcol = QtGui.QLabel('Last Data Col:', self)
        lbldebug = QtGui.QLabel('Debug Dump?', self)

        #buttons
        buttonfilepath = QtGui.QPushButton("Select")
        buttonfilepath.clicked.connect(self.selectExcel)
        buttonquery = QtGui.QPushButton("Select")
        buttonquery.clicked.connect(self.selectQuery)

        #combo boxes
        combonumrange = QtGui.QComboBox(self)
        combonumrange.addItem("Average")
        combonumrange.addItem("First")
        combonumrange.addItem("Last")
        combonumrange.addItem("Min")
        combonumrange.addItem("Max")

        combodayrange = QtGui.QComboBox(self)
        combodayrange.addItem("Average")
        combodayrange.addItem("Ignore Days")

        #file dialog actions
        openExcel = QtGui.QAction(QtGui.QIcon('open.png'), 'Select', self)
        openQuery = QtGui.QAction(QtGui.QIcon('open.png'), 'Select', self)        

        #build horizontal components
        barfilepath = QtGui.QHBoxLayout()
        barfilepath.addWidget(lblfilepath)
        barfilepath.addWidget(buttonfilepath)
        
        barquery = QtGui.QHBoxLayout()
        barquery.addWidget(lblquery)
        barquery.addWidget(buttonquery)        
        
        barnumrange = QtGui.QHBoxLayout()
        barnumrange.addWidget(lblnumrange)
        barnumrange.addWidget(combonumrange)
        
        bardayrange = QtGui.QHBoxLayout()
        bardayrange.addWidget(lbldayrange)
        bardayrange.addWidget(combodayrange)
        
        barfirstcol = QtGui.QHBoxLayout()
        barfirstcol.addWidget(lblfirstcol)
        
        barlastcol = QtGui.QHBoxLayout()
        barlastcol.addWidget(lbllastcol)
        
        bardebug = QtGui.QHBoxLayout()
        bardebug.addWidget(lbldebug)

        lowbar = QtGui.QHBoxLayout()
        lowbar.addStretch(1)
        lowbar.addWidget(okButton)
        lowbar.addWidget(resetButton)

        
        vbox = QtGui.QVBoxLayout()
        vbox.addLayout(barfilepath)
        vbox.addLayout(barquery)
        vbox.addLayout(barnumrange)
        vbox.addLayout(bardayrange)
        vbox.addLayout(barfirstcol)
        vbox.addLayout(barlastcol)
        vbox.addLayout(bardebug)
        vbox.addLayout(lowbar)

        self.setLayout(vbox)

        self.setWindowTitle("Title")
        self.show()

    def selectExcel(self):
        self.fp = QtGui.QFileDialog.getOpenFileName()

    def selectQuery(self):
        self.qu = QtGui.QFileDialog.getOpenFileName()


def main():
    app = QtGui.QApplication(sys.argv)
    m = mainwin()
    sys.exit(app.exec_())    

if __name__ == "__main__":
    main()
