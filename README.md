# multithreading+multiprocessing socket listener
## start
```
cd danmu_listener
virtualenv env
source env/bin/activate
pip install -r requirement.txt
python danmu_new_1.py
```

This is an extension built on [pip danmu](https://github.com/littlecodersh/danmu/tree/master/danmu)

## Why multithreading
The original danmu was using python package socket to listen to chat messages in video streaming with two threads at a time. One listener and one heart beating. In order to amplify the ability to listen to thousands of channels at a time, we must apply multithreading.

## why multiprocessing
However, during the testing, I found out that each os has its own limit of how many threads you can start at a time. Mine would stop when threads >= 900. Therefore, we must use different processes to hold multithreading.

## why boht multithreading and multiprocessing
During the time I google for advices, I rarely see anyone using both at a time. However, my testing shows that if I built multiprocessing directly. Each process would cost 7 mb for the memory because multiprocessing does not share memory while there is a great overhead for each process, which makes memory the bottleneck!

## Queue and MongoDB
I used `multiprocessing.Queue` to receive messages among different threads and processes. My initial plan was using  `Queue.Queue` in each process, then write another process to specifically to run `multiprocessing.Queue.get(thread_message)` among each different process. However, it turns out that `multiprocessing.Queue` can easily fetch all messages among different threads and processes.
Right now, I am using `pymongo` and `insert_one` to insert each message `get()` from the Queue. It works out well locally as well cloud storage.

# future work to be done
## use `asyncio` on python 3
asyncio provides a perfect way to listen to web socket using async, but it only works with python3. I would have to make great effor to rewrite my script and also rewrite the whole `pip danmu` using asyncio

## use redis for concurrency messaging
Right now, it works alright by using `insert_one` and `multiprocessing.Queue` to handle the data transferring. In the future, I may end up using redis for better performance.

## use proxy to fake IP addresses
The website I am crawling has limit for each IP address, in order to overcome that I would need to buy more proxies....

## please support me!
