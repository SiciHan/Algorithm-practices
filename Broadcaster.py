
import json
import heapq
class Node(object):
    def __init__(self,nodeName):
        self.name=nodeName
        self.directTo=list()
        self.isFrom=list()
        self.isExplored=False
        self.groupLeader=None

class NodeWeighted(object):
    def __init__(self,nodeName):
        self.name=nodeName
        self.directTo=list()
        self.isFrom=list()
        self.isExplored=False
        self.groupLeader=None
        self.outEdge=list()

class Edge(object):
    def __init__(self,edgeString,dictOfNode):
        index=edgeString.find('->')
        nodename1=edgeString[0:index]
        nodename2=edgeString[index+2:]
        if nodename1 in dictOfNode.keys():
            Node1=dictOfNode[nodename1]
        else:
            dictOfNode.update({nodename1:Node(nodename1)})
            Node1=dictOfNode[nodename1]

        if nodename2 in dictOfNode.keys():
            Node2=dictOfNode[nodename2]
        else:
            dictOfNode.update({nodename2:Node(nodename2)})
            Node2=dictOfNode[nodename2]

        Node1.directTo.append(Node2)
        Node2.isFrom.append(Node1)

class Graph(object):
    def __init__(self,data):
        #assume no duplicated edges in the data
        self.listOfEdges=list()
        self.dictOfNode=dict()
        self.groupleaders=list()
        self.groupleadersCount=list()
        
        for edgeString in data:
            self.listOfEdges.append(Edge(edgeString,self.dictOfNode))
        self.currentLabel=len(self.dictOfNode)
        self.listOfOrderedNodes=[None]*self.currentLabel

class GraphWeighted(object):
    def __init__(self,data):
        #assume no duplicated edges in the data
        self.listOfEdges=list()
        self.dictOfNode=dict()
        self.groupleaders=list()
        self.groupleadersCount=list()
        for edgeString in data:
            self.listOfEdges.append(EdgeWeighted(edgeString,self.dictOfNode))
        self.currentLabel=len(self.dictOfNode)
        self.listOfOrderedNodes=[None]*self.currentLabel

class EdgeWeighted(object):
    def __init__(self,edgeString,dictOfNode):
        index1=edgeString.find('->')
        index2=edgeString.find(',')
        nodename1=edgeString[0:index1]
        nodename2=edgeString[index1+2:index2]
        self.weight=int(edgeString[index2+1:])
        if nodename1 in dictOfNode.keys():
            Node1=dictOfNode[nodename1]
        else:
            dictOfNode.update({nodename1:NodeWeighted(nodename1)})
            Node1=dictOfNode[nodename1]

        if nodename2 in dictOfNode.keys():
            Node2=dictOfNode[nodename2]
        else:
            dictOfNode.update({nodename2:NodeWeighted(nodename2)})
            Node2=dictOfNode[nodename2]

        Node1.directTo.append(Node2)
        Node2.isFrom.append(Node1)
        Node1.outEdge.append(self)
        self.FromVertex=Node1
        self.ToVertex=Node2

    def __cmp__(self, other):
        return cmp(self.weight, other.weight)

def DepthFirstSearchLoop(graph):
    #mark all nodes unexplored
    for nodename,node in graph.dictOfNode.items():
        node.isExplored=False
    # current label =n
    currentLabel=graph.currentLabel
    # for each vertex
    for nodename,node in graph.dictOfNode.items():
        if node.isExplored==False:
            DepthFirstSearch(graph,node)

def DepthFirstSearch(graph,startVertex):
    #if the point is the end point, set the ordering to the current label and decrement
    if startVertex.directTo==list():
        pass
    else:
        # for every edge (s,v)
        for v in startVertex.directTo:
            #if v not yet explored, mark it explored, and DFS(G,V)
            if v.isExplored==False:
                v.isExplored=True
                DepthFirstSearch(graph,v)
    orderofnode=graph.currentLabel
    # place the vertex into the nth position
    graph.listOfOrderedNodes[orderofnode-1]=startVertex
    graph.currentLabel-=1
def DepthFirstSearchLoopModified(graph):
    #mark all nodes unexplored
    for nodename,node in graph.dictOfNode.items():
        node.isExplored=False
    # for each vertex
    for node in graph.listOfOrderedNodes:
        # if it not explore, mark it as explored
        if node.isExplored==False:
            node.isExplored=True
            # if it is the root, assign the leader to itself
            if node.isFrom==list():
                node.groupLeader=node
                graph.groupleaders.append(node.name)
                graph.groupleadersCount.append(1)
                DepthFirstSearchModified(graph,node)

