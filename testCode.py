from main import Documentation

authors = {
    "Freddy" : "https://github.com/FreddyPashley"
}

docs = Documentation("My Library's Docs", authors=authors)


def mulTwoNums(x:int, y:int) -> float:
    return float(x * y)

docs.addFunction(mulTwoNums, credit="Freddy")


def anotherFunction(arg1, arg2, arg3):
    return arg1 == arg2 == arg3

docs.addFunction(anotherFunction)


docs.start()

# Main
print(mulTwoNums(2, 3))












# def addTwoNums(x:int, y:int) -> int:
#     """
#     # Subtitle
#     text
#     # Subtitle 2
#     1. op1
#     2. op2
#     3. op3
#     """
#     return x + y

# docs.addFunction(addTwoNums)