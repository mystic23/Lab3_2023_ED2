import socket, threading
from random import randint


"""
mergeA 1
heapA 2
quickM

unsorted 0
sorted 1
"""
def to_string(arr):
    return ",".join(str(i) for i in arr)

def to_array(string):
    res = []
    for x in string.split(","):
        if len(x)>0:
            res.append(int(x))
    return res 
# 1,2,3,
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

#print("Elija un metodo: (1) Mergesort (2) Heapsort (3) Quicksort")
# op = input()
op = 1

time_limit = 0.5
# metodo y limite de tiempo

while active!=2: # wait until 2 conections
    server.listen(2)
    clientsock, clientAddress = server.accept()
    print ("Connection from : ", clientAddress)
    conexiones.append([clientsock,clientAddress])
    active +=1
    print("Active connections",active)

array = [randint(0,10) for x in range(1000000)]  # create array
msg = to_string(array)
sorted = False
i = 0
x = 0
while not sorted:
    
    conn = conexiones[i][0] # connection
    address = conexiones[i][1]
    print("Address ",address)
    
    if x ==0 or x==1:  # on first time to each client
        conditions = f"{str(op)},{str(time_limit)}"
        print("conditions: ",conditions)
        v1 = conn.send(bytes(str(conditions),"UTF-8")) # send conditions
        print("SENT CONDITIONS. Size:",v1)

    v2 =conn.send(bytes(msg,'UTF-8')) # send array
    print("SENT ARRAY. Size:",v2)
    ready = conn.recv(1).decode() # get if array was sorted
    print("READY IS ",ready, "size ",len(ready))
    data = conn.recv(4096000000) # receive array from client
    array = data.decode()
    
    array = to_array(array)
    print("LEN ",len(array))

    if int(ready) == 1:
        sorted = True
        print("it was sorted")
        print("Array printed")
        break
    else:
        print("not sorted")
    x +=1 
    i +=1
    if i==2:
        i = 0
