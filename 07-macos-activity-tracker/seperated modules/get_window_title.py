import time
import subprocess

def get_active_window_and_document():
    script = '''
        tell application "System Events"
            set frontmostProcess to first process where it is frontmost
            set windowTitle to name of front window of frontmostProcess
            set documentPath to value of attribute "AXDocument" of front window of frontmostProcess
            set appName to name of frontmostProcess
        end tell
        return {appName, windowTitle, documentPath}
    '''

    try:
        result = subprocess.check_output(['osascript', '-e', script])
        app_name, window_title, document_path = result.decode('utf-8').strip().split(", ", 2)
        
        if app_name == "Google Chrome":
            tab_title, tab_url = get_chrome_active_tab_info()
            return app_name, tab_title, tab_url
        else:
            if app_name == "Electron":
                app_name = "Visual Studio Code"
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
        result = subprocess.check_output(['osascript', '-e', script])
        tab_title, tab_url = result.decode('utf-8').strip().split(", ", 1)
        return tab_title, tab_url
    except subprocess.CalledProcessError:
        return None, None


print(get_active_window_and_document())
time.sleep(1)
print(get_active_window_and_document())
time.sleep(1)
print(get_active_window_and_document())
time.sleep(1)
print(get_active_window_and_document())
time.sleep(1)
print(get_active_window_and_document())