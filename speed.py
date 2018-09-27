import speedtest
import boto3
import random
import sched
import time
from decimal import *

interval = 60

dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
table = dynamodb.Table('wifi-speedtest-results')

def do_speedtest():
    s = speedtest.Speedtest()
    s.get_servers([])
    s.get_best_server()
    s.download()
    s.upload()

    results_dict = s.results.dict()

    timestamp = results_dict['timestamp']
    download = Decimal(str(results_dict['download']))
    upload = Decimal(str(results_dict['upload']))

    table.put_item(Item={
        'timestamp': timestamp,
        'download': download,
        'upload': upload,
    })

s = sched.scheduler(time.time, time.sleep)
def do_something(sc): 
    print "Doing stuff..."
    do_speedtest()
    s.enter(60, 1, do_something, (sc,))

s.enter(60, 1, do_something, (s,))
s.run()