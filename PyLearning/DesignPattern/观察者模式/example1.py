from abc import ABCMeta, abstractmethod


# 抽象订阅者
class Observer(metaclass=ABCMeta):
    @abstractmethod
    def update(self, notice):     # notice是一个Notice类的对象
        pass


# 抽象发布者
class Notice:
    def __init__(self):
        self.observers = []

    def attach(self, obs):
        # 添加订阅者
        self.observers.append(obs)

    def detach(self, obs):
        # 删除订阅者
        self.observers.remove(obs)

    def notify(self):
        # 通知所有的订阅者
        for obs in self.observers:
            obs.update(self)


# 具体发布者
class StaffNotice(Notice):
    def __init__(self, name: str, company_info: str = None):
        super(StaffNotice, self).__init__()
        self.name = name
        self.__company_info = company_info

    @property
    def company_info(self):
        return self.__company_info

    @company_info.setter
    def company_info(self, info):
        self.__company_info = info
        # 发布新消息并通知所有的订阅者
        self.notify()


class Staff(Observer):
    def __init__(self, name: str):
        self.name = name

    def update(self, notice: StaffNotice):
        print("{}收到{}通知，{}".format(self.name, notice.name, notice.company_info))


def main():
    notice = StaffNotice("人事", "初始公司消息")
    s1 = Staff("1号员工")
    notice.attach(s1)
    s2 = Staff("2号员工")
    notice.attach(s2)
    notice.company_info = "最新消息：公司今年业绩非常好，给大家准备了丰厚的奖金！"

    notice.detach(s2)
    notice.company_info = "最新消息：中秋和国庆放假8天"



if __name__ == '__main__':
    main()