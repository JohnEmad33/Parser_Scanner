from graphviz import Graph
shape = {'expression' : 'oval', 'statement' : 'rectangle'}
class TreeNode:
    count = 1;
    def __init__(self, type, stringValue):
        self.children = []                                              # Contains children nodes connected directly to self node
        self.rightSibling = None                                        # Contains the direct right Sibling of self node in the tree diagram
        self.type = type                                                # Exp or Statement
        self.stringValue = stringValue                                  # Text to be written in the tree
        self.parent = None
        self.name = TreeNode.count
        TreeNode.count = TreeNode.count + 1

    def addChild(self, child):
        self.children.append(child)

    def getChildren(self):
        return self.children

    def getChild(self, index):
        if index < len(self.children):
            return self.children[index]

    def getChildrenNumber(self):
        return len(self.children)

    def setRightSibling(self, sibling):
        self.rightSibling = sibling

    def getRightSibling(self):
        return self.rightSibling

    def setType(self, type):
        self.type = type

    def getType(self):
        return self.type

    def setStringValue(self, value):
        self.stringValue = value

    def getStringValue(self):
        return self.stringValue

    def setParent(self, parent):
        self.parent = parent

    def getParent(self):
        return self.parent
    def getName(self):
        return self.name

class Tree:
    def __init__(self, root):
        self.root = root
    def getRoot(self):
        return self.root
    def setRoot(self, root):
        self.root = root

    ### function for traversing the tree
    def draw(self, node, graph, subgraph, rootFlag):
        if node == None:
            return
        if(rootFlag):
            if node.getRightSibling() != None:
                n = node
                subgraph = Graph()
                subgraph.attr(rank='same')
                subgraph.node(str(node.getName()), node.getStringValue(), shape=shape[node.getType()], ordering="out")
                while n.getRightSibling() != None:
                    subgraph.node(str(n.getRightSibling().getName()), n.getRightSibling().getStringValue(), shape=shape[n.getRightSibling().getType()] ,ordering = "in")
                    subgraph.edge(str(n.getName()), str(n.getRightSibling().getName()))
                    n = n.getRightSibling()

                graph.subgraph(subgraph)

        if node.getRightSibling() != None:
            self.draw(node.getRightSibling(), graph, subgraph, False)

        child = node.getChildren()
        #To handle the children order
        for i in range(node.getChildrenNumber()):
            if(i == 0):
                subgraph2 = Graph()
                subgraph2.attr(rank='same', remincross="true")
                subgraph2.node(str(child[i].getName()), child[i].getStringValue(), shape=shape[child[i].getType()],ordering = "out",weight='3')
            n = child[i]
            while n.getRightSibling() != None:
                subgraph2.node(str(n.getRightSibling().getName()), n.getRightSibling().getStringValue(),
                               shape=shape[n.getRightSibling().getType()], ordering="out")
                subgraph2.edge(str(n.getName()), str(n.getRightSibling().getName()))
                n = n.getRightSibling()
            if(i < node.getChildrenNumber() - 1):
                subgraph2.node(str(child[i+1].getName()), child[i+1].getStringValue(), shape=shape[child[i+1].getType()],
                               ordering="out")
                subgraph2.edge(str(n.getName()), str(child[i+1].getName()), style = "invis")

        if(node.getChildrenNumber() > 0):
            graph.subgraph(subgraph2)

        for i in range(node.getChildrenNumber()):
            graph.edge(str(node.getName()), str(child[i].getName()))
            self.draw(child[i], graph, subgraph, False)



    #draw the node
    def DrawTree(self):
        graph = Graph(format='png')
        graph.attr()
        rootFlag = True
        subgraph = Graph()
        self.draw(self.root, graph, subgraph,rootFlag)
        graph.render(filename="test4", view=0, cleanup=1)
