import socket,time
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
        if len(x)>0: # add non-empty values
            res.append(int(x))
    return res 

def is_sorted(arr):
    # all returns True if all elements are smaller than the next
    # one in the array
    return all(arr[i] <= arr[i+1] for i in range(len(arr)-1))

LOCALHOST = '10.20.30.159'
  # Replace with IP address 
PORT = 65432  # replace with 65432 or other available port
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# socketoptions
server.bind((LOCALHOST, PORT))
# set socket 
print("Server started")
print("Waiting for client request..")

active = 0
conexiones = []

print("Elija un metodo: (1) Mergesort (2) Heapsort (3) Quicksort")
op = int(input())
print("Elija numero mas grande")
upper = int(input())
print("Elija tiempo limite")
time_limit = float(input())
print("Elija longitud de arreglo")
L = int(input())

""" op = 3
upper = 100
time_limit = 0.5
L = 100000 """
# metodo y limite de tiempo

while active!=2: # wait until 2 conections
    server.listen(2)
    clientsock, clientAddress = server.accept()
    print ("Connection from : ", clientAddress)
    conexiones.append([clientsock,clientAddress])
    active +=1
    print("Active connections",active)

array = [randint(0,upper) for x in range(L)]  # create array
base = array.sort()

msg = to_string(array)

sorted = False
i = 0
x = 0
ready = 0
while not sorted:
    #print("Attempt #",x)
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

    #ready = conn.recv(1).decode() # get if array was sorted
    #print("READY IS ",ready, "size ",len(ready))

    data = conn.recv(4096000000) # receive array from client
    array = data.decode()
    print("converted array")

    array = to_array(array)
    print(array)
    print("length: ",len(array))
    A = len(array)==L
    B = is_sorted(array)
    print("IS L? ",A)
    print("sorted?",B)
    if A and B:
        print("conditions met")
        ready = 1

    
    if int(ready) == 1:
        sorted = True
        print("it was sorted")
        break
    else:
        print("not sorted")
    x +=1 
    i +=1
    if i==2:
        i = 0
