# import the main window object (mw) from aqt
from aqt import mw
# import the "show info" tool from utils.py
from aqt.utils import showInfo, showText, qconnect
# import all of the Qt GUI library
from aqt.qt import *

import re, random

__window = None

# add custom model if needed


def addCustomModel(name, col):

    # create custom model for imported deck
    mm = col.models
    existing = mm.byName("Basic Test")
    if existing:
        fields = mm.fieldNames(existing)
        if "Front" in fields and "Back" in fields:
            return existing
        else:
            existing['name'] += "-" + 'test'
            mm.save(existing)
    m = mm.new("Basic Test")

    # add fields
    mm.addField(m, mm.newField("Front"))
    mm.addField(m, mm.newField("Back"))
    mm.addField(m, mm.newField("Add Reverse"))

    # add cards
    t = mm.newTemplate("Normal")

    # front
    t['qfmt'] = "{{Front}}"
    t['afmt'] = "{{FrontSide}}\n\n<hr id=answer>\n\n{{Back}}"
    mm.addTemplate(m, t)

    # back
    t = mm.newTemplate("Reverse")
    t['qfmt'] = "{{#Add Reverse}}{{Back}}{{/Add Reverse}}"
    t['afmt'] = "{{FrontSide}}\n\n<hr id=answer>\n\n{{Front}}"
    mm.addTemplate(m, t)

    mm.add(m)
    return m

class NotesWindow(QWidget):

    # main window of notes plugin
    def __init__(self):
        super(NotesWindow, self).__init__()

        self.hello = ["Hallo Welt", "Hei maailma", "Hola Mundo", "Привет мир"]

        self.deckNames = mw.col.decks.allNames()

        self.initGUI()

    # create GUI skeleton
    def initGUI(self):

        self.description = QLabel("Paste to import below", alignment=Qt.AlignCenter)
        self.description.setStyleSheet("font-weight: bold")

        self.text = QLabel("Import Notes to Deck:")
        self.deckSelection = QComboBox()
        self.deckSelection.addItems(self.deckNames)
        self.deckSelection.view().setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        self.notes = QTextEdit("", self)
        self.button = QPushButton("Create Cards", self)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.description)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.deckSelection)
        self.layout.addWidget(self.notes)
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)

        self.button.clicked.connect(self.createCards)

        # go, baby go!
        self.setMinimumWidth(500)
        self.setMinimumHeight(500)
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.setWindowTitle("Import Notion Notes")
        self.resize(self.minimumSizeHint())
        self.show()

    def createCards(self):

        def ankify(text):
            text = text.replace('\n', '<br>')
            text = re.sub(r'\*(.+?)\*', r'<b>\1</b>', text)
            return text

        deckName = self.deckSelection.currentText()
        deck = mw.col.decks.get(mw.col.decks.id(deckName))
        model = addCustomModel('Notion', mw.col)

        # assign custom model to new deck
        mw.col.decks.select(deck["id"])
        mw.col.decks.save(deck)

        # assign new deck to custom model
        mw.col.models.setCurrent(model)
        model["did"] = deck["id"]
        mw.col.models.save(model)

        #self.text.setText(self.notes.toPlainText())
        notes = self.notes.toPlainText().split('\n')

        # check for at least one question and answer
        if len(notes) < 2: return

        # Creating notes
        self.description.setText(f'Converting notes into anki cards...')

        for i in range(0, len(notes), 2):
            # check if there is an answer to the question
            if i + 1 >= len(notes): break

            # create a new note
            card = mw.col.newNote()
            card["Front"] = ankify(notes[i])
            card["Back"] = ankify(notes[i + 1])

            mw.col.addNote(card)

        self.description.setText(f'Success! Imported {len(notes) // 2} cards.')

        mw.col.reset()
        mw.reset()






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
