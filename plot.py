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

argp.add_argument("--wasmonly",action='store_true')
argp.add_argument("--nowasm",  action='store_true')

argp.add_argument("--Bursts",action='store_true')
argp.add_argument("--Buildup",action='store_true')
argp.add_argument("--Saturation",action='store_true')
args = argp.parse_args()
REGIME=False
logpath = args.file
if args.Buildup:
    REGIME='Buildup'
if args.Saturation:
    REGIME='Saturation'
if args.Bursts:
    REGIME='Bursts'


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
      'Saturation': [ item for sublist in [[800]*60*30,[800,800] ] for item in sublist],
      'saturation_wasmonly'  : [ item for sublist in [[800]*60*30,[800,800] ] for item in sublist],

      'Bursts'      : [ item for sublist in [
          [400]*121, 
          [200]*10, [800]*5, [1700]*5, [1500]*5,[800]*5, [400]*120,
          [200]*10, [800]*5, [1500]*5, [1700]*5, [1500]*5, [800]*5, [400]*120,
          [200]*10, [800]*5, [1700]*5, [1500]*5,[800]*5,[750]*5, [400]*120,
          ] for item in sublist],
      'bursts_wasmonly'    : [ item for sublist in [
          [400]*120, 
          [200]*10, [800]*5, [1700]*5, [1500]*5,[800]*5, [400]*120,
          [200]*10, [800]*5, [1500]*5, [1700]*5, [1500]*5, [800]*5, [400]*120,
          [200]*10, [800]*5, [1700]*5, [1500]*5,[800]*5,[750]*5, [400]*120,
          ] for item in sublist],

      'Buildup'     : [ item for sublist in [
            [300]*62, [400]*60,[500]*60,[600]*60,[700]*60,[800]*60,[900]*60,[1000]*60,#...
            [800]*10,[600]*10, [400]*10,
            [300]*60, [400]*60,[500]*60,[600]*60,[700]*60,[800]*60,[900]*60,[1000]*60,#...
            [800]*10,[600]*10, [400]*10,
            [300]*60, [400]*60,[500]*60,[600]*60,[700]*60,[800]*60,[900]*60,[1000]*60,#...
            [800]*10,[600]*10, [400]*10,
          ] for item in sublist],
      'buildup_wasmonly'   : [ item for sublist in [
            [300]*60, [400]*60,[500]*60,[600]*60,[700]*60,[800]*60,[900]*60,[1000]*60,#...
            [800]*10,[600]*10, [400]*10,
            [300]*60, [400]*60,[500]*60,[600]*60,[700]*60,[800]*60,[900]*60,[1000]*60,#...
            [800]*10,[600]*10, [400]*10,
            [300]*60, [400]*60,[500]*60,[600]*60,[700]*60,[800]*60,[900]*60,[1000]*60,#...
            [800]*10,[600]*10, [400]*10,
          ] for item in sublist]
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

lat[0].tick_params(
    size=12,
    axis        = 'y',    # changes apply to the x-axis
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

annotation = """ 
[{} endpoints]
AWS rx5large | 4 core/16GB
Intel(R) Xeon(R) Platinum 8259CL CPU @ 2.50GHz
""".format( "Only /wasm" if args.wasmonly else "Only non-/wasm")
 
axarr[0].text(0.05, 0.90, annotation, transform=axarr[0].transAxes, fontsize=16,
        verticalalignment='top')


axarr[0].set_title(f"{REGIME}",fontsize=20)
legendPatches = []
legendPatches.append(Patch(facecolor='royalblue', label= "Min/Max Spread"))
legendPatches.append(Patch(facecolor='blue', label= "Mean Wait-time"))
# handles, _ = axarr[0].get_legend_handles_labels()
axarr[0].legend(handles=[*legendPatches], loc='best', fontsize=14)
axarr[0].tick_params(labelsize=14)
axarr[1].tick_params(labelsize=14)

axarr[0].grid(alpha=0.3)
axarr[1].grid(alpha=0.3)

plt.legend()
plt.show()

