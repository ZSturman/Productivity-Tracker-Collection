import socket
import time
import subprocess
from pynput import keyboard, mouse
import csv
import os
from txt_from_screen import run_txt_from_screen

device_name = socket.gethostname()

idle_time_limit = 10  # Time in seconds after which the user is considered idle
last_activity_time = time.time()
user_is_idle = False

def get_active_window_and_document():
    script = '''
        tell application "System Events"
            set frontmostProcess to first process where it is frontmost
            try
                set windowTitle to name of front window of frontmostProcess
                set documentPath to value of attribute "AXDocument" of front window of frontmostProcess
            on error
                set windowTitle to "N/A"
                set documentPath to "N/A"
            end try
            set appName to name of frontmostProcess
        end tell
        return {appName, windowTitle, documentPath}
    '''

    try:
        result = subprocess.check_output(['/usr/bin/osascript', '-e', script])
        app_name, window_title, document_path = result.decode('utf-8').strip().split(", ", 2)
        
        if app_name == "Google Chrome":
            tab_title, tab_url = get_chrome_active_tab_info()
            return app_name, tab_title, tab_url
        else:
            if app_name == "Electron":
                app_name = "Visual Studio Code"
            if document_path == "missing value":
                document_path = "N/A"
            return app_name, window_title, document_path

    except subprocess.CalledProcessError:
        return None, None, None

def get_chrome_active_tab_info():
    script = '''
        tell application "Google Chrome"
            set activeTab to active tab of front window
            set tabTitle to title of activeTab
            set tabURL to URL of activeTab
        end tell
        return {tabTitle, tabURL}
    '''
    try:
        result = subprocess.check_output(['/usr/bin/osascript', '-e', script])
        tab_title, tab_url = result.decode('utf-8').strip().split(", ", 1)
        return tab_title, tab_url
    except subprocess.CalledProcessError:
        return None, None



def on_keyboard_event(key_event):
    global last_activity_time
    last_activity_time = time.time()


def on_mouse_move(x, y):
    global last_activity_time
    last_activity_time = time.time()


def on_mouse_click(x, y, button, pressed):
    global last_activity_time
    last_activity_time = time.time()


def on_mouse_scroll(x, y, dx, dy):
    global last_activity_time
    last_activity_time = time.time()


# Set up listeners for keyboard and mouse events
keyboard_listener = keyboard.Listener(on_press=on_keyboard_event)
mouse_listener = mouse.Listener(on_move=on_mouse_move, on_click=on_mouse_click, on_scroll=on_mouse_scroll)


def write_to_csv(date, time, device_name, app_name, window_title, document_path, active_status):
    #file_path = f'/Users/zacharysturman/data_collection/activity_log_{date}.csv'
    file_path = f'/Users/zacharysturman/Library/Mobile Documents/com~apple~CloudDocs/Data_collection/csv_and_txt_from_screen_macbook/activity_log_{date}.csv'
    file_exists = os.path.isfile(file_path)
    
    with open(file_path, mode='a') as csv_file:
        fieldnames = ['date', 'time', 'device_name', 'app_name', 'window_title', 'document_path', 'active_status']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        
        if not file_exists:
            writer.writeheader()
        
        writer.writerow({
            'date': date,
            'time': time,
            'device_name': device_name,
            'app_name': app_name,
            'window_title': window_title,
            'document_path': document_path,
            'active_status': active_status
        })

# Start the listeners
keyboard_listener.start()
mouse_listener.start()

# Get the initial active window information
initial_app_name, initial_window_title, initial_document_path = get_active_window_and_document()

# Write the initial active status to the CSV file
write_to_csv(time.strftime('%Y-%m-%d'), time.strftime('%H:%M:%S'), device_name, initial_app_name, initial_window_title, initial_document_path, True)

try:
    prev_app_name, prev_window_title, prev_document_path = None, None, None
    current_date = time.strftime('%Y-%m-%d')
    last_txt_from_screen_time = time.time()

    while True:
        time.sleep(1)  # Check for idle status every second
        current_time = time.time()
        elapsed_time = current_time - last_activity_time
        txt_from_screen_elapsed_time = current_time - last_txt_from_screen_time

        app_name, window_title, document_path = get_active_window_and_document()
        new_date = time.strftime('%Y-%m-%d')
        
        # If it's a new day, update the current_date variable
        if new_date != current_date:
            current_date = new_date

        # If the user switches between windows/tabs
        if (prev_app_name, prev_window_title, prev_document_path) != (app_name, window_title, document_path):
            prev_app_name, prev_window_title, prev_document_path = app_name, window_title, document_path
            write_to_csv(current_date, time.strftime('%H:%M:%S'), device_name, app_name, window_title, document_path, not user_is_idle)

        if elapsed_time > idle_time_limit and not user_is_idle:
            user_is_idle = True
            write_to_csv(current_date, time.strftime('%H:%M:%S'), device_name, app_name, window_title, document_path, not user_is_idle)
        elif elapsed_time <= idle_time_limit and user_is_idle:
            user_is_idle = False
            write_to_csv(current_date, time.strftime('%H:%M:%S'), device_name, app_name, window_title, document_path, not user_is_idle)

        # Schedule txt_from_screen function
        if elapsed_time <= 11 * 60 and txt_from_screen_elapsed_time >= 2 * 60:
            try:
                run_txt_from_screen()
                last_txt_from_screen_time = time.time()
            except Exception as e:
                print(f"Error running txt_from_screen: {e}")

except KeyboardInterrupt:
    keyboard_listener.stop()
    mouse_listener.stop()