import numpy as np
import matplotlib.pyplot as plt

N = np.arange(-2.0, 2.0, 0.001)
Re,Im = np.meshgrid(N,N)

Z = Re + Im*1j

C = 0.156j-0.8
J = 0.0

for i in range(200):
    t = abs(Z)<=2
    J = J+t
    Z = Z*Z+C
print(np.min(J))
print(np.max(J))
ans = plt.imshow(J, cmap=plt.cm.jet)
plt.colorbar()
plt.show()