import threading
import numpy as np
def bubble_sort(array, stop_event):
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
            

    print("Process was finished!")

def mergeSort(array,stop_event):
  if len(array) > 1:

    # r is the point or middle from
    #  where the array is divided into two subarrays
    r = len(array)//2

    L = array[:r] # until middle
    M = array[r:] # from middle

    # Sort the two halves
    mergeSort(L,stop_event)
    mergeSort(M,stop_event)

    i = j = k = 0

    # Until we reach either end of either L or M, pick larger among
    # elements L and M and place them in the correct position at the array
    while i < len(L) and j < len(M):
      if L[i] < M[j]:
        array[k] = L[i]
        i += 1
      else:
        array[k] = M[j]
        j += 1
      k += 1
      if stop_event.is_set():
         return
      
    # When we run out of elements in either L or M,
    # pick up the remaining elements and put in A[p..r]
    while i < len(L):
      array[k] = L[i]
      i += 1
      k += 1
      if stop_event.is_set():
         return
    while j < len(M):
      array[k] = M[j]
      j += 1
      k += 1
      if stop_event.is_set():
         return
      
class OrderVec:
    def __init__(self, values: list[int],stop_event) -> None:
        '''
            Constructor

            Args:
                values (list[int]) : [lista que se quiere ordenar]

            Return:

        '''
        self.values = values
        self.heap_sort(stop_event)

    def heapify(self, array: list(), n: int, k: int,stop_event) -> None:
        '''
            Forma un maxHeap

            Args:
                array (list): [Lista que se quiere ordenar]
                n     (int) : [Tamaño de la lista]
                k     (int) : [Indice de la lista]

            Return:

        '''
        # Suponemos que el más grande es el de la posicion k
        mayor = k

        # Indices de los hijos izquierdo y derecho (l & r)
        l = 2 * k + 1
        r = 2 * k + 2

        # Verificamos que no sobrepase el tamaño del arreglo y si la posicion del "más grande" con el valor de la posicion del hijo izq es menor
        if l < n and array[mayor] < array[l]:
            mayor = l 
        
        # Lo mismo de arriba pero con la posicion del hijo derecho
        if r < n and array[mayor] < array[r]:
            mayor = r

        # Hacemos un "swap" en caso tal de que sean distintos al final
        if mayor != k:
            array[k], array[mayor] = array[mayor], array[k]
            self.heapify(array, n, mayor,stop_event)
            
        if stop_event.is_set():
         return
    def heap_sort(self,stop_event) -> None:
        '''
            Ordena la lista

            Args:

            Return:

        '''
        # Definimos el tamaño de nuestro arreglo
        size  = len(self.values)

        # Por temas de optimizacion, se realizara hasta la mitad de los elementos del array y haremos un max heap (arbol donde cada root es mayor que sus hijos)
        for k in range(size//2, -1, -1):
            if stop_event.is_set():
              return
            self.heapify(self.values, size, k,stop_event)


        # Dado nuestro maxHeap anterior, empezamos a extraer los elementos para empezar con el ordenamiento haciendo otro "swap"
        for k in range(size-1, 0, -1):
            if stop_event.is_set():
              return
            self.values[k], self.values[0] = self.values[0], self.values[k]
            # Claramente el indice va a comenzar en 0
            self.heapify(self.values, k, 0,stop_event)

def my_function(stop_event,type:int):
    # Your function code goes here
    array = [np.random.randint(500) for i in range(1000000)]
    # Call the bubble sort algorithm
    if type ==1:
      print("merge")
      mergeSort(array, stop_event)
    elif type==2:
      print("bubble")
      bubble_sort(array,stop_event)
    else:
      print("heap")
      solution = OrderVec(array,stop_event)
      for i in range(100):
         print(array[i])
      print("MIN",min(array))
    # Print the sorted array
    #print("Sorted array:", array)

def timeout_handler():
    print("Function timed out")

# Set a timeout of Z seconds
Z = 5
# Create a stop event
stop_event = threading.Event()
type =3
# Create a thread and start it
t = threading.Thread(target=my_function, args=(stop_event,type,))
t.start()

# Wait for the thread to complete or timeout
t.join(Z)

if t.is_alive():
    # Set the stop event to signal the thread to stop
    stop_event.set()

    # Wait for the thread to stop
    t.join()

    # Call the timeout handler
    timeout_handler()
