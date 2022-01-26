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
df       = pd.read_csv(logspath,delimiter=' ',lineterminator="\n", header=None)

report={

}

for index, row in df.iterrows():
    [field ,timestamp, value ] = row
    if timestamp not in report:
        report[timestamp] ={
            "inbound": [],
            "wait" : [],
        }

    else:
        if field =='data_received':
            report[timestamp]['inbound'].append(value)
        elif field =='http_req_waiting':
            report[timestamp]['wait'].append(value)


# [1643101997, 1643101998, 1643101999, 1643102000, 1643102001, 1643102002, 1643102003,
# 1643102004, 1643102005, 1643102006, 1643102007, 1643102008, 1643102009, 1643102010,
# 1643102011, 1643102012, 1643102013, 1643102014, 1643102015, 1643102016, 1643102017,
# 1643102018, 1643102019, 1643102020, 1643102021, 1643102022, 1643102023, 1643102024,
# 1643102025, 1643102026, 1643102027, 1643102028]

for t in report.items():

    waittimes = t[1]['wait']
    traffic   = t[1]['inbound']
    std  = np.std(waittimes)
    mean = np.mean(t[1]['wait'])
    report[t[0]]['mean'] = mean
    report[t[0]]['std']  = std


    # print(t[0], mean, p5, p95)


# for t in report.keys():
#     timestamp = str(datetime.fromtimestamp(t))[-8:]
#     report[timestamp] = report.pop(t)

timestamps = [*report.keys()]
means      = np.array([* map(lambda x: x['mean'], report.values()) ])
stds       = np.array([* map(lambda x: x['std'], report.values()) ])

# print("tst len: ", len(timestamps))
# print("measn len: ", len(means))
# print("5s len: ", len(p5s))
# print("95s len: ", len(p95s))



plt.plot(timestamps, [2000]*len(timestamps), '-', color='red', label="2s Threshold")
plt.plot(timestamps, means, 'b-', label="wait_mean")
plt.fill_between(timestamps, means-stds, means+stds, color='b', alpha=0.1)

plt.xlabel("Time elapsed (s)")
plt.ylabel("Request waittime (ms) ")
plt.show()


print("Mean", np.mean(report[1643102018]['wait']))
print("Q95: ",np.percentile(report[1643102028]['wait'], 95))

