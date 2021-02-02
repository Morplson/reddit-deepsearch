import threading
import math


start_array = [1,2,3,4,5,6,7,8,9,1,2,3,4,5,6,7,8,9]

def threaded_function(batch_data):
    for v in batch_data:
        print(str(v))

        results.append(v+1)




#Treading
results = []

data = start_array
thread_num = 4

if len(data)>0:
    class_size = math.ceil(len(data)/thread_num)
    classes = [data[x:x+class_size] for x in range(0, len(data), class_size)]

    threads = []
    for i in range(len(classes)):
        thread = threading.Thread(target=threaded_function,args=(classes[i],))
        threads.append(thread)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()
