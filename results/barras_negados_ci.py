# Douglas D. Lieira <douglas.lieira@unesp.br>

import resSim1 as sim1
import resSim2 as sim2
import resSim3 as sim3
import resSim4 as sim4
import resSim5 as sim5
import random
import time
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import scipy.stats

def mean_confidence_interval(data, confidence=0.95):
    a = 1.0 * np.array(data)
    n = len(a)
    m, se = np.mean(a), scipy.stats.sem(a)
    h = se * scipy.stats.t.ppf((1 + confidence) / 2., n-1)
    return m, m-h, m+h, h*6

numDevices = [sim1.nDevices, sim2.nDevices, sim3.nDevices, sim4.nDevices, sim5.nDevices]

NegadosGreedy = []
NegadosGreedy.append(np.average(sim1.Negados[0]))
NegadosGreedy.append(np.average(sim2.Negados[0]))
NegadosGreedy.append(np.average(sim3.Negados[0]))
NegadosGreedy.append(np.average(sim4.Negados[0]))
NegadosGreedy.append(np.average(sim5.Negados[0]))

NegadosReliable = []
NegadosReliable.append(np.average(sim1.Negados[1]))
NegadosReliable.append(np.average(sim2.Negados[1]))
NegadosReliable.append(np.average(sim3.Negados[1]))
NegadosReliable.append(np.average(sim4.Negados[1]))
NegadosReliable.append(np.average(sim5.Negados[1]))

NegadosWOA = []
NegadosWOA.append(np.average(sim1.Negados[2]))
NegadosWOA.append(np.average(sim2.Negados[2]))
NegadosWOA.append(np.average(sim3.Negados[2]))
NegadosWOA.append(np.average(sim4.Negados[2]))
NegadosWOA.append(np.average(sim5.Negados[2]))


NomesMetodos = ['Greedy', 'Reliable', 'TRIAD']

ci_NegadosGreedy = []
ci_NegadosGreedy.append(mean_confidence_interval(sim1.Negados[0])[3])
ci_NegadosGreedy.append(mean_confidence_interval(sim2.Negados[0])[3])
ci_NegadosGreedy.append(mean_confidence_interval(sim3.Negados[0])[3])
ci_NegadosGreedy.append(mean_confidence_interval(sim4.Negados[0])[3])
ci_NegadosGreedy.append(mean_confidence_interval(sim5.Negados[0])[3])

ci_NegadosReliable = []
ci_NegadosReliable.append(mean_confidence_interval(sim1.Negados[1])[3])
ci_NegadosReliable.append(mean_confidence_interval(sim2.Negados[1])[3])
ci_NegadosReliable.append(mean_confidence_interval(sim3.Negados[1])[3])
ci_NegadosReliable.append(mean_confidence_interval(sim4.Negados[1])[3])
ci_NegadosReliable.append(mean_confidence_interval(sim5.Negados[1])[3])
     
ci_NegadosWOA = []
ci_NegadosWOA.append(mean_confidence_interval(sim1.Negados[2])[3])
ci_NegadosWOA.append(mean_confidence_interval(sim2.Negados[2])[3])
ci_NegadosWOA.append(mean_confidence_interval(sim3.Negados[2])[3])
ci_NegadosWOA.append(mean_confidence_interval(sim4.Negados[2])[3])
ci_NegadosWOA.append(mean_confidence_interval(sim5.Negados[2])[3])

labels = numDevices

x = np.arange(len(labels))  # the label locations
width = 0.28  # the width of the bars

r1 = np.arange(len(labels))
r2 = [x + width for x in r1]
r3 = [x + width for x in r2]


fig, ax = plt.subplots()
rects1 = ax.bar(r1, NegadosGreedy, width, color='blue', label='Greedy', yerr = ci_NegadosGreedy)
rects2 = ax.bar(r2, NegadosReliable, width, color='steelblue', label='Reliable',yerr = ci_NegadosReliable)
rects3 = ax.bar(r3, NegadosWOA, width, color='darkblue', label='TRIAD', yerr = ci_NegadosWOA)


# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Número de serviços negados', fontsize=12, fontweight='bold')
#ax.set_title('Denied Services')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()


def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = int(rect.get_height())
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 20),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')


fig.tight_layout()
plt.legend(loc='best', fontsize=12)
plt.xlabel("Número de dispositivos", fontsize=12, fontweight='bold')
plt.tick_params(axis='both', labelsize=12)

plt.show()