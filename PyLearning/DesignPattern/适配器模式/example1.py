
class Synthesizer:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return 'the {} synthesizer'.format(self.name)

    def play(self):
        return 'is playing an electronic song'


class Human:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return 'the {} human'.format(self.name)

    def speak(self):
        return 'says hello'


class Computer:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return 'the {} computer'.format(self.name)

    def execute(self):
        return 'executes a program'


class Aapter:
    def __init__(self, obj, adapted_methods):
        self.obj = obj
        self.__dict__.update(adapted_methods)
        print(self.__dict__)

    def __str__(self):
        return str(self.obj)


def main():
    objects = [Computer('Asus')]
    synth = Synthesizer('moog')
    objects.append(Aapter(synth, dict(execute=synth.play)))
    human = Human('Bob')
    objects.append(Aapter(human, dict(execute=human.speak)))

    for obj in objects:
        print('{} {}'.format(str(obj), obj.execute))
        if hasattr(obj, 'name'):
            print("name =", obj.name)
        elif hasattr(obj, 'obj'):
            print("name =", obj.obj.name)



if __name__ == '__main__':
    main()

