import example
from example import add, swap
import numpy as np

### test add ###
a = add(i=1, j=3)
print(a)
print(add(i=1, j=2))


### test swap ###
m = np.array(3)
n = np.array(4)
swap(m, n)
print("m=", m)
print("n=", n)


### test class ###
p = example.Pet()
print(p.getName())

### test Inheritance and automatic downcasting  ###

p = example.Dog("Petter")
print(p.getName())
#p.bark()

p.setName("Charly")
print(p.getName())

help(example)