
from abc import ABCMeta, abstractmethod


class Handler(metaclass=ABCMeta):
    def __init__(self):
        self.__successor = None

    @property
    def successor(self):
        return self.__successor

    @successor.setter
    def successor(self, succesor):
        self.__successor = succesor

    @abstractmethod
    def handle_request(self, request):
        pass


class ConcreteHandler1(Handler):
    def __init__(self):
        super().__init__()

    def handle_request(self, request: int):
        if 0 <= request < 10:
            print("{} 处理请求 {}".format(self.__class__.__name__, request))
        elif self.successor is not None:
            # 将请求传递给继任者处理
            self.successor.handle_request(request)


class ConcreteHandler2(Handler):
    def __init__(self):
        super().__init__()

    def handle_request(self, request: int):
        if 10 <= request < 20:
            print("{} 处理请求 {}".format(self.__class__.__name__, request))
        elif self.successor is not None:
            # 将请求传递给继任者处理
            self.successor.handle_request(request)


class ConcreteHandler3(Handler):
    def __init__(self):
        super().__init__()

    def handle_request(self, request: int):
        if 20 <= request < 30:
            print("{} 处理请求 {}".format(self.__class__.__name__, request))
        elif self.successor is not None:
            # 将请求传递给继任者处理
            self.successor.handle_request(request)


def main():
    h1 = ConcreteHandler1()
    h2 = ConcreteHandler2()
    h3 = ConcreteHandler3()
    h1.successor = h2
    h2.successor = h3

    request = [2, 5, 14, 22, 18]

    for req in request:
        # 从h1开始处理请求
        h1.handle_request(req)


if __name__ == '__main__':
    # main()
    a = [1, 6, 0, 0]
    print(hex(int.from_bytes(bytes(a), byteorder='little')))