

class Target:
    def request(self):
        print("普通请求")


class Adaptee:
    def request(self):
        print("特殊请求")


class Adapter(Target):
    def __init__(self):
        self.adapter = Adaptee()

    def request(self):
        self.adapter.request()


if __name__ == '__main__':

    taget = Adapter()
    taget.request()