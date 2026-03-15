from datetime import date, datetime, time
import json
import streamlit as st


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, time):
            return obj.strftime("%H:%M:%S")
        elif isinstance(obj, date):
            return obj.isoformat()
        elif isinstance(obj, datetime):
            return obj.isoformat()
        return super(CustomJSONEncoder, self).default(obj)

def valid_value(value):
    return value not in [None, "None", "null", "Null", "NULL", "none", "NoneType", False, "", 0, []]



def conditional_date_input(label, checked, help=None):
    if checked:
        return st.date_input(label, help=help)
    else:
        st.write(label)
        return None
    
def formatted_options(old_value, options):
    old_value = old_value.capitalize()
    sorted_options = sorted(options)
    if old_value in sorted_options:
        sorted_options.remove(old_value)
    return [old_value] + sorted_options