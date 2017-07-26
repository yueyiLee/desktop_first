# -*- coding: utf-8 -*-

# 把函数作为参数传入，这样的函数称为高阶函数，函数式编程就是指这种高度抽象的编程范式
def abs_add(x,y,f):
    return  f(x) + f(y)
print(abs_add(3,-4,abs))

# map()函数接收两个参数，一个是函数，一个是Iterable，map将传入的函数依次作用到序列的每个元素，并把结果作为新的Iterator返回
def f_map(x):
    return x*x
r = map(f_map,[1,2,3,4,5,6])
print(list(r))
str_map = list(map(str,[1,2,3,4,5]))
print(str_map)

# reduce把一个函数作用在一个序列[x1, x2, x3, ...]上，这个函数必须接收两个参数，
# reduce把结果继续和序列的下一个元素做累积计算，其效果就是：
from functools import reduce
def add(x,y):
    return x+y
print(reduce(add,[1,4,3,5,7]))
def fn(x,y):
    return x*10 + y
print((reduce(fn,[4,5,3,2,1])))

def str2int(s):
    def fn(x, y):
        return x * 10 + y
    def char2num(s):
        # note this:
        return {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9}[s]
    return reduce(fn, map(char2num, s))
print(str2int("3222"))

def is_odd(n):
    return n%2==0
print(list(filter(is_odd,[1,2,3,4,5])))
# 用filter求素数,使用埃氏筛法
# 生成一个无限奇数序列
def _odd_iter():
    n = 1
    while True:
        n = n+2
        yield n
def not_divisible(n):
    return lambda x: x % n >0
def main():
    yield 2
    it = _odd_iter()
    while True:
        n = next(it)
        yield n
        it = filter(not_divisible(n),it)
for n in main():
    if n < 10:
        print(n)
    else:
        break

print(sorted([2,3,-45,32,-9,88]))
# sorted()函数也是一个高阶函数，它还可以接收一个key函数来实现自定义的排序
print(sorted([2,3,-45,32,-9,88],key=abs))
print(sorted(['bob', 'about', 'Zoo', 'Credit'], key=str.lower,reverse=True))

# 如果不需要立刻求和，而是在后面的代码中，根据需要再计算怎么办？可以不返回求和的结果，而是返回求和的函数
def lazy_sum(*arg):
    def sum():
        ax = 0
        for n in arg:
            ax = ax + n
        return ax
    return sum
f = lazy_sum(1,2,3,4,5)
# 我们在函数lazy_sum中又定义了函数sum，并且，内部函数sum可以引用外部函数lazy_sum的参数和局部变量，当lazy_sum返回函数sum时，
# 相关参数和变量都保存在返回的函数中，这种称为“闭包（Closure）”的程序结构拥有极大的威力
print(f())   # 最后调用了一下f才能返回真正的求和结果,arg的内容也跟着传进来了，不用再调用f时再写一遍参数

# 返回函数不要引用任何循环变量，或者后续会发生变化的变量。
# 如果一定要引用循环变量怎么办？方法是再创建一个函数，用该函数的参数绑定循环变量当前的值，
# 无论该循环变量后续如何更改，已绑定到函数参数的值不变：
def count():
    def f(j):
        def g():
            return j*j
        return g
    fs = []
    for i in range(1,4):
        fs.append(f(i))
    return fs
# 用lambada改写一下，能简洁一些
def count1():
    f = lambda j:(lambda :j*j)
    fs = []
    for i in range(1, 4):
        fs.append(f(i))
    return fs
f1,f2,f3 = count1()
print(f1(),f2(),f3())

# 定义一个能打印日志的decorator
def log(func):
    def wrapper(*arg,**kw):
        print("we will call %s" %func.__name__)
        return func(*arg,**kw)
    return wrapper
# 把该装饰器放在函数定义的前面
import time
@log
def now():
    print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
now()
# 如果decorator本身需要传入参数，那就需要编写一个返回decorator的高阶函数，写出来会更复杂。比如，要自定义log的文本
import functools
def log(text):
    def decorator(func):
        # 函数也是对象，它有__name__等属性，但你去看经过decorator装饰之后的函数，它们的__name__已经从原来的'now'变成了'wrapper';
        # 返回的那个wrapper()函数名字就是'wrapper'，所以，需要把原始函数的__name__等属性复制到wrapper()函数中，否则，有些依赖函数签名的代码执行就会出错。
        # 不需要编写wrapper.__name__ = func.__name__这样的代码，Python内置的functools.wraps就是干这个事的，所以，一个完整的decorator的写法如下：
        @functools.wraps(func)
        def wrapper(*arg,**kw):
            print("%s  %s" %(text,func.__name__))
            return func(*arg,**kw)
        return wrapper
    return decorator
# 把这个三层的装饰器放在函数定义前面，给出text，如果必要的话
@log("三层嵌套")
def now():
    print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
now()

