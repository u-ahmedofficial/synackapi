import requests
import warnings
import json
from threading import Thread
from Queue import Queue

requests.adapters.DEFAULT_RETRIES = 10
warnings.filterwarnings("ignore")
token = raw_input("Please enter your Synack Auth Header (Command from web console: sessionStorage.getItem('shared-session-com.synack.accessToken')): ")
target_code = raw_input("Please enter your target codename: ")
max_page_count = 100
blocks = []

def return_ips(q, result):
    while not q.empty():
        x = q.get()
        response = response = requests.get('https://platform.synack.com/api/targets/'+target_code+'/cidrs',params={'page': x[1]},headers={'Authorization': 'Bearer '+token},verify=False)
        temp = json.dumps(response.json()['cidrs']).replace("[","").replace("]","").replace("\"","").replace(", ","\n").split("\n")
        blocks.extend(temp)
        print("Page "+str(x[1])+" done.")
        q.task_done()
    return True

pages = []
for x in range(1, max_page_count, 3):
    pages.append(x)
    
q = Queue(maxsize=0)
for i in range(len(pages)):
    	q.put((i, pages[i]))

for i in range(20):
    	worker = Thread(target=return_ips, args=(q,pages))
    	worker.setDaemon(True)  
	worker.start()
q.join()

blocks = list(set(blocks))
f = open("blocks.txt","w+")
for i in range (len(blocks)):
	f.write(blocks[i]+"\n")
f.close()
print ("All done! Blocks have been added to blocks.txt file.")
