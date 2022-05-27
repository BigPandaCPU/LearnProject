#****  迭代器 demo   ****#
# class A:
#     """A实现了迭代器协议，它的实例就是一个迭代器"""
#     def __init__(self, n):
#         self.idx = 0
#         self.n = n
#     def __iter__(self,):
#         print("__iter__")
#         return self
#     def __next__(self):
#         if self.idx < self.n:
#             val = self.idx
#             self.idx += 1
#             return val
#         else:
#             raise StopIteration()
#
# a = A(3)
# for i in a:
#     print(i)
#
# for i in a:
#     print(i)

#****  可迭代对象  ****#
# 一个类是「迭代器」，那么它的实例不是一个「可迭代对象」吗
#但凡是可以返回一个「迭代器」的对象，都可以称之为「可迭代对象」

class A:
    # A是迭代器 因为它实现了 __iter__ 和__next__方法
    def __init__(self, n):
        self.idx = 0
        self.n = n

    def __iter__(self):
        return self

    def __next__(self):
        if self.idx < self.n:
            val = self.idx
            self.idx += 1
            return val
        else:
            raise StopIteration()

class B:
    #B不是迭代器
    def __init__(self, n):
        self.n = n
    def __iter__(self):
        return A(self.n)

#a是一个迭代器，同时也是一个可迭代对象
a = A(3)
for i in a:
    print(i)

print(iter(a))

#b不是迭代器，但它是可迭代对象，因为它把迭代细节交给了A
b = B(3)
for i in b:
    print(i)
print(iter(b))

