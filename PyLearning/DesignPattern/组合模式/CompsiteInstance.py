# -*- coding: utf-8 -*-

"""
@author: Mark Wu
@file: CompsiteInstance.py
@time: 2023/5/1 19:30
"""

# 抽象公司类
class Company(object):
    def __init__(self, name):
        self.name = name

    def Add(self, company):
        pass

    def Remove(self, company):
        pass

    def Display(self, depth):
        pass

    def LineOfDuty(self):
        pass


# 具体公司类
class ConcreteCompany(Company):
    def __init__(self, name):
        super(ConcreteCompany, self).__init__(name)
        self.__children = []

    def Add(self, company):
        self.__children.append(company)

    def Remove(self, company):
        self.__children.remove(company)

    def Display(self, depth):
        print("-"*depth + self.name)
        for company in self.__children:
            company.Display(depth+2)

    # 履行职责
    def LineOfDuty(self):
        for company in self.__children:
            company.LineOfDuty()


# 人力资源部类
class HRDepartment(Company):
    def __init__(self, name):
        super(HRDepartment, self).__init__(name)

    def Add(self, company):
        pass

    def Remove(self, company):
        pass

    def Display(self, depth):
        print("-"*depth, self.name)

    def LineOfDuty(self):
        print("%s员工招聘培训管理" % self.name)


# 财务部类
class FinanceDepartment(Company):
    def __init__(self, name):
        super(FinanceDepartment, self).__init__(name)

    def Add(self, company):
        pass

    def Remove(self, company):
        pass

    def Display(self, depth):
        print("-" * depth, self.name)

    def LineOfDuty(self):
        print("%s公司财务收支管理" % self.name)


def main():
    root = ConcreteCompany("北京总公司")
    root.Add(HRDepartment("总公司人力资源部"))
    root.Add(FinanceDepartment("总公司财务部"))

    comp = ConcreteCompany("上海华东分公司")
    comp.Add(HRDepartment("华东公司人力资源部"))
    comp.Add(FinanceDepartment("华东分公司财务部"))

    root.Add(comp)

    comp1 = ConcreteCompany("南京办事处")
    comp1.Add(HRDepartment("南京办事处人力资源部"))
    comp1.Add(FinanceDepartment("南京办事处财务部"))

    comp.Add(comp1)

    comp2 = ConcreteCompany("杭州办事处")
    comp2.Add(HRDepartment("杭州办事处人力资源部"))
    comp2.Add(FinanceDepartment("杭州办事处财务部"))
    comp.Add(comp2)

    print("-------------公司结构-------------")
    root.Display(1)

    print("-------------公司职责--------------")
    root.LineOfDuty()



if __name__ == '__main__':
    main()


