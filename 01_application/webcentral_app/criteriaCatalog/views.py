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

            else:
                flattendTreeList.append({"content": self.dictOfTree[key]})
                flattendTreeList.append({"outdent": True})
                outdentCount -= 1
        for outdent in range(outdentCount):
            flattendTreeList.append({"outdent": True})
        flattendTreeList.append({"outdent": True})
        return flattendTreeList


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
                queueBreathFirstSearch.append(childNode)
            currentTree.dictOfTree
            currentTree.addToDict(currentNode, list(childsOfCurrentElement))
        listOfFlattenedTrees.append(currentTree.flattenDictTreeToList())
    # hi = listOfTrees[0].flattenDictTreeToList()
    
    return render(
        request, 
        "criteriaCatalog/criteriaCatalogDetails.html", 
        {
            "criteriaCatalog": CriteriaCatalog.objects.filter(id = id)[0],
            "trees": listOfFlattenedTrees,
        }
    )