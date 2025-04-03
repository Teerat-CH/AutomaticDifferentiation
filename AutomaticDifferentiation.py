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
        self.tree = None

    def parse(self, string, variableValues):
        self.expressionTree = ExpressionTree()
        self.variables = variableValues
        self.tree, self.variables = self.expressionTree.build(string, variableValues)
    
    def diffWRT(self, variableName):
        if not self.evaluated:
            self.expressionTree.root.evaluate()
            self.expressionTree.root.feedBackwardWith(1)
        if variableName in self.variables:
            return self.variables[variableName].sum
        return 0
    
if __name__ == "__main__":
    AD = AutomaticDifferentiation()
    equation = "(x^3/y^2)^4*(z/(y^2))"
    AD.parse(equation, {"x": 2, "y": 4,  "z": 3})
    result = AD.diffWRT("y")
    print(result)