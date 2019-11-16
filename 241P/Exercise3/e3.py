import collections
class Solution:
    # On2
    def __init__(self):
        self.numOfEdges = 0
        self.numOfNodes = 0
        self.indexOfNodes = 0
        self.edges = []
    def adjacencyMatrixToAdjacencyLists(self,adM):
        adList = collections.defaultdict(list)
        n = len(adM)
        for i in range(n):
            for j in range(i+1,n):
                if (adM[i][j]):
                    adList[i].append(j)
                    adList[j].append(i)
        return adList

    # On2
    def adjacencyListToIncidenceMatrix(self,adList):
        self.numOfEdges = sum(len(adj) for adj in adList.values())
        self.numOfNodes = len(adList)
        self.indexOfNodes = collections.defaultdict()
        for i,node in enumerate(adList):
            self.indexOfNodes[node] = i
        
        self.edges = []
        inM = [[0] * self.numOfEdges for _ in range(self.numOfNodes)]
        for node in adList:
            for nei in adList[node]:
                if {node, nei} not in self.edges:
                    inM[self.indexOfNodes[node]][len(self.edges)] = 1
                    inM[self.indexOfNodes[nei]][len(self.edges)] = 1
                    self.edges.append({node,nei})
        return inM

    # On2
    def incidenceMatrixToAdjacencyLists(self,inM):
        adList = collections.defaultdict(list)
        n = len(inM)
        for j in range(n):
            a = b = -1
            for i in range(n):
                if (inM[i][j]):
                    if a == -1:
                        a = i
                    else:
                        b = i
            if b != -1:
                adList[a].append(b)
                adList[b].append(a)
        return adList

graph =  {'A':['D','B','I'],'B':['A','C','D','E'],'C':['B','E','F'],'D':['A','B','E','G'],'E':['B','C','D','F','G','H'],'F':['C','E','H'],'G':['D','E','H','I','J'],'H':['E','F','G','J'],'I':['A','G','J'],'J':['I','G','H']}
graph1 = {'A':['B','E'],'B':['A','F','C'],'C':['B','G','D'],'D':['C','H'],'E':['A','F','I'],'F':['B','E','J','G'],'G':['C','F','K','H'],'H':['D','G','L'],'I':['E','J','M'],'J':['I','F','K','M'],'K':['G','J','L','O'],'L':['H','K','P'],'M':['I','N'],'N':['J','M','O'],'O':['N','K','P'],'P':['O','L']}

s = Solution()
inM = s.adjacencyListToIncidenceMatrix(graph)
for row in inM:
    print(row)
adList = s.incidenceMatrixToAdjacencyLists(inM)
print(adList)
print(s.edges)
print(s.indexOfNodes)
