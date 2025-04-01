from Node import Node, ConstNode, VariableNode, AdditionNode, MultiplicationNode, ExponentNode
from ExpressionTree import ExpressionTree

Number = float | int
Variable = str
Operator = str
Expression = Number | Variable | Operator

class AutomaticDifferentiation:
    def __init__(self):
        self.variables = None
        self.expressionTree = None
        self.evaluated = False

    def parse(self, string, variableValues):
        self.expressionTree = ExpressionTree()
        self.variables = variableValues
        self.expressionTree.build(string, variableValues)
    
    def diffWRT(self, variableName):
        if not self.evaluated:
            self.expressionTree.root.evaluate()
            self.expressionTree.root.feedBackwardWith(1)
        if variableName in self.variables:
            return self.variables[variableName].sum
        return 0
    
if __name__ == "__main__":
    AD = AutomaticDifferentiation() # 3x^2 + 2x^4 + 5x + 5
    equation = "x^(y+z)"
    AD.parse(equation, {"x": VariableNode("x", 2), "y": VariableNode("y", 3),  "z": VariableNode("z", 3)})
    result = AD.diffWRT("x")
    print(result)