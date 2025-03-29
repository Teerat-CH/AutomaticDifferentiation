from typing import Literal, Optional, Union

Variable = str
Number = float
Operator = Literal['+', '-', '*', '/', '^']
Expression = Union[Number, Variable, Operator]

class Node:
    def __init__(self, expression = None):
        self.expression: Optional[Expression] = expression
        self.parent: Optional[Node] = None
        self.leftChild: Optional[Node] = None
        self.rightChild: Optional[Node] = None

    def setParent(self, parent: "Node"):
        self.parent = parent
    
    def setLeftChild(self, leftChild: "Node"):
        self.leftChild = leftChild

    def setRightChild(self, rightChild: "Node"):
        self.rightChild = rightChild

    def evaluate(self):
        if (self.leftChild == None and self.rightChild == None):
            if isinstance(self.expression, float):
                return self.expression # return expression if it is a number
            else:
                raise ValueError("Expected number as a leaf node")
        else:
            if self.expression in ('+', '-', '*', '/', '^'):
                leftVal = self.leftChild.evaluate()
                rightVal = self.rightChild.evaluate()

                if self.expression == '+':
                    return leftVal + rightVal
                elif self.expression == '-':
                    return leftVal - rightVal
                elif self.expression == '*':
                    return leftVal * rightVal
                elif self.expression == '/':
                    return leftVal / rightVal
                elif self.expression == '^':
                    return leftVal ** rightVal
                else:
                    raise ValueError("Unknown operator")

if __name__ == "__main__":
    node = Node()
    print(node)