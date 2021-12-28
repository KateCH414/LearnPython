# --*-- coding:utf-8 --*--


def test(*args):
    print("run")
    print(args[0]+args[1])

if __name__ == '__main__':

    test("1","2")