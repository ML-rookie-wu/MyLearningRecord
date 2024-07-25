from abc import ABCMeta, abstractmethod


class Request:
    def __init__(self):
        self.__requestType = None
        self.__requestContent = None
        self.__number = None

    @property
    def request_type(self):
        return self.__requestType

    @request_type.setter
    def request_type(self, value: str):
        self.__requestType = value

    @property
    def requset_content(self):
        return self.__requestContent

    @requset_content.setter
    def request_content(self, content: str):
        self.__requestContent = content

    @property
    def number(self):
        return self.__number

    @number.setter
    def number(self, num: int):
        self.__number = num


class Manager(metaclass=ABCMeta):
    def __init__(self, name):
        self.__superior = None
        self.name = name

    @property
    def superior(self):
        return self.__superior

    @superior.setter
    def superior(self, superior):
        self.__superior = superior

    @abstractmethod
    def handle_request(self, request: Request):
        pass


# 经理
class CommonManager(Manager):
    def __init__(self, name):
        super().__init__(name)

    def handle_request(self, request: Request):
        if request.request_type == "请假" and request.number <= 2:
            print("{}: {} 数量{} 被批准".format(self.name, request.request_content, request.number))
        else:
            if self.superior is not None:
                self.superior.handle_request(request)


# 总监
class Majordomo(Manager):
    def __init__(self, name):
        super().__init__(name)

    def handle_request(self, request: Request):
        if request.request_type == "请假" and 2 < request.number <= 5:
            print("{}: {} 数量{} 被批准".format(self.name, request.request_content, request.number))
        else:
            if self.superior is not None:
                self.superior.handle_request(request)


# 总经理
class GeneralManager(Manager):
    def __init__(self, name):
        super().__init__(name)

    def handle_request(self, request: Request):
        if request.request_type == "请假":
            print("{}: {} 数量{} 被批准".format(self.name, request.request_content, request.number))

        elif request.request_type == "加薪" and request.number <= 500:
            print("{}: {} 数量{} 被批准".format(self.name, request.request_content, request.number))

        elif request.request_type == "加薪" and request.number > 500:
            print("{}: {} 数量{} 再说吧".format(self.name, request.request_content, request.number))

        else:
            if self.superior is not None:
                self.superior.handle_request(request)


def main():
    jingli = CommonManager("经理")
    zongjian = Majordomo("总监")
    zongjingli = GeneralManager("总经理")

    jingli.superior = zongjian
    zongjian.superior = zongjingli

    request = Request()
    request.request_type = "请假"
    request.request_content = "小菜请假"
    request.number = 1
    jingli.handle_request(request)

    request = Request()
    request.request_type = "请假"
    request.request_content = "小菜请假"
    request.number = 4
    jingli.handle_request(request)

    request = Request()
    request.request_type = "加薪"
    request.request_content = "小菜请求加薪"
    request.number = 500
    jingli.handle_request(request)

    request = Request()
    request.request_type = "加薪"
    request.request_content = "小菜请求加薪"
    request.number = 1000
    jingli.handle_request(request)


if __name__ == '__main__':
    main()