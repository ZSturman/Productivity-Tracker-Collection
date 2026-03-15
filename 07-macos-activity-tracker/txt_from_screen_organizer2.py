import spacy
import os
import csv
import datetime

nlp = spacy.load("en_core_web_sm")

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
    doc1 = nlp(text)
    max_similarity = -1
    most_similar_label = ''

    for label in labels:
        doc2 = nlp(label)
        similarity = doc1.similarity(doc2)

        if similarity > max_similarity:
            max_similarity = similarity
            most_similar_label = label

    return most_similar_label

def assign_labels_to_texts(texts, label_categories):
    assigned_labels = []

    for text in texts:
        labels = {}
        for category, label_set in label_categories.items():
            most_similar_label = get_most_similar_label(text, label_set)
            labels[category] = most_similar_label

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
output_file = 'labeled_information.csv'

# Define your label categories and corresponding labels
label_categories = {
    'timeframe': {
        'time_period': ['Within 24 hours', 'Within 48 hours', 'Within a week', 'Within a month', 'Within 6 months', 'Within a year', 'Within 5 years', 'Lifetime'],
        'priority': ['Obligation', "When there's time", 'Low', 'Urgent', 'Important', 'Nice to have'],
        'goal_difficulty': ['Easy', 'Moderate', 'Hard', 'Very Hard'],
        },
    'area_of_life': {
        'category': ['Health', 'Wealth', 'Relationship', 'Career', 'Personal Growth', 'Spirituality', 'Social Life', 'Family', 'Fun & Recreation', 'Contribution', 'Environment', 'Education', 'Civic Engagement'],
        'subcategory': ['Physical Health', 'Mental Health', 'Emotional Health', 'Financial Health', 'Spiritual Health', 'Professional Growth', 'Hobbies & Interests', 'Travel & Exploration', 'Philanthropy', 'Community Involvement', 'Eco-Friendly Living', 'Sustainable Practices', 'Formal Education', 'Informal Education', 'Continuing Education', 'Volunteering', 'Political Advocacy', 'Human Rights'],
        },
    'content': {
        'medium': ['Book', 'Article', 'Video', 'Podcast', 'Documentary', 'Movie', 'TV Show', 'Course', 'Blog', 'Online Course', 'Seminar', 'Workshop', 'Conference', 'Webinar', 'Live Stream', 'Infographic'],
        'genre': ['Creative', 'Analytical', 'Physical', 'Social', 'Adventurous', 'Intellectual', 'Emotional', 'Spiritual', 'Financial', 'Environmental', 'Occupational', 'Relationship', 'Health', 'Artistic', 'Musical', 'Dramatic', 'Scientific', 'Technological', 'Cultural', 'Historical', 'Political', 'Humanitarian'],
        'topic': ['Personal Development', 'Education', 'Career', 'Health', 'Relationships', 'Wealth', 'Spirituality', 'Social Life', 'Family', 'Fun & Recreation', 'Contribution', 'Technology', 'Environment', 'Politics', 'History', 'Science', 'Art', 'Music', 'Literature', 'Sports',   'Travel', 'Cuisine', 'Languages', 'Mental Health', 'Emotional Intelligence', 'Parenting', 'Productivity'],
        'target_audience': ['Students', 'Professionals', 'Entrepreneurs', 'Parents', 'Self-employed', 'Self-learners', 'People in need'],
        },
    'goal': {
        'goal': ['Learn', 'Do', 'Be', 'Experience', 'Achieve', 'Acquire', 'Create', 'Overcome', 'Improve', 'Master', 'Teach', 'Inspire', 'Share'],
        'goal_type': ['Habit', 'Project', 'Event', 'Milestone', 'Challenge', 'Skill', 'Mindset', 'Attitude'],
        'goal_status': ['Not Started', 'In Progress', 'Completed', 'Abandoned', 'On Hold', 'Under Review'],
        'goal_relationship': ['Parent', 'Sibling', 'Friend', 'Partner', 'Mentor', 'Colleague', 'Neighbor'],
        'goal_motivation': ['Intrinsic', 'Extrinsic', 'Fear-based', 'Value-based', 'Achievement', 'Growth', 'Contribution', 'Enjoyment'],
        'goal_scope': ['Personal', 'Family', 'Community', 'Global'],
        'use_case': ['Task management', 'Collaboration', 'Communication', 'Resource management', 'Meditation', 'Mindfulness', 'Well-being', 'Goal tracking', 'Habit tracking', 'Project management', 'Self-improvement', 'Time management', 'Productivity'],
        },
    'tools': {
        'platform': ['Web', 'iOS', 'Android', 'Mac', 'Windows', 'Linux', 'Cross-platform', 'Command Line'],
        'device': ['Phone', 'Tablet', 'Laptop', 'Desktop', 'Smartwatch'],
        },
    'tech': {
        'framework': ['Python', 'JavaScript', 'React', 'Vue', 'Angular', 'Django', 'Flask', 'Node.js', 'Express', 'Ruby on Rails', 'Laravel', 'Spring', 'Flask', 'Django', 'Rails', 'ASP.NET', 'Meteor', 'Ember.js', 'Svelte', 'Gatsby', 'Next.js', 'Nuxt.js', 'Play', 'Zend', 'Symfony'],
        'language': ['Python', 'JavaScript', 'Java', 'C', 'C++', 'C#', 'PHP', 'Ruby','Go', 'Swift', 'Kotlin', 'Rust', 'TypeScript', 'Perl', 'Shell', 'Scala', 'Elixir', 'Lua', 'Objective-C', 'Groovy', 'Dart', 'Haskell', 'Julia', 'R', 'MATLAB'],
        },
}

file_texts = process_files_in_folder(folder_path)
assigned_labels = assign_labels_to_texts(file_texts, label_categories)
save_to_csv(assigned_labels, output_file)
