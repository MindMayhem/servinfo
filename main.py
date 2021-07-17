import socket, tqdm
import os
from _thread import *

ServerSideSocket = socket.socket()
from requests import get

host = get('https://api.ipify.org').text
print(host)
port = 12345
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"
ThreadCount = 0
try:
    ServerSideSocket.bind((host, port))
except socket.error as e:
    print(str(e))

print(f"SERVER READY\nListening on: {host}:{port}\n\nReady to work..")
ServerSideSocket.listen(5)

def multi_threaded_client(connection):
   try:
      received = connection.recv(BUFFER_SIZE)
      print(str(received))
      filename, filesize = str(received).split(SEPARATOR)
# remove absolute path if there is
      filename = os.path.basename(filename)
# convert to integer
      filesize = int(filesize.replace("'",""))
      progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
      with open(filename, "wb") as f:
         while True:
            bytes_read = connection.recv(BUFFER_SIZE)
            if not bytes_read:    
               break
            f.write(bytes_read)
        # update the progress bar
            progress.update(len(bytes_read))
      connection.close()
   except Exception as e:
      print(f"ERROR: {e}")

while True:
    Client, address = ServerSideSocket.accept()
    start_new_thread(multi_threaded_client, (Client, ))
ServerSideSocket.close()