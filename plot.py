import argparse
from distutils.command.build import build
from functools import total_ordering
from pprint import pprint
import sys
import fontTools
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import matplotlib.ticker as plticker
from matplotlib.patches import Patch, Polygon
import seaborn as sns
from dask import dataframe as  dd
from dask import dataframe
from time import time


"""
The csv is a truncated k6 output of the form with two waiting/dat rows repeating for each request:

http_req_connecting 1643769199 17.185348
http_req_waiting 1643769199 22.982642
data_received 1643769199 509.000000
http_req_connecting 1643769199 0.000000
...
"""

argp =argparse.ArgumentParser()
argp.add_argument("-f","--file",type=str)
argp.add_argument("--Burst",action='store_true')
argp.add_argument("--Buildup",action='store_true')
argp.add_argument("--Saturation",action='store_true')
args = argp.parse_args()
REGIME=False
logpath = args.file
if args.Buildup:
    REGIME='Buildup'
if args.Saturation:
    REGIME='Saturation'
if args.Burst:
    REGIME='Burst'


# logpath = sys.argv[1]
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
    report[t[0]]['w_min']   = min(waittimes)
    report[t[0]]['w_max']   = max(waittimes)
    report[t[0]]['traffic'] = sum(traffic)
    report[t[0]]['n_reqs']  = n_reqs

timestamps = [*map(lambda k: str( datetime.fromtimestamp(int(k)) )[-8:], report.keys())]

w_u     = np.array([* map(lambda x: x['w_u'], report.values())])
w_min   = np.array([* map(lambda x: x['w_min'], report.values())])
w_max   = np.array([* map(lambda x: x['w_max'], report.values())])
w_std   = np.array([* map(lambda x: x['w_std'], report.values())])
n_reqs  = np.array([* map(lambda x: x['n_reqs'], report.values())])
traffic = np.array([* map(lambda x: x['traffic'], report.values())])

THRESHOLD_LATENCY_MS = 2000

regimes = {
    'Saturation': [ item for sublist in [[750]*60*5, [ 750 ]] for item in sublist],
    'Burst'     : [ item for sublist in [[200]*13, [300]*10, [1500]*5, [750,750], [300]*30, [200]*60, [800]*2,[2000]*5,[1500]*5,[800]*2,[400]*10,[300]*80] for item in sublist],
    'Buildup'   : [ item for sublist in [[300]*11, [400]*40, [600]*40, [700]*10,[1000]*60,[700]*10,[600]*20,[500]*10,[400]*10,[500]*41] for item in sublist]
}



# # -⋯⋯⋅⋱⋰⋆⋅⋅⋄⋅⋅∶⋅⋅⋄▫▪▭┈┅✕⋅⋅⋄⋅⋅✕∶⋅⋅⋄⋱⋰⋯⋯⋯⋯⋅⋱⋰⋆⋅⋅⋄⋅⋅[Plots]∶⋅⋅⋄▫▪▭┈┅✕⋅⋅⋄⋅⋅✕∶⋅⋅⋄⋱⋰⋯⋯⋯⋅⋱⋰⋆⋅⋅⋄⋅⋅∶⋅⋅⋄▫▪▭┈┅✕⋅⋅⋄⋅⋅✕∶⋅⋅⋄⋱⋰⋯⋯

f, axarr = plt.subplots( nrows=2, ncols=1, figsize=(7, 7),
                       gridspec_kw={
                        #    'width_ratios': [3, 3],
                           'height_ratios': [6, 2],
                       'wspace': 0.1,
                       'hspace': 0.05},sharex=True)
lat        = axarr
timestamps = np.arange(len(timestamps))
print("FOUND TIMESTAMPS", len(timestamps))
print("REGIME len", len(regimes[REGIME]))

lat[0].plot(timestamps, w_u, 'b-',  label="Average time spent waiting")
lat[0].fill_between(timestamps,
                 w_min,
                 w_max,
                 color='b',
                 alpha=0.2)

lat[0].plot(timestamps,
         [THRESHOLD_LATENCY_MS]*len(timestamps),
         'red',
         linewidth=0.5,
         label=f"{THRESHOLD_LATENCY_MS/1000}s Threshold")

lat[0].tick_params(
    size=12,
    axis        = 'x',    # changes apply to the x-axis
    which       = 'both', # both major and minor ticks are affected
    bottom      = False,  # ticks along the bottom edge are off
    top         = False,  # ticks along the top edge are off
    labelbottom = False) # labels along the bottom edge are o
lat[0].set_ylabel('Http Request Waittime ($\it{ms}$)', fontsize=16)
# lat[0].set_title('Waiting time')


vus = axarr[1]
vus.tick_params(
    size=12,
    which       = 'both') 
vus.plot(timestamps, regimes[REGIME], 'black',linewidth=0.5)
vus.set_ylabel("Virtual Users",fontsize=16)
vus.set_xlabel('Time Elapsed ($\it{s}$)',fontsize=16)

# plt.title("Average Waiting time per second.")



# lat.set_axisbelow(True)

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

axarr[0].set_title(f"{REGIME} Regime",fontsize=20)
legendPatches = []
legendPatches.append(Patch(facecolor='royalblue', label= "Min/Max Spread"))
legendPatches.append(Patch(facecolor='blue', label= "Mean Wait-time"))
# handles, _ = axarr[0].get_legend_handles_labels()
axarr[0].legend(handles=[*legendPatches], loc='best', fontsize=14)
axarr[1].tick_params(labelsize=14)

axarr[0].grid(alpha=0.3)
axarr[1].grid(alpha=0.3)

plt.legend()
plt.show()

