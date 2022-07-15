from DelaunayTriangulation import triangulation
import numpy as np
import matplotlib.pyplot as plt

from scipy.spatial import Delaunay
data = np.random.randn(50 ,2)
print(data)
out = triangulation(data, 2)
out_new = out.reshape((-1,2))
out_new2 = out_new.reshape((-1, 3, 2))

print(out_new2)
plt.figure(1)
h,w,_ = out_new2.shape
for i in range(h):
    tmp = list(out_new2[i, :, 0])
    x = np.append(out_new2[i, :, 0], out_new2[i, 0, 0])
    y = np.append(out_new2[i, :, 1], out_new2[i, 0, 1])
    plt.plot(x, y)
plt.ioff()
plt.savefig('Delaunay1.png', transparent=True, dpi=600)

points = data
tri = Delaunay(points)
center = np.sum(points[tri.simplices], axis=1) / 3.0
'''
color = []
for sim in points[tri.simplices]:
    x1, y1 = sim[0][0], sim[0][1]
    x2, y2 = sim[1][0], sim[1][1]
    x3, y3 = sim[2][0], sim[2][1]

    s = ((x1-x2)**2+(y1-y2)**2)**0.5 + ((x1-x3)**2+(y1-y3)**2)**0.5 + ((x3-x2)**2+(y3-y2)**2)**0.5
    color.append(s)
color = np.array(color)
'''
color = []
for index, sim in enumerate(points[tri.simplices]):
    cx, cy = center[index][0], center[index][1]
    x1, y1 = sim[0][0], sim[0][1]
    x2, y2 = sim[1][0], sim[1][1]
    x3, y3 = sim[2][0], sim[2][1]

    s = ((x1 - cx) ** 2 + (y1 - cy) ** 2) ** 0.5 + ((cx - x3) ** 2 + (cy - y3) ** 2) ** 0.5 + (
                (cx - x2) ** 2 + (cy - y2) ** 2) ** 0.5
    color.append(s)
color = np.array(color)
plt.figure(2, figsize=(20, 10))
plt.tripcolor(points[:, 0], points[:, 1], tri.simplices.copy(), facecolors=color, edgecolors='k')
plt.tick_params(labelbottom='off', labelleft='off', left='off', right='off', bottom='off', top='off')
ax = plt.gca()
plt.scatter(points[:, 0], points[:, 1], color='r')
# plt.grid()
#plt.show()
plt.savefig('Delaunay2.png', transparent=True, dpi=600)

