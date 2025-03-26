import genanki, random
from wanikani import getNoteData
from SETTINGS import TIME_DELTA

# fmt: off
# generate suitable ids once then hardcode them
# print(random.randrange(1 << 30, 1 << 31))


# import card style from cards.css
card_style = ""
with open("cards.css", "r") as file:
    card_style = file.read().strip()


# import kanji script from kanji.js
kanji_script = ""
with open("kanji.js", "r") as file:
    kanji_script = file.read().strip()


# radical card question for anki
radical_question = """
Name this Radical.
<div class="subject radical">{{subject}}</div>
""".strip()

# radical card answer for anki
radical_answer = """
{{FrontSide}}
<hr />
<div class="main-row"><span class="info">name: </span>{{meaning}}</div>
<div class="mnemonic">{{mnemonic}}</div>
""".strip()

# radical note anki model
radical_model = genanki.Model(
    1827008493,  # model ID
    "WaniKani-Radical",  # model name
    fields=[
        {"name": "subject"},
        {"name": "meaning"},
        {"name": "mnemonic"}],
    templates=[
        {
            "name": "Radical-Quiz",
            "qfmt": radical_question,
            "afmt": radical_answer
        }
    ],
    css=card_style,
)


# vocabulary card question for anki
vocabulary_question = """
Name and read this Vocabulary.
<div class="subject vocabulary">{{subject}}</div>
""".strip()

# vocabulary card answer for anki
vocabulary_answer = """
{{FrontSide}}<hr />

<div class="main-row">
  <span class="info">meaning:</span>
  <span class="primary">{{primary_meaning}}</span>
  <span class="other">{{other_meanings}}</span>
</div>
<div class="mnemonic">{{meaning_mnemonic}}</div><hr />

<div class="main-row">
  <span class="info">reading:</span>
  <span class="primary">{{primary_reading}}</span>
  <span class="other">{{other_readings}}</span>
</div>
<div class="mnemonic">{{reading_mnemonic}}</div>
""".strip()

# vocabulary model for anki
vocabulary_model = genanki.Model(
    1892872892,  # model ID
    "WaniKani-Vocabulary",  # model name
    fields=[
        {"name": "subject"},

        # meaning section in anki note
        {"name": "primary_meaning"},
        {"name": "other_meanings"}, 
        {"name": "meaning_mnemonic"},

        # reading section in anki note
        {"name": "primary_reading"},
        {"name": "other_readings"}, 
        {"name": "reading_mnemonic"}
    ],
    templates=[
        {
            "name": "Vocabulary-Quiz",
            "qfmt": vocabulary_question,
            "afmt": vocabulary_answer
        }
    ],
    css=card_style,
)


# kanji card question for anki
kanji_question = """
Name and read this Kanji.
<div class="subject kanji">{{subject}}</div>
""".strip()

# kanji card answer for anki
kanji_answer = """
{{FrontSide}}<hr />

<div class="main-row">
  <span class="info">meaning:</span>
  <span class="primary">{{primary_meaning}}</span>
  <span class="other">{{other_meanings}}</span>
</div>
<div class="mnemonic">{{meaning_mnemonic}}</div><hr />

<div class="main-row">
  <div class="sub-row" id="onyomi">
    <span class="info">on-reading:</span>
    <span class="primary">{{primary_reading_on}}</span>
    <span class="other">{{other_readings_on}}</span>
  </div>
  <div class="sub-row" id="kunyomi">
    <span class="info">kun-reading:</span>
    <span class="primary">{{primary_reading_kun}}</span>
    <span class="other">{{other_readings_kun}}</span>
  </div>
</div>
<div class="mnemonic">{{reading_mnemonic}}</div><hr />

<div class="main-row aligned" id="similar">
  <span class="info">similar kanji:</span>
  <span class="links"></span>
</div>
""".strip()

# add kanji script to answer part of card
kanji_answer += f"<script>{kanji_script}</script>"

