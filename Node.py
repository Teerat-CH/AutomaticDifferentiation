Number = float | int
Variable = str
Operator = str
Expression = Number | Variable | Operator

class Node:
    def __init__(self, expression: Expression = None):
        self.expression = expression

    def evaluate(self):
        pass

class ConstNode(Node):
    def __init__(self, expression):
        super().__init__(expression)

    def evaluate(self):
        return self.expression
    
    def feedBackwardWith(self, value):
        pass
    
class VariableNode(Node):
    def __init__(self, expression, value):
        super().__init__(expression)
        self.value = value
        self.sum = 0

    def evaluate(self):
        return self.value
    
    def feedBackwardWith(self, value):
        self.sum += value

class AdditionNode(Node):
    def __init__(self):
        super().__init__("+")
        self.leftChild: Node = None
        self.rightChild: Node = None
        self.leftChildEvaluatedValue = None
        self.rightChildEvaluatedValue = None

    def evaluate(self):
        if self.leftChild is not None and self.rightChild is not None:
            self.leftChildEvaluatedValue = self.leftChild.evaluate()
            self.rightChildEvaluatedValue = self.rightChild.evaluate()
            return self.leftChildEvaluatedValue + self.rightChildEvaluatedValue
        
    def feedBackwardWith(self, value: Number):
        self.leftChild.feedBackwardWith(value)
        self.rightChild.feedBackwardWith(value)

    def setLeftChildToBe(self, node: Node):
        self.leftChild = node

    def setRightChildToBe(self, node: Node):
        self.rightChild = node

class MultiplicationNode(Node):
    def __init__(self):
        super().__init__("*")
        self.leftChild: Node = None
        self.rightChild: Node = None
        self.leftChildEvaluatedValue = None
        self.rightChildEvaluatedValue = None

    def evaluate(self):
        if self.leftChild is not None and self.rightChild is not None:
            self.leftChildEvaluatedValue = self.leftChild.evaluate()
            self.rightChildEvaluatedValue = self.rightChild.evaluate()
            return self.leftChildEvaluatedValue * self.rightChildEvaluatedValue
        
    def feedBackwardWith(self, value: Number):
        self.leftChild.feedBackwardWith(value * self.rightChildEvaluatedValue)
        self.rightChild.feedBackwardWith(value * self.leftChildEvaluatedValue)

    def setLeftChildToBe(self, node: Node):
        self.leftChild = node

    def setRightChildToBe(self, node: Node):
        self.rightChild = node

class ExponentNode(Node):
    def __init__(self):
        super().__init__("^")
        self.leftChild: Node = None
        self.rightChild: Node = None
        self.leftChildEvaluatedValue = None
        self.rightChildEvaluatedValue = None

    def evaluate(self):
        if self.leftChild is not None and self.rightChild is not None:
            self.leftChildEvaluatedValue = self.leftChild.evaluate()
            self.rightChildEvaluatedValue = self.rightChild.evaluate()
            return self.leftChildEvaluatedValue ** self.rightChildEvaluatedValue
        
    def feedBackwardWith(self, value: Number):
        self.leftChild.feedBackwardWith(value * (self.rightChildEvaluatedValue * (self.leftChildEvaluatedValue ** (self.rightChildEvaluatedValue - 1))))

    def setLeftChildToBe(self, node: Node):
        self.leftChild = node

    def setRightChildToBe(self, node: Node):
        self.rightChild = node

if __name__ == "__main__":
    root = AdditionNode()
    l1 = MultiplicationNode()
    r1 = MultiplicationNode()
    root.setLeftChildToBe(l1)
    root.setRightChildToBe(r1)

    l21 = ConstNode(3)
    r21 = ExponentNode()
    l1.setLeftChildToBe(l21)
    l1.setRightChildToBe(r21)

    l22 = ConstNode(2)
    r1.setLeftChildToBe(l22)

    x = VariableNode("x", 5)
    two = ConstNode(2)
    r21.setLeftChildToBe(x)
    r21.setRightChildToBe(two)
    r1.setRightChildToBe(x)

    print(root.evaluate())
    root.feedBackwardWith(1)
    print(x.sum)