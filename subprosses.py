import subprocess
import threading

def run_script(script_name):
    subprocess.call([python_path, script_name])

python_path = r'C:\Users\zacv2\PycharmProjects\CellularDrone\venv\Scripts\python.exe'
script1 = r'C:/Users/zacv2/PycharmProjects/CellularDrone/compressedVideoClient.py'
script2 = r'C:/Users/zacv2/PycharmProjects/CellularDrone/keyboardServer.py'

# Start keyboard server in a separate thread
thread1 = threading.Thread(target=run_script, args=(script1,))
thread1.start()

# Run compressed video client script in the main thread
run_script(script2)

# Wait for thread1 to complete
thread1.join()
