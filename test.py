def myFunc(x, y=True):
    return x if y else 1

print(myFunc.__code__.co_code)