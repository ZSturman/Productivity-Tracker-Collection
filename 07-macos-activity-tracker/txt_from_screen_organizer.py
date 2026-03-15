import os
import csv
import re
import datetime

def read_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    return content

def extract_data_from_content(content):
    sections = content.split('\n\n')

    extracted_data = {
        'text': sections[1].replace("Extracted Text:\n", "").strip(),
        'nouns': sections[2].replace("Analyzed Text (Nouns):\n", "").strip(),
        'named_entities': sections[3].replace("Named Entities:\n", "").strip(),
        'pos_tagging': sections[4].replace("POS Tagging (Nouns):\n", "").strip(),
        'subject_verb_pairs': sections[5].replace("Dependency Parsing (Subject-Verb Pairs):\n", "").strip(),
        'object_verb_pairs': sections[6].replace("Dependency Parsing (Object-Verb Pairs):\n", "").strip(),
        'verbs': sections[7].replace("Extracted Verbs:\n", "").strip()
    }

    return extracted_data

def organize_information(folder_path):
    data_list = []
    
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".txt"):
            file_path = os.path.join(folder_path, file_name)
            content = read_text_file(file_path)
            data = extract_data_from_content(content)
            data_list.append(data)
    
    return data_list

def save_to_csv(data_list, output_file):
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['text', 'nouns', 'named_entities', 'pos_tagging', 'subject_verb_pairs', 'object_verb_pairs', 'verbs']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for data in data_list:
            writer.writerow(data)

current_date = datetime.datetime.now().strftime("%Y-%m-%d")
folder_path = f'text_from_screen/{current_date}'
output_file = 'organized_information.csv'

data_list = organize_information(folder_path)
save_to_csv(data_list, output_file)
