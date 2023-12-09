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
    

def useCaseView(request, id):
    """

    """
    # return a nested dictionary, which contains the hierarchical data
    topicForSelectedUseCase = Topic.objects.filter(useCase__id=id)
    
    dictOfElements = {}
    rootElements = topicForSelectedUseCase.filter(parent=None)
    topicsWithoutRootElements = topicForSelectedUseCase.exclude(parent=None)
    listOfTrees = []
    for element in rootElements:
        nodeRootElement = Node(element)
        currentTree = Tree(nodeRootElement)
        # print(currentTree.root.topic.text)
        listOfTrees.append(currentTree)
        childsOfCurrentElement = topicsWithoutRootElements.filter(parent=element)
        topicsWithoutRootElements = topicsWithoutRootElements.exclude(parent=element)
        for childElement in childsOfCurrentElement:
            childNode = Node(childElement)
            nodeRootElement.addNeighbour(childNode)

    
    
    return render(
        request, 
        "criteriaCatalog/criteriaCatalogDetails.html", 
        {
            "useCase": UseCase.objects.filter(id = id)[0],
            "trees": listOfTrees,
        }
    )