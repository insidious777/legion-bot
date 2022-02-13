from threading import Thread
proxy_folder = 'D:\dev\legionNETWORK\denis_proxy.txt'
def take_proxy(thread_number):
   with open(proxy_folder) as file:
      lines = file.readlines()
      proxy_str = lines[thread_number].strip()
   return proxy_str

def mainth(thread_number):
   print(take_proxy(thread_number))


for i in range(10):
   Thread(target=mainth, args=(i,)).start()

