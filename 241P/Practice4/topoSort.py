import collections
def topoSort(graph):

    indegree = collections.Counter()
    for node in graph:
        if node not in indegree:
            indegree[node] = 0
        for nxt in graph[node]:
            indegree[nxt] += 1
    
    print(indegree)
    queue = collections.deque()

    for node in indegree:
        if indegree[node] == 0:
            queue.append(node)
    ans = []
    while queue:
        node = queue.popleft()
        ans.append(node)
        if node in graph:
            for nxt in graph[node]:
                indegree[nxt] -= 1
                if indegree[nxt] == 0:
                    queue.append(nxt)
    print(indegree)

    print(ans)


graph = {'A':['B','D'],'B':['C','E','D'],'C':['F'],'D':['E','G'],'E':['C','G','F'],'F':['H'],'G':['F','I'],'H':['G','J'],'I':['J']}
topoSort(graph)