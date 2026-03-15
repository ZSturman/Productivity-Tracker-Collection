import socket
import platform

# Get the device name (hostname)
device_name = socket.gethostname()

# Get the system information
system_name = platform.system()
system_version = platform.version()

print(f"Device Name: {device_name}")
print(f"System Name: {system_name}")
print(f"System Version: {system_version}")
