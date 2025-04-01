from Node import Node, ConstNode, VariableNode, AdditionNode, MultiplicationNode, ExponentNode
import re

from matplotlib import pyplot as plt
import networkx as nx

def getOperatorIndex(expression, operator):
    balance = 0
    splitIndex = -1
    for i in range(len(expression)):
        token = expression[i]
        if token == '(': balance += 1
        if token == ')': balance -= 1
        if balance == 0 and token == operator: return i
    return splitIndex

def splitExpression(expression, splitIndex):
    left = expression[:splitIndex]
    right = expression[splitIndex+1:]
    return left, right

def findMatchingParenthesis(tokens):
    balance = 0
    for i in range(len(tokens)):
        token = tokens[i]
        if token == '(':
            balance += 1
        elif token == ')':
            balance -= 1
            if balance == 0:
                return i
        if balance < 0:
            raise ValueError("Mismatched parentheses")
    raise ValueError("No matching closing parenthesis")

def parseLeafNode(expression, variables) -> Node:
    if not expression:
        raise ValueError("Empty expression in parseLeafNode")
    first_token = expression[0]
    if first_token == '(':
        endIndex = findMatchingParenthesis(expression)
        if endIndex != len(expression)-1:
            raise ValueError("Parentheses did not wrap around expression")
        subExpression = expression[1:endIndex]
        return parseAddition(subExpression, variables)
    elif first_token.isdigit(): return ConstNode(int(first_token))
    elif first_token.isalpha(): return variables[first_token]
    else:
        raise ValueError(f"Unexpected token: {first_token}")

def parseExponent(expression, variableValues):
    
    splitIndex = getOperatorIndex(expression, "^")
    if splitIndex == -1: return parseLeafNode(expression, variableValues)
    left, right = splitExpression(expression, splitIndex)
    
    currNode = ExponentNode()
    currNode.setLeftChildToBe(parseLeafNode(left, variableValues))
    currNode.setRightChildToBe(parseExponent(right, variableValues))
    return currNode

def parseMultiplication(expression, variableValues):

    splitIndex = getOperatorIndex(expression, "*")
    if splitIndex == -1: return parseExponent(expression, variableValues)
    left, right = splitExpression(expression, splitIndex)
    
    currNode = MultiplicationNode()
    currNode.setLeftChildToBe(parseExponent(left, variableValues))
    currNode.setRightChildToBe(parseMultiplication(right, variableValues))
    return currNode

def parseAddition(expression, variableValues):

    splitIndex = getOperatorIndex(expression, "+")
    if splitIndex == -1: return parseMultiplication(expression, variableValues)
    left, right = splitExpression(expression, splitIndex)
    
    currNode = AdditionNode()
    currNode.setLeftChildToBe(parseMultiplication(left, variableValues))
    currNode.setRightChildToBe(parseAddition(right, variableValues))
    return currNode

class ExpressionTree:
    def __init__(self):
        self.root = None

    def build(self, expression, variableValues):
        token = re.findall(r'\d+|[a-zA-Z]+|[+*^()]', expression)
        self.root = parseAddition(token, variableValues)
        return self.root

if __name__ == "__main__":
    ET = ExpressionTree()

    xNode = VariableNode("x", 10)
    yNode = VariableNode("y", 10)
    zNode = VariableNode("z", 10)

    variableValues = {
        "x": xNode,
        "y": yNode,
        "z": zNode
    }
    node = ET.build("9+5*x*y+5*x^2*y^4+7*z^9+8*x*y*z", variableValues)
    print(node.evaluate())
    node.feedBackwardWith(1)
    print(variableValues["x"].sum)