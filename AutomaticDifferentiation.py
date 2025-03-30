from Node import Node, ConstNode, VariableNode, AdditionNode, MultiplicationNode, ExponentNode
from ExpressionTree import ExpressionTree

Number = float | int
Variable = str
Operator = str
Expression = Number | Variable | Operator

class AutomaticDifferentiation:
    def __init__(self):
        self.variables = {"name": Node()}
        self.expressionTree = None
        self.evaluated = False

    def parse(self, string, variableValues):
        self.expressionTree = ExpressionTree()
        self.expressionTree.build(string, variableValues)
    
    def diffWRT(self, variableName):
        if not self.evaluated:
            self.expressionTree.root.evaluate()
            self.expressionTree.root.feedBackwardWith(1)
        return self.variables[variableName].sum
    
if __name__ == "__main__":
    AD = AutomaticDifferentiation() # 3x^2 + 2x

    root = AdditionNode()
    l1 = MultiplicationNode()
    r1 = MultiplicationNode()
    root.setLeftChildToBe(l1)
    root.setRightChildToBe(r1)

    l21 = ConstNode(3)
    r21 = ExponentNode(2)
    l1.setLeftChildToBe(l21)
    l1.setRightChildToBe(r21)

    l22 = ConstNode(2)
    r1.setLeftChildToBe(l22)

    x = VariableNode("x", 5)
    AD.variables["x"] = x
    r21.setChildToBe(x)
    r1.setRightChildToBe(x)

    et = ExpressionTree()
    et.root = root
    AD.expressionTree = et
    
    print(AD.diffWRT("x"))