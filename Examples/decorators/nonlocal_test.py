# testing nonlocal behavior:


# A triple-nested function!

s = "in global scope"


def func1():
    # global s
    # nonlocal s  # this raises an error.
    s = "in func1 scope"

    def func2():
        # global s
        # nonlocal s
        s = "in func2 scope"

        def func3():
            # global s
            # nonlocal s
            s = "in func3 scope"
            print("s in func3:", s)
            return None

        func3()
        print("s in func2:", s)
        return None
    func2()
    print("s in func1:", s)
    return None

func1()
print("in global:", s)



