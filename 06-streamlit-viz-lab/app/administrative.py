import os
import uuid
from datetime import date, datetime, time
import json
import pandas as pd

def make_safe():
    uuid_str = str(uuid.uuid4())
    safe_title = uuid_str.replace(" ", "_")
    safe_title = safe_title.replace("/", "_")
    safe_title = safe_title.replace("\\", "_")
    safe_title = safe_title.replace(":", "_")
    safe_title = safe_title.replace("*", "_")
    safe_title = safe_title.replace("?", "_")
    safe_title = safe_title.replace("\"", "_")
    safe_title = safe_title.replace("<", "_")
    safe_title = safe_title.replace(">", "_")
    safe_title = safe_title.replace("|", "_")
    return safe_title

    
def valid_value(value):
    if value in [None, "None", "null", "Null", "NULL", "none", "NoneType", False, "", 0, [], {}]:
        return False
    if isinstance(value, dict) and not value:  # check if it's an empty dictionary
        return False
    return True

def formatted_options(old_value, options):
    old_value = old_value.capitalize()
    sorted_options = sorted(options)
    if old_value in sorted_options:
        sorted_options.remove(old_value)
    return [old_value] + sorted_options

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, time):
            return obj.strftime("%H:%M:%S")
        elif isinstance(obj, date):
            return obj.isoformat()
        elif isinstance(obj, datetime):
            return obj.isoformat()
        return super(CustomJSONEncoder, self).default(obj)
    

def make_sure_items_are_in_csv(directory_path, productivity_csv, productivity_csv_path, timeline_csv, timeline_csv_path, folders):
    # if folder not in productivity_csv, add it
    for folder in folders:
        folder_path = os.path.join(directory_path, folder)
        if folder_path not in productivity_csv["folder_dir"].values:
            new_folder = pd.DataFrame({"id": make_safe(), "date_created": [pd.Timestamp.now()], "date_updated": [pd.Timestamp.now()], "folder_dir": [folder_path], "identifying_type": ["folder"], "title": [folder], "most_recently_selected": [pd.Timestamp.now()]})
            new_folder.to_csv(productivity_csv_path, mode="a", header=False, index=False)
        # if json_data in folder, add the files that end with .json to productivity_csv
        if os.path.exists(os.path.join(folder_path, "json_data")):
            json_files = [file for file in os.listdir(os.path.join(folder_path, "json_data")) if os.path.isfile(os.path.join(folder_path, "json_data", file)) and file.endswith(".json")]
            for json_file in json_files:
                json_file_path = os.path.join(folder_path, "json_data", json_file)
                with open(json_file_path, "r") as file:
                    json_data = json.load(file)
                if json_data["id"] not in productivity_csv["id"].values:
                    json_id = json_data["id"]
                    identifying_type = json_data["identifying_type"]
                    title = json_data["title"]
                    date_created = json_data["date_created"]
                    date_updated = json_data["date_modified"]

                    new_json_file = pd.DataFrame({"id": json_id, "date_created": date_created, "date_updated": date_updated, "folder_dir": [json_file_path], "identifying_type": identifying_type, "title": title, "most_recently_selected": [pd.Timestamp.now()]})
                    new_json_file.to_csv(productivity_csv_path, mode="a", header=False, index=False)

                if json_data["id"] not in timeline_csv['id'].values:
                    json_id = json_data["id"]
                    identifying_type = json_data["identifying_type"]
                    title = json_data["title"]
                    completed = json_data["completed"]
                    if completed == True:
                        completed = json_data["datetime_completed"]
                    else:
                        completed = None
                    started = json_data["started"]
                    if started == True:
                        started = json_data["datetime_started"]
                    else:
                        started = None
                    no_due_date = json_data["no_due_date"]
                    if not no_due_date:
                        due_date = json_data["datetime_due"]
                    else:
                        due_date = None
                    estimated_duration = json_data["estimated_duration"]
                    actual_duration = json_data["actual_duration"]
                    new_timeline_row = pd.DataFrame({"id": json_id, "completed": completed, "type": identifying_type, "title": title, "started": started, "estimated_duration": estimated_duration, "actual_duration": actual_duration, "due_date": due_date}, index=[0])
                    new_timeline_row.to_csv(timeline_csv_path, mode="a", header=False, index=False)


def comment_safe(comment):
    # get the first 10 characters of comment
    comment_preview = comment[:10]
    comment_preview = comment_preview.replace("\n", " ")
    comment_preview = comment_preview.replace("\r", " ")
    comment_preview = comment_preview.replace("\t", " ")
    comment_preview = comment_preview.replace("#", "")
    comment_preview = comment_preview.replace("*", "")
    comment_preview = comment_preview.replace("-", "")
    comment_preview = comment_preview.replace("+", "")
    comment_preview = comment_preview.replace("=", "")
    comment_preview = comment_preview.replace("~", "")
    comment_preview = comment_preview.replace("`", "")
    comment_preview = comment_preview.replace(">", "")
    comment_preview = comment_preview.replace("<", "")
    comment_preview = comment_preview.replace("!", "")
    comment_preview = comment_preview.replace("[", "")
    comment_preview = comment_preview.replace("]", "")
    comment_preview = comment_preview.replace("(", "")
    comment_preview = comment_preview.replace(")", "")
    comment_preview = comment_preview.replace("{", "")
    comment_preview = comment_preview.replace("}", "")
    comment_preview = comment_preview.replace(".", "")
    comment_preview = comment_preview.replace(",", "")
    comment_preview = comment_preview.replace(":", "")
    comment_preview = comment_preview.replace(";", "")
    comment_preview = comment_preview.replace("|", "")
    comment_preview = comment_preview.replace("/", "")
    comment_preview = comment_preview.replace("\\", "")
    comment_preview = comment_preview.replace("?", "")
    comment_preview = comment_preview.replace("&", "")
    comment_preview = comment_preview.replace("$", "")
    comment_preview = comment_preview.replace("@", "")
    comment_preview = comment_preview.replace("%", "")
    comment_preview = comment_preview.replace("^", "")
    comment_preview = comment_preview.replace("'", "")
    comment_preview = comment_preview.replace('"', "")
    comment_preview = comment_preview.replace(" ", "_")
    
    # add "..." to the end of the comment preview if the comment is longer than 10 characters
    if len(comment) > 10:
        comment_preview += "..."

    return comment_preview