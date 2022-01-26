from itertools import tee
import os
import json
import sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import seaborn as sns
sns.set_theme(style="darkgrid")


logspath = sys.argv[1]
df = pd.read_csv(logspath, delimiter=' ', lineterminator="\n", header=None)
report = {}

for index, row in df.iterrows():
    [field, timestamp, value] = row
    if timestamp not in report:
        report[timestamp] = {
            "inbound": [],
            "wait": [],
        }

    else:
        if field == 'data_received':
            report[timestamp]['inbound'].append(value)
        elif field == 'http_req_waiting':
            report[timestamp]['wait'].append(value)

for t in report.items():

    # --+-+-+--+-+-+-+-+-+-
    waittimes = t[1]['wait']
    traffic   = t[1]['inbound']
    # -+-+-+--+-+-+--+-+-+-

    n_reqs = len(t[1]['wait'])
    w_std  = np.std(waittimes)
    w_u    = np.mean(t[1]['wait'])


    report[t[0]]['w_u']     = w_u
    report[t[0]]['w_std']   = w_std
    report[t[0]]['traffic'] = sum(traffic)
    report[t[0]]['n_reqs']  = n_reqs


timestamps = [*report.keys()]
<<<<<<< HEAD
means      = np.array([* map(lambda x: x['mean'], report.values()) ])
stds       = np.array([* map(lambda x: x['std'], report.values()) ])

# print("tst len: ", len(timestamps))
# print("measn len: ", len(means))
# print("5s len: ", len(p5s))
# print("95s len: ", len(p95s))
=======
w_u        = np.array([* map(lambda x: x['w_u'], report.values())])
w_std      = np.array([* map(lambda x: x['w_std'], report.values())])
n_reqs     = np.array([* map(lambda x: x['n_reqs'], report.values())])
traffic    = np.array([* map(lambda x: x['traffic'], report.values())])

THRESHOLD_LATENCY_MS = 2000
>>>>>>> 9fd65a0fe04e47513bafcfe4c95bcab87ef52539

# -⋯⋯⋅⋱⋰⋆⋅⋅⋄⋅⋅∶⋅⋅⋄▫▪▭┈┅✕⋅⋅⋄⋅⋅✕∶⋅⋅⋄⋱⋰⋯⋯⋯⋯⋅⋱⋰⋆⋅⋅⋄⋅⋅[Plots]∶⋅⋅⋄▫▪▭┈┅✕⋅⋅⋄⋅⋅✕∶⋅⋅⋄⋱⋰⋯⋯⋯⋅⋱⋰⋆⋅⋅⋄⋅⋅∶⋅⋅⋄▫▪▭┈┅✕⋅⋅⋄⋅⋅✕∶⋅⋅⋄⋱⋰⋯⋯

f, axarr = plt.subplots(2, sharex=True)

lat = axarr[0]
lat.plot(timestamps, w_u, 'b-', label="wait_mean")
lat.set_title('Waiting time')
lat.fill_between(timestamps, w_u-w_std, w_u+w_std, color='b', alpha=0.2)
lat.plot(timestamps, [THRESHOLD_LATENCY_MS]*len(timestamps),'-', color='red', label=f"{THRESHOLD_LATENCY_MS/1000}s Threshold")
lat.set_ylabel('Http Request Waittime (ms)')

_twinx_n_reqs = lat.twinx()
_twinx_n_reqs.plot(timestamps,n_reqs, color='blue', alpha=0.6 )


traffic_in = axarr[1]
traffic_in.plot(timestamps, traffic/1024, color='black', alpha=0.2)
traffic_in.set_title('Inbound Traffic')
traffic_in.set_ylabel("kB")

plt.show()

