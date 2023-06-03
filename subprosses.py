import threading
import subprocess


def run_script(script_name):
    subprocess.Popen([python_path, script_name], cwd='.')

python_path = r'C:\Users\zacv2\PycharmProjects\CellularDrone\venv\Scripts\python.exe'
script1 = r'C:/Users/zacv2/PycharmProjects/CellularDrone/compressedVideoClient.py'
script2 = r'C:/Users/zacv2/PycharmProjects/CellularDrone/keyboardServer.py'

# Start script 1 in a separate thread
thread1 = threading.Thread(target=run_script, args=(script1,))
thread1.start()

# Start script 2 in the main thread
run_script(script2)

# Wait for thread 1 to complete
thread1.join()
