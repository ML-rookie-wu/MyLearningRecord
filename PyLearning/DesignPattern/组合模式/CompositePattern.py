# -*- coding: utf-8 -*-

"""
@author: Mark Wu
@file: CompositePattern.py
@time: 2023/5/1 16:36
"""

"""
组合模式：将对象组合成树型结构以表示‘部分-整体’的层次结构。组合模式使得用户对单个对象和组合对象的使用具有一致性
"""



class Component(object):

    def __init__(self, name):
        self.name = name

    def Add(self, component):
        pass

    def Remove(self, component):
        pass

    def Display(self, depth):
        pass


class Leaf(Component):
    def __init__(self, name):
        super(Leaf, self).__init__(name)

    def Add(self, component):
        print("Cannot add to leaf")

    def Remove(self, component):
        print("Cannot remove from leaf")

    def Display(self, depth):
        print("-"*depth + self.name)


class Composite(Component):
    def __init__(self, name):
        super(Composite, self).__init__(name)
        self.__children = []

    def Add(self, component):
        self.__children.append(component)

    def Remove(self, component):
        self.__children.remove(component)

    def Display(self, depth):
        print("-"*depth + self.name)
        for component in self.__children:
            component.Display(depth+2)


def main():
    root = Composite("root")
    root.Add(Leaf("Leaf A"))
    root.Add(Leaf("Leaf B"))

    comp = Composite("Compsite X")
    comp.Add(Leaf("Leaf XA"))
    comp.Add(Leaf("Leaf XB"))

    root.Add(comp)

    comp2 = Composite("Compsite XY")
    comp2.Add(Leaf("Leaf XYA"))
    comp2.Add(Leaf("Leaf XYB"))

    comp.Add(comp2)

    root.Add(Leaf("Leaf C"))

    leaf = Leaf("Leaf D")
    root.Add(leaf)

    root.Display(1)
    root.Remove(leaf)

    print("####################################")
    root.Display(1)


if __name__ == '__main__':
    main()


