import socket, threading
from time import sleep
def bubbleSort(array, stop_event):
    n = len(array)

    for i in range(n):
        # Last i elements are already sorted
        for j in range(n - i - 1):
            # Traverse the array from 0 to n-i-1
            # Swap if the element found is greater than the next element
            if array[j] > array[j + 1]:
                array[j], array[j + 1] = array[j + 1], array[j]

            # Check if the thread should stop
            if stop_event.is_set():
                return
    return 1

def my_function(stop_event):
    # Your function code goes here
    # Call the bubble sort algorithm
    bubbleSort(array, stop_event)
    # Print the sorted array

def timeout_handler():
    print("Function timed out")
    
def to_string(arr):
    return ",".join(str(i) for i in arr)

def to_array(string):
    return [int(x) for x in string.split(",")]

# Python program for implementation of Bubble Sort

def reverse(array:list):
    array.sort(reverse=True)


finished = 1 # assume it successfully sorted

SERVER = "127.0.0.1" #local
PORT = 8080
# AF INET IS IPv4 SOCK STREAM IS TCP
times = 0

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER, PORT))

while True:
    print(times)
    conditions = client.recv(1096).decode() # get what method to use
    op = int(conditions.split(",")[0])
    Z = float(conditions.split(",")[1])
    print(conditions)


    in_data =  client.recv(40960000) # receive 
    array= to_array(in_data.decode()) # into arrayz
    if op ==1:
        reverse(array)
    else:
        #bubbleSort(array)
        # Set a timeout of Z seconds
        # Z = 1
        # Create a stop event
        stop_event = threading.Event()

        # Create a thread and start it
        t = threading.Thread(target=my_function, args=(stop_event,))
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
            
                
    if finished == 0:
        print("did not finish")
    else:
        print("FINISHED",finished)
        print(array)
    client.sendall(bytes(str(finished),"UTF-8"))


    out_data = to_string(array)

        #print("From Server :" ,in_data.decode())
        #out_data = input()
    client.sendall(bytes(out_data,'UTF-8'))
        #if out_data=='bye':
        #    break
    times +=1
client.close()