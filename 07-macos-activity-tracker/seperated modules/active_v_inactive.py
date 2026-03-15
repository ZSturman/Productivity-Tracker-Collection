import time
from pynput import keyboard, mouse

idle_time_limit = 10  # Time in seconds after which the user is considered idle
last_activity_time = time.time()
user_is_idle = False



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

# Start the listeners
keyboard_listener.start()
mouse_listener.start()

# Print the initial active status
print(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - active")

try:
    while True:
        time.sleep(1)  # Check for idle status every second
        current_time = time.time()
        elapsed_time = current_time - last_activity_time

        if elapsed_time > idle_time_limit and not user_is_idle:
            user_is_idle = True
            print(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - idle")
        elif elapsed_time <= idle_time_limit and user_is_idle:
            user_is_idle = False
            print(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - active")

except KeyboardInterrupt:
    keyboard_listener.stop()
    mouse_listener.stop()
