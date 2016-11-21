from danmu import DanMuClient
import urllib2
import json
import time, sys
import threading
from multiprocessing import Process 
from multiprocessing import Queue as Process_queue
from pymongo import MongoClient
import pymongo
# import Queue as Thread_queue
# get rooms that are alive

def get_live_rooms(offset,limit):
    live_rooms = []
    num_rooms=0
    for page in range(offset):
        try:
            response = urllib2.urlopen('http://open.douyucdn.cn/api/RoomApi/live?offset={}&limit={}'.format(99*(page)+1,limit))
            live_rooms.extend(json.load(response)['data'])
            num_rooms += 1
            print num_rooms
        except:
            print "endofrooms"
    urls = map(lambda x: x['url'], live_rooms)	
    return set(urls)
# def pp(msg):
#     print(msg.encode(sys.stdin.encoding, 'ignore').
#         decode(sys.stdin.encoding))

# get danmu from room

def start_danmu(dmc,room):
	@dmc.danmu
	def danmu_fn(msg):
		info = {}
		info['room'] = room
		info['time'] = time.time()
		info['uid'] = msg['uid']
		info['nn'] = msg['nn']
		info['rid'] = msg['rid']
		info['txt'] = msg['txt']
		process_queue.put(info)
	# @dmc.gift
	# def gift_fn(msg):
	# 	pp('[%s] sent a gift!' % content['NickName'])

	# @dmc.other
	# def other_fn(msg):
	# 	pp('Other message received')
 	dmc.start(blockThread = True)

def start_thread(dmcs,process_number):
	task = 0
	start_threads = process_number*700
	end_threads = (process_number+1)*700 if (process_number+1)*700<len(dmcs) else len(dmcs)
	for dmc in dmcs[process_number*700:(process_number+1)*700]:
		t = threading.Thread(target=start_danmu, args=(dmc[0],dmc[1],))
		t.daemon = True
		t.start()
		task += 1
		print "process{}:{}task started".format(process_number,task)
	while True:
		time.sleep(10)
		print "process{}:{}room_listening_to".format(process_number,threading.active_count()/3+1)


def start_process(dmcs):
	process = 0
	processes_need = len(dmcs)/700+1
	for process_number in range(processes_need):
		p = Process(target=start_thread, args=(dmcs,process_number,))
		p.daemon = True
		p.start()
		process += 1
		print "process started:{}".format(process)

if __name__ == "__main__":

	all_rooms = get_live_rooms(2,100)
	dmcs_unvalid = map(lambda x: (DanMuClient(x),x),all_rooms)
	dmcs = filter(lambda x: x[0].isValid(), dmcs_unvalid) #dmc is the tuple that contains(dmc,rom)
	process_queue = Process_queue()
	start_process(dmcs)
	# connect to MongoDB
	DBclient = MongoClient()
	danmu_db = DBclient['danmu']
	danmu_info = danmu_db['test']
	while True:
		item = process_queue.get()
		danmu_info.insert_one(item).inserted_id

