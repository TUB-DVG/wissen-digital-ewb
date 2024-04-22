from django.shortcuts import render

from .models import (
    CriteriaCatalog,
    Topic,
)

def index(request):
    """Return the criteriaCatalog-Page
    
    """
    allCatalogs = CriteriaCatalog.objects.all()
    # breakpoint()
    return render(
        request, 
        'criteriaCatalog/criteriaCatalog.html', 
        {
            "useCases": allCatalogs,
        }
    )

class Node:
    def __init__(self, topic: Topic):
        self.topic = topic
        self.neighbours = []
        self.depth = None
    def addNeighbour(self, neighbourTopic):
        self.neighbours.append(neighbourTopic)
    
    def addDepth(self, depth: int):
        """adds the depth of the element in the tree

        """
        self.depth = depth
    def __str__(self):
        return str(self.topic)

class Tree:
    def __init__(self, rootNode):
        self.root = rootNode
        self.level = []
        self.dictOfTree = {}
    def addToDict(self, node, listOfNodesForLayer):
        self.dictOfTree[node] = listOfNodesForLayer

def tree_to_html(tree, root):
    html = []
    html.append({"indent": True})
    html.append({"content": root})
    for child in tree.get(root, []):
        html += tree_to_html(tree, child)
    html.append({"outdent": True})
    # breakpoint()
    return html


def buildCrtieriaCatalog(request, criteriaCatalogIdentifer):
    """

    """

    id = CriteriaCatalog.objects.filter(name__icontains=criteriaCatalogIdentifer)[0].id


    # return a nested dictionary, which contains the hierarchical data
    topicForSelectedUseCase = Topic.objects.filter(criteriaCatalog__id=id)
    
    dictOfElements = {}
    rootElements = topicForSelectedUseCase.filter(parent=None)
    topicsWithoutRootElements = topicForSelectedUseCase.exclude(parent=None)
    listOfTrees = []
    listOfFlattenedTrees = []
    nodeRootElements = []
    for index, element in enumerate(rootElements):
        nodeRootElement = Node(element)
        nodeRootElements.append(nodeRootElement)
        nodeRootElement.addDepth(0)
        currentTree = Tree(nodeRootElement)
        listOfTrees.append(currentTree)

        # implementation of a breath-first-search:
        queueBreathFirstSearch = []
        queueBreathFirstSearch.append(nodeRootElement)
        topicsWithoutChilds = topicsWithoutRootElements
        
        while len(queueBreathFirstSearch) > 0:
            currentNode = queueBreathFirstSearch.pop()
            childsOfCurrentElement = topicsWithoutChilds.filter(parent=currentNode.topic)
            topicsWithoutChilds = topicsWithoutChilds.exclude(parent=currentNode.topic)
            childNodes = []
            for childElement in childsOfCurrentElement:
                childNode = Node(childElement)
                currentNode.addNeighbour(childNode)
                childNode.addDepth(currentNode.depth+1)
                childNodes.append(childNode)
                queueBreathFirstSearch.append(childNode) 
            currentTree.addToDict(currentNode, childNodes)
        listOfFlattenedTrees.append(tree_to_html(listOfTrees[index].dictOfTree, nodeRootElements[index]))
    return render(
        request, 
        "criteriaCatalog/criteriaCatalogDetails.html", 
        {
            "criteriaCatalog": CriteriaCatalog.objects.get(id = id),
            "trees": listOfFlattenedTrees,
        }
    )