
class TestA:
    def __init__(self):
        pass

    def __del__(self):
        print("----------------调用TestA中的del方法----------")

    def __enter__(self):
        print("-------------调用TestA中的enter方法----------------")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("---------------调用TestA中的exit方法----------------")


class TestB:
    def __init__(self):
        pass

    def __enter__(self):
        print("------------调用TestB中的enter方法------------")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("---------------调用TestB中的exit方法-----------------")

    def __del__(self):
        print("---------------调用TestB中的del方法-------------------")


class Test:

    def __init__(self):
        self.a = TestA()
        self.b = TestB()
        print("-----------调用init方法-----------")

    def __enter__(self):
        print("-------------调用enter方法---------------")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("----------------调用exit方法-------------")

    def __del__(self):
        print("-------------调用del方法--------------")

    def test_api(self):
        print("---------------调用api------------------")
        # print(1 / 0)


def main():
    t = Test()
    t.test_api()
    print(t.__dict__)
    print(t.__class__.__name__)
    print(Test.__dict__)
    print(Test.__name__)

    # with Test() as t:
    #     t.test_api()

if __name__ == '__main__':

    main()
