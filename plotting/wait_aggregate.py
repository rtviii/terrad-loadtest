from functools import total_ordering
import sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import matplotlib.ticker as plticker
import seaborn as sns
from dask import dataframe as  dd
from dask import dataframe
from time import time
# sns.set_theme(style="darkgrid")


"""
The csv is a truncated k6 output of the form with two waiting/dat rows repeating for each request:

http_req_connecting 1643769199 17.185348
http_req_waiting 1643769199 22.982642
data_received 1643769199 509.000000
http_req_connecting 1643769199 0.000000
...
"""

logpath = sys.argv[1]
df:dataframe.DataFrame = dd.read_csv(logpath, sep=' ', lineterminator="\n", names=['metric','timestamp','value'])

total_time = 0
report   = {
}



def _(metric,timestamp,value):
    timestamp = str(timestamp)
    if str(timestamp) not in report:
        global total_time
        total_time += 1
        report[timestamp] = {
            "inbound": [],
            "wait"   : [],
        }
    else:
        if metric == 'data_received':
            report[timestamp]['inbound'].append(value)
        elif metric == 'http_req_waiting':
            report[timestamp]['wait'].append(value)

list(map(_,df['metric'], df['timestamp'], df['value']))

for t in report.items():
    # print(t)

    # --+-+-+--+-+-+-+-+-+-
    n_reqs = len(t[1]['wait'])
    waittimes = t[1]['wait']
    traffic   = t[1]['inbound']
    # -+-+-+--+-+-+--+-+-+-

    w_std  = np.std(waittimes)
    w_u    = np.mean(t[1]['wait'])


    report[t[0]]['w_u']     = w_u
    report[t[0]]['w_std']   = w_std
    report[t[0]]['traffic'] = sum(traffic)
    report[t[0]]['n_reqs']  = n_reqs

timestamps = [*map(lambda k: str( datetime.fromtimestamp(int(k)) )[-8:], report.keys())]

w_u        = np.array([* map(lambda x: x['w_u'], report.values())])
w_std      = np.array([* map(lambda x: x['w_std'], report.values())])
n_reqs     = np.array([* map(lambda x: x['n_reqs'], report.values())])
traffic    = np.array([* map(lambda x: x['traffic'], report.values())])

THRESHOLD_LATENCY_MS = 2000

# # -⋯⋯⋅⋱⋰⋆⋅⋅⋄⋅⋅∶⋅⋅⋄▫▪▭┈┅✕⋅⋅⋄⋅⋅✕∶⋅⋅⋄⋱⋰⋯⋯⋯⋯⋅⋱⋰⋆⋅⋅⋄⋅⋅[Plots]∶⋅⋅⋄▫▪▭┈┅✕⋅⋅⋄⋅⋅✕∶⋅⋅⋄⋱⋰⋯⋯⋯⋅⋱⋰⋆⋅⋅⋄⋅⋅∶⋅⋅⋄▫▪▭┈┅✕⋅⋅⋄⋅⋅✕∶⋅⋅⋄⋱⋰⋯⋯

# f, axarr = plt.subplots(2, sharex=True)
f, axarr = plt.subplots()

lat = axarr
lat.plot(timestamps, w_u, 'b-',  label="Average time spent waiting")
lat.fill_between(timestamps, w_u-w_std, w_u+w_std, color='b', alpha=0.2)
lat.plot(timestamps, [THRESHOLD_LATENCY_MS]*len(timestamps),'red',linewidth=0.5,  label=f"{THRESHOLD_LATENCY_MS/1000}s Threshold")

lat.set_ylabel('Http Request Waittime (ms)')
lat.set_title('Waiting time')
lat.set_axisbelow(True)

# # _twinx_n_reqs = lat.twinx()
# # _twinx_n_reqs.plot(timestamps,n_reqs, color='blue', alpha=0.6, label="Number of requests")
# # _twinx_n_reqs.set_ylabel("Requests/second", color="blue", size=14)
# # _twinx_n_reqs.set_axisbelow(True)
# # _twinx_n_reqs.grid(color='gray', linestyle='dashed')
# # _twinx_n_reqs.tick_params(axis='y', colors='blue')

# # traffic_in = axarr[1]
# # traffic_in.plot(timestamps, traffic/1024, color='black', linewidth=0.5,alpha=0.9, label="Incoming traffic")
# # traffic_in.set_title('Inbound Traffic')
# # traffic_in.set_ylabel("kB")
# # traffic_in.set_xlabel("Time (s)")

# lat.locator_params(axis='x', nbins=10)
# # traffic_in.locator_params(axis='x', nbins=10)

# # loc = plticker.MultipleLocator(base=1.0) # this locator puts ticks at regular intervals
# # axarr.xaxis.set_major_locator(loc)


plt.legend()
plt.show()

