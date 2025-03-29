from Node import Node

class ExpressionTree:
    def __init__(self):
        self.root = None

    def addLeftChild(self, parentNode: "Node", childNode: "Node"): # connect childNode to the parentNode as a left child
        parentNode.setLeftChild(childNode)
        childNode.setParent(parentNode)

    def addRightChild(self, parentNode: "Node", childNode: "Node"): # connect childNode to the parentNode as a right child
        parentNode.setRightChild(childNode)
        childNode.setParent(parentNode)

    def addChildren(self, parentNode: "Node", leftChild: "Node", rightChild: "Node"): # connect children to parentNode as a left child and right child.
        self.addLeftChild(parentNode, leftChild)
        self.addRightChild(parentNode, rightChild)

    def parse(Expression):
        pass


if __name__ == "__main__":
    # 3 + (7 * 5)
    tree = ExpressionTree()
    root = Node("+")
    tree.root = root
    firstLeftChild = Node(3.0)
    firstRightChild = Node("*")
    secondLeftChild = Node(5.0)
    secondRightChild = Node(7.0)

    tree.addChildren(root, firstLeftChild, firstRightChild)
    tree.addChildren(firstRightChild, secondLeftChild, secondRightChild)

    print(root.evaluate())