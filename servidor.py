import socket, threading
from random import randint

"""
mergeA 1
heapA 2
quickL 3
quickR 4

unsorted 0
sorted 1
"""
def to_string(arr):
    return ",".join(str(i) for i in arr)

def to_array(string):
    return [int(x) for x in string.split(",")]

class ClientThread(threading.Thread):
    def __init__(self,clientAddress,clientsocket,op,time=None):
        threading.Thread.__init__(self)
        self.csocket = clientsocket
        self.op = op
        if time:
            self.time = time
        print ("New connection added: ", clientAddress)
    
    
LOCALHOST = "127.0.0.1"
PORT = 8080
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# socketoptions
server.bind((LOCALHOST, PORT))
# set socket 
print("Server started")
print("Waiting for client request..")

active = 0
conexiones = []

op = 1
time_limit = 2
# metodo y limite de tiempo

while active!=2: # wait until 2 conections
    server.listen(2)
    clientsock, clientAddress = server.accept()
    print ("Connection from : ", clientAddress)
    conexiones.append([clientsock,clientAddress])
    active +=1
    print("Active connections",active)

array = [randint(0,500) for x in range(10000)]  # create array
msg = to_string(array)
sorted = False
i = 0
for _ in range(4):

    conn = conexiones[i][0] # connection
    address = conexiones[i][1]
    print("Address ",address)
    print("Op es ",op)
    conditions = f"{str(op)},{str(time_limit)}"
    conn.send(bytes(str(conditions),"UTF-8")) # send conditions
    conn.send(bytes(msg,'UTF-8')) # send array
    print("SENT conditions and ARRAY")
    ready = conn.recv(1096).decode() # get if array was sorted
    print("READY IS ",ready)
    if int(ready) == 1:
        sorted = True
        print("it was sorted")
        break
    else:
        print("not sorted")
    data = conn.recv(40960000) # receive array from client
    array = data.decode()
    print("Array printed")
    i +=1
    if i==2:
        i = 0
