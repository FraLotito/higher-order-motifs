import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sn
import math

plt.rcParams['font.size'] = 14

def lower_bound(n):
    return float(2**(2**n - 2 * n) / (math.factorial(n)))

def up_bound(n):
    return float(2**(2**n - n - 1))

c = [1, 6, 171, 611846, 200253853704319, 263735716028826427334553304608242, 5609038300883759793482640992086670066496449147691597380632107520565546]

low = [lower_bound(n) for n in range(2, len(c)+2)]
up = [up_bound(n) for n in range(2, len(c)+2)]
d = [float(i) for i in c]

fig, ax = plt.subplots()
plt.xlabel("Order")
plt.ylabel("Number of higher-order motifs")
#ax.set(yscale="symlog")
low = [math.log(i, 10) for i in low]
up = [math.log(i, 10) for i in up]
d = [math.log(i, 10) for i in d]
print(d)

sn.lineplot(y=d, x=range(2, len(d)+2), ax=ax, color='black', label='Count')
sn.lineplot(y=low, x=range(2, len(d)+2), label='Lower bound', ax=ax, color='grey', linestyle='dashed')
sn.lineplot(y=up, x=range(2, len(d)+2), label='Upper bound', ax=ax, color='grey', linestyle='dotted')

plt.fill_between(range(2, len(d)+2), up, low, color='grey', alpha=0.4)

import numpy as np

def myticks(x,pos):

    if x == 0: return "$0$"

    exponent = int(x)

    return r"$10^{{ {:2d} }}$".format(exponent)

ax.yaxis.set_major_formatter(ticker.FuncFormatter(myticks))

#plt.legend()
fig.tight_layout()
sn.despine()
plt.legend(frameon=False)
#plt.show()
plt.savefig("fig1a.pdf")