def DepthFirstSearchModified(graph,startVertex):
    #if the point is the end point, set the ordering to the current label and decrement
    if startVertex.directTo==list():
        pass
    else:
        # for every edge (s,v)
        for v in startVertex.directTo:
            #if v not yet explored, mark it explored, and DFS(G,V)
            if v.isExplored==False:
                v.isExplored=True
                v.groupLeader=startVertex.groupLeader
                index=graph.groupleaders.index(v.groupLeader.name)
                graph.groupleadersCount[index]+=1
                DepthFirstSearchModified(graph,v)

def DijkstraAlgorithm(graph,s,v):
    #initialize
    verticesProcessed=[s,] # a collection of vertices on the left collection
    shortestPathDistance=dict() # a record of optimized accumulated distance for all vertices in vertice:distance format like a score
    shortestPath=dict() # a record of optimized path from s to each vertex
    shortestPathDistance[s.name]=0 # make the score of s =0
    shortestPath[s.name]=list() # no path from s to s
    # my own initialization
    frontierEdges=s.outEdge[:]
   
    #main loop
    #while verticesProcessed is not the entire vertices
    while len(verticesProcessed)!=len(graph.dictOfNode):
        nextVertexToProcess=None
        minscore=100000000000
        #for all edges that v in verticesProcessed and w in notprocessed
        for e in frontierEdges:
            #print(e.FromVertex.name,e..name)
            # compute shortestPathDistance to v from s  +weight of the edge v,w
            score=shortestPathDistance[e.FromVertex.name]+e.weight
            if score<minscore:
                minscore=score
                previousVertex=e.FromVertex
                nextVertexToProcess=e.ToVertex
                edgeToBeAddedToPath=e
        # add w to processed
        verticesProcessed.append(nextVertexToProcess)
        #set shortest Path Distance to w from s= shortestPathDistance to v from s  +weight of the edge v,w
        shortestPathDistance[nextVertexToProcess.name]=minscore
        # add edge v,w to the path
        Bv=list(shortestPath[previousVertex.name]) # to copy the previous path
        Bv.append(edgeToBeAddedToPath)#add the edge to the previous path 
        shortestPath[nextVertexToProcess.name]=Bv #assigned the updated path
        #my own modification: update the frontier edge list
        frontierEdges.remove(edgeToBeAddedToPath)
        frontierEdges.extend(nextVertexToProcess.outEdge[:])
        if v in verticesProcessed:
            return shortestPath[v.name]

def main():
    #part1:
    #open json file
    with open("sampleBroadcaster1.json") as json_file:
        data=json.load(json_file)
        edges=data["data"]
    #create a graph
    graph1=Graph(edges)

    #Perform Depth-First Search to the Graph to assign group leaders
    #theoretically, shoudld do a two DFS: 
    #One for topological ordering to make sure the parent is always before child
    #the other one is to assign their groups.
    #first pass
    DepthFirstSearchLoop(graph1)
    #second pass
    DepthFirstSearchLoopModified(graph1)
    res1=graph1.groupleaders
    #part2:
    #similar to part one, just need to add a counter
    graph2=Graph(edges)
    #first pass
    DepthFirstSearchLoop(graph2)
    #second pass
    DepthFirstSearchLoopModified(graph2)
    max=-1
    maxindex=-1
    for i in range(len(graph2.groupleadersCount)):
        if graph2.groupleadersCount[i]>max:
            max=graph2.groupleadersCount[i]
            maxindex=i
            tempLeader=graph2.groupleaders[maxindex]
        elif graph2.groupleadersCount[i]==max:
            if graph2.groupleaders[i]>tempLeader:
                maxindex=i

    res2=graph2.groupleaders[maxindex]
    print(res2)
    #part 3
    #this question is to find the shortest path for a directed acyclic graph with positive weights
    # we can use Dijkstra's Algorithm to solve the problem
    with open("sampleBroadcaster3.json") as json_file:
        data=json.load(json_file)
        edges=data["data"]
        sender=data["sender"]
        recipient=data["recipient"]


    #create a graph
    graph3=GraphWeighted(edges)
    # create vertices
    s=graph3.dictOfNode[sender]
    v=graph3.dictOfNode[recipient]
    shortestpath=DijkstraAlgorithm(graph3,s,v)

    res=list() # to hold a list of letters
    # convert shortestPath to list of letters
    res.append(shortestpath[0].FromVertex.name)
    for e in shortestpath:
        res.append(e.ToVertex.name)
    print(res)

if __name__=="__main__":
    main()