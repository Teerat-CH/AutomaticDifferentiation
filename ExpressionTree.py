from Node import Node, ConstNode, VariableNode, AdditionNode, MultiplicationNode, ExponentNode
import re

import networkx as nx
from matplotlib import pyplot as plt

def parseLeafNode(expression, variables) -> Node:
    expression = expression[0]
    if expression.isdigit():
        return ConstNode(int(expression))
    elif expression.isalpha():
        return variables[expression]

def parseExponent(expression, variableValues):
    if "^" not in expression:
        return parseLeafNode(expression, variableValues)
    
    splitIndex = expression.index("^")
    left = expression[:splitIndex]
    right = expression[splitIndex+1:]

    currNode = ExponentNode()
    currNode.setLeftChildToBe(parseLeafNode(left, variableValues))
    currNode.setRightChildToBe(parseExponent(right, variableValues))

    return currNode

def parseMultiplication(expression, variableValues):
    if "*" not in expression:
        return parseExponent(expression, variableValues)
    
    splitIndex = expression.index("*")
    left = expression[:splitIndex]
    right = expression[splitIndex+1:]

    currNode = MultiplicationNode()
    currNode.setLeftChildToBe(parseExponent(left, variableValues))
    currNode.setRightChildToBe(parseMultiplication(right, variableValues))

    return currNode

def parseAddition(expression, variableValues):
    if "+" not in expression:
        return parseMultiplication(expression, variableValues)
    
    splitIndex = expression.index("+")
    left = expression[:splitIndex]
    right = expression[splitIndex+1:]

    currNode = AdditionNode()
    currNode.setLeftChildToBe(parseMultiplication(left, variableValues))
    currNode.setRightChildToBe(parseAddition(right, variableValues))

    return currNode
    
def parse(expression, variableValues):
    return parseAddition(expression, variableValues)

class ExpressionTree:
    def __init__(self):
        self.root = None

    def build(self, expression, variableValues):
        token = re.findall(r'\d+|[a-zA-Z]+|[+*^()]', expression)
        self.root = parse(token, variableValues)
        return self.root

if __name__ == "__main__":
    ET = ExpressionTree()

    xNode = VariableNode("x", 10)

    variableValues = {
        "x": xNode
    }
    node = ET.build("3*x^2+2*x^4+5*x+5", variableValues)
    print(node.evaluate())
    node.feedBackwardWith(1)
    print(variableValues["x"].sum)