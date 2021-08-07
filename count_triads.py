from loaders import *
from utils import *
import seaborn as sn

plt.rcParams['font.size'] = 16


def load(ds):
    if ds == 'hs':
        d = load_high_school_duplicates(3)
    elif ds == 'ps':
        d = load_primary_school_duplicates(3)
    elif ds == 'hp':
        d = load_hospital_duplicates(3)
    elif ds == 'conf':
        d = load_conference_duplicates(3)
    elif ds == 'work':
        d = load_workplace_duplicates(3)
    m = {}
    E = {}

    res = {}
    res[0] = []
    res[1] = []
    res[2] = []
    res[3] = []

    for e in d:
        if len(e) == 3:
            k = tuple(sorted(e))
            if k in m:
                m[k] += 1
            else:
                m[k] = 1
        
        if len(e) == 2:
            E[tuple(sorted(e))] = 1

    for e in m:
        nodes = list(e)
        nodes = tuple(sorted(tuple(nodes)))
        p_nodes = power_set(nodes)
                
        c = 0
        for edge in p_nodes:
            if len(edge) == 2 and tuple(sorted(edge)) in E:
                c += 1
        res[c].append(m[e])

    R = []
    S = []
    for k in res:
        if len(res[k]) > 0:
            R.append(np.mean(res[k]))
            S.append(np.std(res[k]) / len(res[k]))
        else:
            R.append(0)
            S.append(0)

    return np.array(R), np.array(S)


r, s = load('hs')
        
plt.ylim(0, 5)
plt.ylabel("Weight of group interactions")
plt.xticks(range(4), [])
plt.plot(r, color='orange', label='High School')
plt.fill_between(range(len(r)), r-s, r+s, alpha = 0.25, color='orange')

r, s = load('ps')

plt.plot(r, color='blue', label='Primary School')
plt.fill_between(range(len(r)), r-s, r+s, alpha = 0.25, color='blue')

r, s = load('hp')

plt.plot(r, color='grey', label='Hospital')
plt.fill_between(range(len(r)), r-s, r+s, alpha = 0.25, color='grey')

r, s = load('conf')

plt.plot(r, color='red', label='Conference')
plt.fill_between(range(len(r)), r-s, r+s, alpha = 0.25, color='red')

r, s = load('work')

plt.plot(r, color='purple', label='Workplace')
plt.fill_between(range(len(r)), r-s, r+s, alpha = 0.25, color='purple')

plt.legend(frameon=False)
sn.despine()
plt.savefig("fig3a_pre.pdf")