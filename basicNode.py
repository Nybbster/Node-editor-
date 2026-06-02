import sys

class Graph:

    
    def __init__(self, weights=None, labels=None):
        self.weights = weights or []
        self.labels = labels or []
        self.vertices = []
        self.nodes = []
        

    def addNode(self, node):
        self.nodes.append(node)
        self.labels.append(node.label)
    
    def connectNode(self, node1,node2,label ="",weight = 1):
        self.vertices.append(Vertex(node1,node2,weight,label))

    def deleteNode(self, node):
        self.labels.remove(node)
        self.nodes.remove(node)
    def deleteIndex(self,index):
        self.labels.pop(index)
        self.nodes.pop(index)
    
    def distance(self, soruce,target)->int:
        dist =({})
        prev =({})
        Exesting =[]
        if soruce not in self.nodes or target not in self.nodes:
            return -1
        if soruce == target:
            return 0 
        for node in self.nodes:
            dist[node] = sys.maxsize
            prev[node] = None
            Exesting.append(node)

        dist[soruce] = 0

        while len(Exesting) > 0:
            current = None
            min = sys.maxsize

            for node in Exesting:
                if dist[node] < min:
                    min = dist[node]
                    current = node
            
            if current == None: break

            Exesting.remove(current)

            if current == target:
                return dist[current]
            
            for vertex in self.vertices:
                if current in vertex:
                    edge = None
                    if vertex.GetNode1() == current:
                        edge = vertex.GetNode2()
                    elif vertex.GetNode2() == current:
                        edge = vertex.GetNode1()

                    if edge == None:continue
                
                    if edge not in Exesting: continue

                    alt = dist[current] + vertex.GetWeight()

                    if alt < dist[edge]:
                        dist[edge] = alt
                        prev[edge] = current

        return dist[target]
class Node: 
    def __init__(self,label):
        self.label = label

    def compareTo(self, other):
        return self.label == other.label
    def __hash__(self):
        return hash(self.label)

class Vertex:
    
    def __init__(self, node1, node2,weight =1,label=""):
        self.node1 = node1
        self.node2 = node2
        self.weight = weight
        self.label = label

    def contains(self,node):
        return self.node1 == node or self.node2 == node
    def __contains__(self, node):
        return self.contains(node)
    
    def GetNode1(self): return self.node1
    def GetNode2(self): return self.node2
    def GetWeight(self): return self.weight



# addlist = [1,2,3,4]
# addlistlabel = ["A","B","C","D"]
# g = Graph(addlist,addlistlabel)

# node1 = Node("A")
# g.addNode(node1)
# node2 = Node("B")
# g.addNode(node2)
# node3 = Node("C")
# g.addNode(node3)
# node4 = Node("D")
# g.addNode(node4)


# g.connectNode(node1,node2)
# g.connectNode(node2,node3)
# g.connectNode(node3,node4)

# distance = g.distance(node1,node4)
# print(distance)


