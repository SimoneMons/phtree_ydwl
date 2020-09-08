class Rectangle:
    def __init__(self, length, width):
        self.length = length
        self.width = width

    def area(self):
        return self.length * self.width

    def perimeter(self):
        return 2 * self.length + 2 * self.width



class Area(Rectangle):
    def __init__(self, aa, bb, cc):
        super().__init__(aa, bb)
        self.aa = aa
        self.bb = bb
        self.cc = cc

        print(cc +2)



square = Area(7, 5, 10)
print(square.perimeter())
print(square.area())


def print_kwargs(**kwargs):
    print(kwargs)


print_kwargs(kfwargs1="Shark", kfwargs2=4.5, kfwargs4=True)

class Shark:
    def __init__(self, *args):
        print('Hola Mons')
        self.name = args[1]
        print('name is ', self.name)

    def swim(self):
        print("The shark is swimming.")

    def be_awesome(self):
        print("The shark is being awesome.")


def main():
    sammy = Shark('pippo', 'pippo2')
    sammy.swim()
    sammy.be_awesome()

if __name__ == "__main__":
    main()
