import socket, threading
from sorting_algorithms import mergeSort,OrderVec,quicksort


def my_function(stop_event,op):
    # Your function code goes here
    # Call the bubble sort algorithm
    if op==1:
        print("merge")
        mergeSort(array,stop_event)
    elif op==2:
        print("heap")
        sol = OrderVec(array,stop_event)
    elif op == 3:
        print("quickM")
        quicksort(array,0,len(array)-1,stop_event)
    # Print the sorted array

def timeout_handler():
    print("Function timed out")
    
def to_string(arr):
    return ",".join(str(i) for i in arr)

def to_array(string):
    res = []
    for x in string.split(","):
        if len(x)>0:
            res.append(int(x))
    return res 
    #return [int(x) for x in string.split(",")]

finished = 1 # assume it successfully sorted

SERVER = "127.0.0.1" #local
PORT = 8080
# AF INET IS IPv4 SOCK STREAM IS TCP
times = 0

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER, PORT))

while True:
    print("TIME # ",times)
    if times == 0:
        conditions = client.recv(1096).decode() # get what method to use (first time)
        op = int(conditions.split(",")[0])
        Z = float(conditions.split(",")[1])

    print("conditions es ",conditions)

    in_data =  client.recv(4096000000) # receive 
    check = in_data.decode() 
    if len(check)==0:
        break
    else:
        print("array received")
    array= to_array(check) # into arrayz
    print("Length: ",len(array))
    stop_event = threading.Event()

    # Create a thread and start it
    t = threading.Thread(target=my_function, args=(stop_event,op))
    t.start()

    # Wait for the thread to complete or timeout
    t.join(Z)

    if t.is_alive():
        finished = 0
        # Set the stop event to signal the thread to stop
        stop_event.set()

        # Wait for the thread to stop
        t.join()

        # Call the timeout handler
        timeout_handler()
            
                
    print("finished is ",finished)

    #v0 = client.send(bytes(str(finished),"UTF-8"))
    #print("SENT IF FINISHED. Size: ",v0)

    out_data = to_string(array)

    v = client.send(bytes(out_data,'UTF-8'))
    print("SENT ARRAY. Size: ",v)
    times +=1
client.close()
