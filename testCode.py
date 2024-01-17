from main import Documentation

docs = Documentation(authors={"Freddy":"link"})

def myFunction() -> int:
    """Returns 1"""
    return 1

class MyClass:
    def __init__(self, x:int, y:int) -> None:
        """init doc"""
        self.myX = x
        self.myY = y

    def add(self) -> int:
        """# add doc"""
        return self.myX + self.myY
    
    def sub(self) -> int:
        return self.myX - self.myY
    
class D: pass

docs.addFunction(myFunction)
docs.addClass(MyClass)

docs.start()