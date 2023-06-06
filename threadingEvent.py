import subprocess
import threading

# Event for synchronization
event = threading.Event()

def run_script(script_name):
    subprocess.call([python_path, script_name])
    event.set()  # Signal that the script has finished

python_path = r'C:\Users\zacv2\PycharmProjects\CellularDrone\venv\Scripts\python.exe'
script1 = r'C:/Users/zacv2/PycharmProjects/CellularDrone/compressedVideoClient.py'
script2 = r'C:/Users/zacv2/PycharmProjects/CellularDrone/effecientKeyboardServer.py'

# Start keyboard server in a separate thread
thread1 = threading.Thread(target=run_script, args=(script1,))
thread1.start()

# Wait for thread1 to complete or exit if it takes too long
if not event.wait(timeout=10):
    print("Timeout occurred. Exiting...")
    thread1.join()  # Ensure the thread is terminated
else:
    event.clear()  # Reset the event for reuse

# Run compressed video client script in the main thread
run_script(script2)

# Wait for thread1 to complete
thread1.join()
