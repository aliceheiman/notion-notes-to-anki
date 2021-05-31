# import the main window object (mw) from aqt
from aqt import mw
# import the "show info" tool from utils.py
from aqt.utils import showInfo, showText, qconnect
# import all of the Qt GUI library
from aqt.qt import *

import random

__window = None

class NotesWindow(QWidget):

    # main window of notes plugin
    def __init__(self):
        super(NotesWindow, self).__init__()

        self.hello = ["Hallo Welt", "Hei maailma", "Hola Mundo", "Привет мир"]
        self.initGUI()

    # create GUI skeleton
    def initGUI(self):

        self.button = QPushButton("Import Deck", self)
        self.text = QLabel("Hello World", alignment=Qt.AlignCenter)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)

        self.button.clicked.connect(self.magic)

        # go, baby go!
        self.setMinimumWidth(500)
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.setWindowTitle("Import Notion Notes")
        self.resize(self.minimumSizeHint())
        self.show()

    def magic(self):
        self.text.setText(random.choice(self.hello))

def testFunction() -> None:
    # get the number of cards in the current collection, which is stored in
    # the main window
    cardCount = mw.col.cardCount()
    # show a message box
    showInfo("Card count: %d" % cardCount)

# plugin was called from Anki
def runNotesPlugin():
    global __window
    __window = NotesWindow()


# create a new menu item
action = QAction("Import Notion Notes", mw)
# set it to call testFunction when it's clicked
qconnect(action.triggered, runNotesPlugin)
# and add it to the tools menu
mw.form.menuTools.addAction(action)
