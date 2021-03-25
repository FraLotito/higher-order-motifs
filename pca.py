from sklearn.decomposition import PCA
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#pacs
a = [0, 0, 0, 0.48539389488448925, 0, 0]
a = [0, 0, 0, 3.430109657710983, 0, 0]
#gene
b = [24.15241434774379, 9.346692235101406, 0, -3.5635211304856176, 3.919647479510927, -25.57010162450236]
b = [164.5240610569368, 0, 0, -6.32693022543493, 9.666666666666664, -180.85399267549136]
#high school
c = [-15.490198605529837, -12.410620954294586, 19.65294014032862, -15.40423222226839, 43.41559716026545, -28.08970076578584]
c = [-21.26370056450929, 13.351756271215413, 627.605533661354, -29.28535324096598, 93.31642306656465, -55.93042505458853]
#primary school
d = [-17.84776245695374, -17.964174315974528, 20.6223851433552, 6.082124438608815, 24.267403642840204, -11.047637970199183]
d = [-47.48494322164263, -16.391253096136605, 531.0713110164197, 12.384777138479384, 104.80165863967497, -50.23805670876437]
#conference
e = [-9.249133559457798, -2.510394780108452, 12.10375164853077, 12.931329216530694, 20.28445381815711, -14.095724784575827]
e = [-13.487985104919408, 30.792415803889398, 191.0932639158657, 32.61144841075427, 27.600654201422305, -37.552726270432046]
#workplace
f = [-3.34304606880207, -0.7559289460184544, 40.75, 0.44470757094656654, 33.451910790649556, -6.540988486975065]
f = [-4.311106048233565, -0.4155813868856493, 50.65390588906428, 1.6112974628479158, 28.05905416979542, -7.709772204801725]
#hospital
g = [-17.787976484276285, -15.012986144801719, 41.88467345919259, 24.21882825675594, 32.18664535609761, -9.782477005497382]
g = [-12.487617629452222, -20.96374300871128, 39.762792803281684, 21.645636630173257, 29.458621028437946, -15.678589918043707]
#justice
h = [-13.952192194835186, -3.072710824687064, 88.11885401225116, -3.7293336429411617, 0.6614149259837622, -9.247931711483096]
h = [-10.975295853299073, -1.8695203209925157, 82.03462515000787, -3.1777015710605894, 0.8582827904817272, -15.854526814904174]
#babbuini
j = [-4.909601277515793, -8.491406212215221, 17.83690747413257, -10.531720942189885, 14.28328936948192, -2.1464012781135837]
j = [-4.565550650202703, -11.62232469743248, 21.270531262016164, -22.788209475586335, 9.948669439051884, -2.848546842553079]

z = [a,b,c,d,e,f,g, h, j]
labels = ['PACS', 'Gene', 'HS', 'PS', 'Conf', 'Work', 'Hosp', 'Just', 'Bab']


pca = PCA(n_components=2)
pca_result = pca.fit(z)

fig = plt.figure(figsize = (8,8))
ax = fig.add_subplot(1,1,1) 
ax.set_xlabel('Principal Component 1', fontsize = 15)
ax.set_ylabel('Principal Component 2', fontsize = 15)
ax.set_title('2 component PCA', fontsize = 20)
ax.grid()

import numpy as np
for i in range(len(z)):
    I = pca.transform(np.array(z[i]).reshape((1, -1)))[0]
    ax.scatter(I[0], I[1], label=labels[i])

ax.legend()
plt.show()



from scipy.cluster.hierarchy import dendrogram

def plot_dendrogram(model, **kwargs):
    # Create linkage matrix and then plot the dendrogram

    # create the counts of samples under each node
    counts = np.zeros(model.children_.shape[0])
    n_samples = len(model.labels_)
    for i, merge in enumerate(model.children_):
        current_count = 0
        for child_idx in merge:
            if child_idx < n_samples:
                current_count += 1  # leaf node
            else:
                current_count += counts[child_idx - n_samples]
        counts[i] = current_count

    linkage_matrix = np.column_stack([model.children_, model.distances_,
                                      counts]).astype(float)

    # Plot the corresponding dendrogram
    dendrogram(linkage_matrix, **kwargs)

from sklearn.cluster import AgglomerativeClustering

model = AgglomerativeClustering(distance_threshold=0, n_clusters=None, affinity='cosine', linkage='average')
model = model.fit(z)
plot_dendrogram(model, truncate_mode='level', p=10, labels=labels)

plt.show()

