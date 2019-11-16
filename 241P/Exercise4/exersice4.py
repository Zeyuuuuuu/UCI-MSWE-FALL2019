import collections
class Solution:
    def __init__(self):
        self.res = []

    def dfs(self,graph,node):
        def rec(node):
            if node in self.res:
                return
            self.res.append(node)
            nxts = []
            for nei in graph[node]:
                if nei not in self.res:
                    nxts.append(nei)
            for nxt in sorted(nxts):
                rec(nxt)
        rec(node)
        return self.res

    def bfs(self,graph,node):
        self.res.append(node)
        queue = collections.deque([node])
        while queue:
            curr = queue.popleft()
            for nei in sorted(graph[curr]):
                if nei not in self.res:
                    self.res.append(nei)
                    queue.append(nei)
        return self.res
                                                                                                                                

graph =  {'A':['D','B','I'],'B':['A','C','D','E'],'C':['B','E','F'],'D':['A','B','E','G'],'E':['B','C','D','F','G','H'],'F':['C','E','H'],'G':['D','E','H','I','J'],'H':['E','F','G','J'],'I':['A','G','J'],'J':['I','G','H']}
graph1 = {'A':['B','E'],'B':['A','F','C'],'C':['B','G','D'],'D':['C','H'],'E':['A','F','I'],'F':['B','E','J','G'],'G':['C','F','K','H'],'H':['D','G','L'],'I':['E','J','M'],'J':['I','F','K','M'],'K':['G','J','L','O'],'L':['H','K','P'],'M':['I','N'],'N':['J','M','O'],'O':['N','K','P'],'P':['O','L']}


s = Solution()
print(s.dfs(graph1,'A'))
s1 = Solution()
print(s1.bfs(graph1,'A'))