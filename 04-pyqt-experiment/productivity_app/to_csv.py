import csv
from data_collection.data_categories import data_categories

header = ["id", "category", "subcategory", "topic", "subtopic", "collection_method", "collection_frequency",
          "collection_source", "specificity", "data_format", "auto_or_manual", "trigger", "datetime_last_collection",
          "explanation", "comments", "active"]

# Recursive function to flatten the nested dictionary
def flatten_dict(d, prefix="", flattened=None):
    if flattened is None:
        flattened = {}
    for key, value in d.items():
        if isinstance(value, dict):
            if prefix:
                new_prefix = f"{prefix} > {key}"
            else:
                new_prefix = key
            flatten_dict(value, new_prefix, flattened)
        elif isinstance(value, list):
            for i, item in enumerate(value):
                if prefix:
                    new_prefix = f"{prefix} > {key} > {item}"
                else:
                    new_prefix = f"{key} > {item}"
                flattened[new_prefix] = {}
        else:
            if prefix:
                if prefix not in flattened:
                    flattened[prefix] = {}
                flattened[prefix][key] = value
            else:
                flattened[key] = value
    return flattened

# Flatten the dictionary
flattened_data = flatten_dict(data_categories)

# Write data to CSV file
with open("productivity_app/data_categories.csv", "w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=header)
    writer.writeheader()
    for i, (key, value) in enumerate(flattened_data.items(), start=1):
        if isinstance(value, dict):
            split_key = key.split(" > ")
            category = split_key[0] if len(split_key) >= 1 else ""
            subcategory = split_key[1] if len(split_key) >= 2 else ""
            topic = split_key[2] if len(split_key) >= 3 else ""
            subtopic = split_key[3] if len(split_key) >= 4 else ""
            row = {
                "id": i,
                "category": category,
                "subcategory": subcategory,
                "topic": topic,
                "subtopic": subtopic,
                "collection_method": value.get("collection_method", ""),
                "collection_frequency": value.get("collection_frequency", ""),
                "collection_source": value.get("collection_source", ""),
                "specificity": value.get("specificity", ""),
                "data_format": value.get("data_format", ""),
                "auto_or_manual": value.get("automation", ""),
                "trigger": value.get("trigger", ""),
                "datetime_last_collection": value.get("datetime_last_collection", ""),
                "explanation": value.get("explanation", ""),
                "comments": value.get("comments", ""),
                "active": value.get("active", "")
            }
            writer.writerow(row)

print("CSV file created successfully.")