# kanji note anki model
kanji_model = genanki.Model(
    2100118601,  # model ID
    "WaniKani-Kanji",  # model name
    fields=[
        {"name": "subject"},

        # meanings section in anki note
        {"name": "primary_meaning"},
        {"name": "other_meanings"}, 
        {"name": "meaning_mnemonic"},

        # readings section in anki note
        {"name": "primary_reading_on"},
        {"name": "other_readings_on"}, 
        {"name": "primary_reading_kun"},
        {"name": "other_readings_kun"},
        {"name": "reading_mnemonic"},

        # similar kanji section in anki note
        {"name": "similar_characters"},
        {"name": "similar_meanings"}
    ],
    templates=[
        {
            "name": "Kanji-Quiz",
            "qfmt": kanji_question,
            "afmt": kanji_answer
        }
    ],
    css=card_style,
)


# Finds primary item that matches condition
def getPrimary(items, cond=(lambda item: True)):
    for item in items:
        if item["primary"] and cond(item): return item

    return {}


# Finds other items that match condition
def getOthers(items, cond=(lambda item: True)):
    other = []
    for item in items:
        if not item["primary"] and cond(item): other.append(item)

    return other


# Returns both primary and other meanings / readings
# Pass data_type="meaning" or data_type="reading"
def extractNoteData(note, data_type, reading_type=None):
    condition = lambda item: item["type"] == reading_type
    if not reading_type: condition = lambda item: True

    primary = getPrimary(note[data_type+"s"], condition).get(data_type, "")
    others = getOthers(note[data_type+"s"], condition)
    others = ", ".join(reading[data_type] for reading in others)

    return primary, others


# Formats radical note data as needed for Anki
def processRadical(note):
    meaning = getPrimary(note["meanings"])['meaning']
    return [note["subject"], meaning, note["meaning_mnemonic"]]


# Formats kanji note data as needed for Anki
def processKanji(note):
    meaning_primary, meaning_others = extractNoteData(note, "meaning")
    onyomi_primary, onyomi_others = extractNoteData(note, "reading", "onyomi")
    kunyomi_primary, kunyomi_others = extractNoteData(note, "reading", "kunyomi")
    
    return [
        note["subject"],

        # meaning section on the anki note
        meaning_primary, meaning_others,
        note["meaning_mnemonic"],

        # reading section on the anki note
        onyomi_primary, onyomi_others,
        kunyomi_primary, kunyomi_others,
        note["reading_mnemonic"],

        # similar kanji section on the anki note
        ", ".join(kanji["character"] for kanji in note["similar_kanji"]),
        ", ".join(kanji["meaning"] for kanji in note["similar_kanji"]),
    ]


# Formats vocabulary note data as needed for Anki
def processVocabulary(note):
    meaning_primary, meaning_others = extractNoteData(note, "meaning")
    reading_primary, reading_others = extractNoteData(note, "reading")

    return [
        note["subject"],

        # meaning section on the anki note
        meaning_primary, meaning_others,
        note["meaning_mnemonic"],

        # reading section on the anki note
        reading_primary, reading_others,
        note["reading_mnemonic"],
    ]


# Uses one of the above processors to format note data
def processNote(note_data): 
    processors = {
        "radical": processRadical,
        "kanji": processKanji,
        "vocabulary": processVocabulary
    }
    return processors[note_data["type"]](note_data)


# Returns a Anki note of given type with given fields
def createNote(type, fields):
    models = {
        "radical": radical_model,
        "kanji": kanji_model,
        "vocabulary": vocabulary_model
    }
    return genanki.Note(model=models[type], fields=fields)


# Adds Anki notes as described in deck_data
def processDeck(deck, deck_data):
    for note_data in deck_data:
        fields = processNote(note_data)
        note = createNote(note_data["type"], fields)

        deck.add_note(note)
        

# Creates a ready to import Anki deck file
def createDeckFile(delta=24):
  deck = genanki.Deck(
      1218215477,  # deck ID
      "WaniKani - Recent Mistakes",  # deck name
  )

  deck_data = getNoteData(delta)
  print(f"Number of recent mistakes: {len(deck_data)}")

  processDeck(deck, deck_data)
  genanki.Package(deck).write_to_file("IMPORTME.apkg")


# call this to create recent mistakes anki deck
createDeckFile(TIME_DELTA)
