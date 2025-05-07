from Node import Node, ConstNode, VariableNode, AdditionNode, SubtractionNode, MultiplicationNode, DivisionNode, ExponentNode, SinNode, CosNode, LogNode
import re
import math

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

    if first_token == 'sin' or first_token == 'cos':
        if len(expression) < 2 or expression[1] != '(':
            raise ValueError(f"Expected '(' after {first_token}")
        endIndex = findMatchingParenthesis(expression[1:])
        subExpression = expression[2:endIndex+1]
        childNode = parseAdditionSubtraction(subExpression, variables)
        currNode = SinNode() if first_token == "sin" else CosNode()
        currNode.setChildToBe(childNode)
        return currNode

    # Deal with log(base)(argument)
    if first_token == 'log':
        if len(expression) < 2 or expression[1] != '(':
            raise ValueError("Expected '(' after 'log'")
        
        # Parse the base
        endBaseParentheses = findMatchingParenthesis(expression[1:])
        logBaseSubExpression = expression[2:endBaseParentheses + 1]
        logBaseNode = parseAdditionSubtraction(logBaseSubExpression, variables)
        
        # Parse the argument
        logArgumentExpression = expression[endBaseParentheses + 2:]
        if len(logArgumentExpression) == 0 or logArgumentExpression[0] != '(':
            raise ValueError("Expected '(' for log argument")
        
        endArgumentParentheses = findMatchingParenthesis(logArgumentExpression)
        logArgumentSubExpression = logArgumentExpression[1:endArgumentParentheses]
        logArgumentNode = parseAdditionSubtraction(logArgumentSubExpression, variables)

        # Create the LogNode
        currNode = LogNode()
        currNode.setLeftChildToBe(logBaseNode)
        currNode.setRightChildToBe(logArgumentNode)

        return currNode

    # Deal with ln()
    if first_token == 'ln':
        if len(expression) < 2 or expression[1] != '(':
            raise ValueError(f"Expected '(' after {first_token}")
        endIndex = findMatchingParenthesis(expression[1:])
        subExpression = expression[2:endIndex+1]
        childNode = parseAdditionSubtraction(subExpression, variables)
        currNode = LogNode()
        currNode.setLeftChildToBe(VariableNode("e", math.e))
        currNode.setRightChildToBe(childNode)
        return currNode

    # Deal with Parentheses
    if first_token == '(':
        endIndex = findMatchingParenthesis(expression)
        if endIndex != len(expression)-1:
            raise ValueError("Parentheses did not wrap around expression")
        subExpression = expression[1:endIndex]
        return parseAdditionSubtraction(subExpression, variables)
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

def parseMultiplicationDivision(expression, variableValues):

    splitIndexMultiplication = getOperatorIndex(expression, "*")
    splitIndexDivision = getOperatorIndex(expression, "/")

    if splitIndexMultiplication == -1 or (splitIndexDivision != -1 and splitIndexDivision < splitIndexMultiplication):
        splitIndex = splitIndexDivision
        currNode = DivisionNode()
    else:
        splitIndex = splitIndexMultiplication
        currNode = MultiplicationNode()

    if splitIndex == -1: return parseExponent(expression, variableValues)
    left, right = splitExpression(expression, splitIndex)
    
    currNode.setLeftChildToBe(parseExponent(left, variableValues))
    currNode.setRightChildToBe(parseMultiplicationDivision(right, variableValues))
    return currNode

def parseAdditionSubtraction(expression, variableValues):

    splitIndexAddition = getOperatorIndex(expression, "+")
    splitIndexSubtraction = getOperatorIndex(expression, "-")

    if splitIndexAddition == -1 or (splitIndexSubtraction != -1 and splitIndexSubtraction < splitIndexAddition):
        splitIndex = splitIndexSubtraction
        currNode = SubtractionNode()
    else:
        splitIndex = splitIndexAddition
        currNode = AdditionNode()

    if splitIndex == -1: return parseMultiplicationDivision(expression, variableValues)
    left, right = splitExpression(expression, splitIndex)
    
    currNode.setLeftChildToBe(parseMultiplicationDivision(left, variableValues))
    currNode.setRightChildToBe(parseAdditionSubtraction(right, variableValues))
    return currNode

class ExpressionTree:
    def __init__(self):
        self.root = None
        self.variables = {
            "e": math.e,
            "pi": math.pi
        }

    def build(self, expression, variableValues):

        # TODO automatically generate variableValue dict
        for variableName, value in variableValues.items():
            newVarNode = VariableNode(variableName, value)
            self.variables[variableName] = newVarNode
        
        # Enclose every negative sign in parentheses. For example, -(x+y) should be (-(x+y)) or -5*x + 3 should be (-5)*x + 3. x-y or 5-3 need not be inside parentheses. 
        # Multiplication must be explicit. For example, 12x should be written as 12*x.
        # sin and cos are in radian
        expression = expression.replace('(-', '(0-')
        token = re.findall(r'\d+|[a-zA-Z]+|[+*\/^()-]', expression)
        self.root = parseAdditionSubtraction(token, self.variables)
        return self.root, self.variables
    
    

if __name__ == "__main__":
    ET = ExpressionTree()

    variableValues = {}
    root, variables = ET.build("log(2)(8)", variableValues)  # Unpack the tuple
    print(root.evaluate())  # Call evaluate() on the root node