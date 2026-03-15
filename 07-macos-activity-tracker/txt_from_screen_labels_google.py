import os
import csv
import datetime
import gensim.downloader as api
from gensim.models import KeyedVectors

# Load the Google News word2vec model
word_vectors = api.load("word2vec-google-news-300")

def read_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    return content

def process_files_in_folder(folder_path):
    file_texts = []

    for file_name in os.listdir(folder_path):
        if file_name.endswith(".txt"):
            file_path = os.path.join(folder_path, file_name)
            content = read_text_file(file_path)
            file_texts.append(content)

    return file_texts

def get_most_similar_label(text, labels):
    tokens = [token for token in text.lower().split() if token in word_vectors]
    max_similarity = -1
    most_similar_label = ''
    confidence = 0

    for label in labels:
        label_tokens = [token for token in label.lower().split() if token in word_vectors]

        if not tokens or not label_tokens:
            continue

        similarity = word_vectors.n_similarity(tokens, label_tokens)

        if similarity > max_similarity:
            max_similarity = similarity
            most_similar_label = label
            confidence = similarity

    return most_similar_label, confidence

def assign_labels_to_texts(texts, label_categories):
    assigned_labels = []

    for text in texts:
        labels = {}
        for category, label_set in label_categories.items():
            most_similar_label, confidence = get_most_similar_label(text, label_set)
            labels[category] = most_similar_label
            labels[f"{category}_confidence"] = confidence

        assigned_labels.append(labels)

    return assigned_labels

def save_to_csv(assigned_labels, output_file):
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = list(assigned_labels[0].keys())
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for labels in assigned_labels:
            writer.writerow(labels)

current_date = datetime.datetime.now().strftime("%Y-%m-%d")
folder_path = f'text_from_screen/{current_date}'
output_file = 'labeled_information_google.csv'

# Define your label categories and corresponding labels
label_categories = {
    'time_period':['By end of the week', 'By end of the month', 'By end of the year', 'By end of the decade', 'Before I die'],
    'priority':['High', 'Medium', 'Low'],
    'category':['Health', 'Wealth', 'Relationship', 'Career', 'Personal Growth', 'Spirituality', 'Social Life', 'Family', 'Fun & Recreation', 'Contribution'],
    'genre':['Creative', 'Analytical', 'Physical', 'Social', 'Adventurous', 'Intellectual', 'Emotional', 'Spiritual', 'Financial', 'Environmental', 'Occupational', 'Relationship', 'Health'],
    'medium':['Book', 'Article', 'Video', 'Podcast', 'Documentary', 'Movie', 'TV Show', 'Course'],
    'goal':['Learn', 'Do', 'Be'],
    'goal_type':['Habit', 'Project', 'Event'],
    'goal_status':['Not Started', 'In Progress', 'Completed', 'Abandoned'],
    'goal_relationship':['Parent', 'Sibling', 'Friend'],
    'goal_relationship_status':['Not Started', 'In Progress', 'Completed', 'Abandoned'],
    'use_case':['Goal tracking', 'Habit tracking', 'Project management', 'Self-improvement', 'Time management', 'Productivity'],
    'topic':['Personal Development', 'Education', 'Career', 'Health', 'Relationships', 'Wealth', 'Spirituality', 'Social Life', 'Family', 'Fun & Recreation', 'Contribution'],
    'platform':['Web', 'iOS', 'Android', 'Mac', 'Windows', 'Linux', 'Cross-platform', 'Command Line'],
    'device':['Phone', 'Tablet', 'Laptop', 'Desktop', 'Smartwatch'],
    'target_audience':['Students', 'Professionals', 'Entrepreneurs', 'Parents', 'Self-employed', 'Self-learners', 'People in need'],
    'framework':['Python', 'JavaScript', 'React', 'Vue', 'Angular', 'Django', 'Flask', 'Node.js', 'Express', 'Ruby on Rails', 'Laravel', 'Spring', 'Flask', 'Django', 'Rails'],
    'language':['Python', 'JavaScript', 'Java', 'C', 'C++', 'C#', 'PHP', 'Ruby', 'Go', 'Swift', 'Kotlin', 'Rust', 'TypeScript'],
}

file_texts = process_files_in_folder(folder_path)
assigned_labels = assign_labels_to_texts(file_texts, label_categories)
save_to_csv(assigned_labels, output_file)
