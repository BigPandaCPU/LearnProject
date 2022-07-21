import numpy as np
import matplotlib.pyplot as plt

N = np.arange(-2.0, 2.0, 0.005)
Re,Im = np.meshgrid(N,N)

Z = Re + Im*1j

C = 0.156j-0.8
J = 0.0

for i in range(200):
    t = abs(Z)<=1000
    J = J+t
    Z = Z*Z+C
J_max = np.max(J)
idx_max = np.where(J==J_max)
print(np.min(J))
print(np.max(J))
KK = np.zeros_like(J)
KK[idx_max] = 1
plt.figure()
ans = plt.imshow(KK, cmap=plt.cm.gray)

plt.figure()
ans2 = plt.imshow(J, cmap=plt.cm.gray)
plt.colorbar()
plt.show()