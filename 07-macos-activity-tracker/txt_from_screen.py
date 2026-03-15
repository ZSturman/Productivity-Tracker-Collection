import pytesseract
from PIL import ImageGrab
import spacy
from datetime import datetime
import os
from screeninfo import get_monitors
import plistlib

with open('/Users/zacharysturman/scripts/productivity_tracker/com.zacharysturman.productivity_macbook.plist', 'rb') as plist_file:
    plist_data = plistlib.load(plist_file)

pytesseract.pytesseract.tesseract_cmd = plist_data['TesseractCommandPath']

# Load the English language model in spaCy
nlp = spacy.load("en_core_web_sm")

def capture_screenshot():
    left = top = right = bottom = None
    for monitor in get_monitors():
        if left is None:
            left = monitor.x
        else:
            left = min(left, monitor.x)
        if top is None:
            top = monitor.y
        else:
            top = min(top, monitor.y)
        if right is None:
            right = monitor.x + monitor.width
        else:
            right = max(right, monitor.x + monitor.width)
        if bottom is None:
            bottom = monitor.y + monitor.height
        else:
            bottom = max(bottom, monitor.y + monitor.height)

    return ImageGrab.grab(bbox=(left, top, right, bottom))

def extract_text_from_image(image):
    return pytesseract.image_to_string(image)


def analyze_text(text):
    doc = nlp(text)
    labels = []

    for token in doc:
        if token.pos_ == 'NOUN':
            labels.append(token.text)
    
    return labels

def named_entity(text):
    doc = nlp(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return entities

def pos_tagging(text, pos_tag):
    doc = nlp(text)
    words = [token.text for token in doc if token.pos_ == pos_tag]
    return words

def dependency_parsing(text, relation=None):
    doc = nlp(text)
    if relation:
        pairs = [(token.head.text, token.text) for token in doc if token.dep_ == relation]
    else:
        pairs = [(token.head.text, token.text, token.dep_) for token in doc]
    return pairs

def extract_verbs(text):
    doc = nlp(text)
    verbs = [token.text for token in doc if token.pos_ == 'VERB']
    return verbs


def save_text_to_file(text, labels, entities, words, subject_verb_pairs, object_verb_pairs, verbs):
    # Get the current date and time in the desired format
    current_datetime = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    current_date = datetime.now().strftime('%Y-%m-%d')

    #base_dir = '/Users/zacharysturman/data_collection/text_from_screen/'
    base_dir = '/Users/zacharysturman/Library/Mobile Documents/com~apple~CloudDocs/Data_collection/csv_and_txt_from_screen_macbook/text_from_screen/'
    date_dir = os.path.join(base_dir, current_date)

    if not os.path.exists(date_dir):
        os.makedirs(date_dir)

    file_name = f"text_{current_datetime}.txt"
    file_path = os.path.join(date_dir, file_name)

    # Save the text and outputs of other functions to the file
    with open(file_path, 'w', encoding='utf-8') as file:
        print(  "Writing to file...")
        file.write("Extracted Text:\n")
        file.write(text)
        file.write("\n\nAnalyzed Text (Nouns):\n")
        file.write(', '.join(labels))
        file.write("\n\nNamed Entities:\n")
        for ent in entities:
            file.write(f"{ent[0]} ({ent[1]})\n")
        file.write("\n\nPOS Tagging (Nouns):\n")
        file.write(', '.join(words))
        file.write("\n\nDependency Parsing (Subject-Verb Pairs):\n")
        for pair in subject_verb_pairs:
            file.write(f"{pair[0]} -> {pair[1]}\n")
        file.write("\n\nDependency Parsing (Object-Verb Pairs):\n")
        for pair in object_verb_pairs:
            file.write(f"{pair[0]} -> {pair[1]}\n")
        file.write("\n\nExtracted Verbs:\n")
        file.write(', '.join(verbs))


def run_txt_from_screen():
    # Capture the screenshot
    image = capture_screenshot()

    # Extract text from the screenshot
    text = extract_text_from_image(image)

    # Analyze the text (extract nouns)
    labels = analyze_text(text)

    # Get named entities
    entities = named_entity(text)

    # Perform POS tagging for nouns
    words = pos_tagging(text, 'NOUN')

    # Perform dependency parsing for 'nsubj' relations (subject-verb pairs)
    subject_verb_pairs = dependency_parsing(text, 'nsubj')

    # Perform dependency parsing for 'dobj' relations (object-verb pairs)
    object_verb_pairs = dependency_parsing(text, 'dobj')

    # Extract verbs from the text
    verbs = extract_verbs(text)

    # Save the text and function outputs to a file with the current date and time
    save_text_to_file(text, labels, entities, words, subject_verb_pairs, object_verb_pairs, verbs)