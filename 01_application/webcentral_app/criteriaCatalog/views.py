from django.shortcuts import render

from .models import (
    Topic,
    UseCase,
)

def index(request):
    """Return the criteriaCatalog-Page
    
    """
    allUseCases = UseCase.objects.all()
    return render(
        request, 
        'criteriaCatalog/criteriaCatalog.html', 
        {
            "useCases": allUseCases,
        }
    )

class Node:
    def __init__(self, topic):
        self.topic = topic
        self.neighbours = []
    def addNeighbour(self, neighbourTopic):
        self.neighbours.append(neighbourTopic)

class Tree:
    def __init__(self, rootNode):
        self.root = rootNode
        self.level = []
        self.dictOfTree = {}
    def addToDict(self, node, listOfNodesForLayer):
        self.dictOfTree[node.topic] = listOfNodesForLayer
    def flattenDictTreeToList(self):
        """
        """
        flattendTreeList = []
        depthFirstSearchList = []
        listOfDictKeys = []
        listOfDictKeys.append(list(self.dictOfTree.keys())[0])
        outdentCount = 0
        while len(listOfDictKeys) > 0:
            key = listOfDictKeys.pop(0)
            flattendTreeList.append({"indent": True})
            flattendTreeList.append({"content": key})
            # breakpoint()
            if len(self.dictOfTree[key]) > 0:
                for nodeValue in self.dictOfTree[key]:
                    if len(self.dictOfTree[nodeValue]) == 0:
                        flattendTreeList.append({"indent": True})
                        flattendTreeList.append({"content": nodeValue})
                        flattendTreeList.append({"outdent": True})
                    else:
                        listOfDictKeys.append(nodeValue)
                        outdentCount += 1

            else:
                flattendTreeList.append({"content": self.dictOfTree[key]})
                flattendTreeList.append({"outdent": True})
                outdentCount -= 1
        for outdent in range(outdentCount):
            flattendTreeList.append({"outdent": True})
        return flattendTreeList

    

def useCaseView(request, id):
    """

    """
    # return a nested dictionary, which contains the hierarchical data
    topicForSelectedUseCase = Topic.objects.filter(useCase__id=id)
    
    dictOfElements = {}
    rootElements = topicForSelectedUseCase.filter(parent=None)
    topicsWithoutRootElements = topicForSelectedUseCase.exclude(parent=None)
    listOfTrees = []
    listOfFlattenedTrees = []
    for element in rootElements:
        nodeRootElement = Node(element)
        currentTree = Tree(nodeRootElement)
        # print(currentTree.root.topic.text)
        listOfTrees.append(currentTree)

        # implementation of a breath-first-search:
        queueBreathFirstSearch = []
        queueBreathFirstSearch.append(nodeRootElement)
        topicsWithoutChilds = topicsWithoutRootElements
        
        while len(queueBreathFirstSearch) > 0:
            currentNode = queueBreathFirstSearch.pop()
            childsOfCurrentElement = topicsWithoutChilds.filter(parent=currentNode.topic)
            topicsWithoutChilds = topicsWithoutChilds.exclude(parent=currentNode.topic)
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
            "useCase": UseCase.objects.filter(id = id)[0],
            "trees": listOfFlattenedTrees,
        }
    )