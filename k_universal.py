import functools
import itertools

import networkx as nx
import matplotlib.pyplot as plt

def createGraph(k):    
    adjList = list()
    mapToBinary = dict()
    G = nx.DiGraph()
    _maxlen = k
    for j in range(0,2**(k-1)):
        adjList.append(list())
    for i in range(0,2**k):
        res = bin(i)
        if (len(res) - 2<_maxlen):
            res = '0b'+ functools.reduce(lambda a,b:a+"0",range(_maxlen - (len(res)-2) ),"")+res[2:]
                
        v1 = res[2:-1]; v2 = res[3:]
        mapToBinary[int(v1,2)] = v1;mapToBinary[int(v2,2)] = v2
        G.add_edge(v1,v2,edge_value = res[2:])
        adjList[int(v1,2)].append(int(v2,2))
        
    return (adjList,G,mapToBinary)

def drawGraph(G):
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels = True)
    edge_labels = dict([((u,v,), d['edge_value']) for u, v, d in G.edges(data = True)])
    nx.draw_networkx_edge_labels(G, pos, edge_labels = edge_labels, label_pos = 0.3, font_size = 11) #prints weight on all the edges
    return pos

def DFS(adjList,current_node,visited,postOrderMap,currentCount):
    visited[current_node] = 1
    postCount = currentCount
    for i in range(0,len(adjList[current_node])):
        if(visited[adjList[current_node][i]] == 0 and current_node != adjList[current_node][i]):
            postCount = DFS(adjList,adjList[current_node][i],visited,postOrderMap,postCount+1)
    postOrderMap[postCount + 1] = current_node    
    return postCount + 1

def sccDFS(adjList,current_node,component,currentComponent):
    internalVisited = [False] * len(adjList)
    
    #dfs implemented through loop
    dfsStack = [];
    dfsStack.append(current_node)    
    currentSearchNode = None
    while(len(dfsStack)>0):
        currentSearchNode = dfsStack.pop()
        internalVisited[currentSearchNode] = True
        component[currentSearchNode] = currentComponent
        for i in range(0,len(adjList[currentSearchNode])):
            if(component[adjList[currentSearchNode][i]] == None and (not internalVisited[adjList[currentSearchNode][i]])):
                dfsStack.append(currentSearchNode)
                dfsStack.append(adjList[currentSearchNode][i])
                break    

            
def SCC(adjList):
    nodes = len(adjList)
    g_reverse = list()
    currentComponent = 0
    currentCount = 0
    visited = [0] * nodes
    postOrderMap = {}
    for i in range(0,nodes):
        g_reverse.append(list())
    for i in range(0,nodes):
        for k in adjList[i]:
            g_reverse[k].append(i)

    #keep running dfs and on reaching a non expanisve node run sccDFS
    currentNode = None
    while(not all(visited)):        
        for j in (0,len(visited)):
            if(visited[j]==0):
                currentNode = j; break                
        currentCount = DFS(g_reverse,currentNode,visited,postOrderMap,currentCount) + 1
            
    return postOrderMap

def verifyEulerian(adjList):
    n = len(adjList)
    incount = [0] * n
    outcount = [0] * n

    for i in range(0,n):
        outcount[i] += len(adjList[i])
        for j in range(0,len(adjList[i])):
            incount[adjList[i][j]]+=1

    for i in range(0,n):
        if incount[i] != outcount[i]:
            return False

    return True
                
def performMerge(newCycle,oldCycle):
    if(oldCycle == None):
        return newCycle
    else:
        temp = []
        _oldPos = 0; _newPos = 0;
        while(oldCycle[_oldPos] != newCycle[_newPos]):
            temp.append(oldCycle[_oldPos])
            _oldPos += 1
        while(_newPos<len(newCycle)):
            temp.append(newCycle[_newPos])
            _newPos += 1
        _oldPos += 1
        while(_oldPos<len(oldCycle)):
            temp.append(oldCycle[_oldPos])
            _oldPos += 1
        return temp
            
        
def dfsCycle(adjMat,pos,visit,edgesTouched,start_pos,visitedOnce):
    visit.append(pos)
    visitedOnce[pos] = True
    edgesUsed = 0
    for i in range(0,len(adjMat)):        
        if(adjMat[pos][i] == 1):            
            adjMat[pos][i] = 0    
            if(i == start_pos):
                visit.append(start_pos)
                return edgesTouched+1
                #cycle found
            edgesUsed = dfsCycle(adjMat,i,visit,edgesTouched+1,start_pos,visitedOnce)
            break
    return edgesUsed  

def createCompleteEulerianCycle(adjList,k,start_pos,mapToBinary):
    n = len(adjList)
    adjMat = list()
    totalEdges = 0
    for i in range(n):
        l1 = [0] * n
        adjMat.append(l1)
    for i in range(n):
        for j in adjList[i]:
            adjMat[i][j] = 1
            totalEdges += 1

    
    cyclePossible = True
    visitedOnce = [False] * n
    visitedOnce[start_pos] = True
    current_all_cycle = None
    while(cyclePossible):
        randomCycle = list()
        start_pos = None
        
        for i in range(0,n):
            for j in adjList[i]:
                if(adjMat[i][j] and visitedOnce[i]):
                    start_pos = i
                    break
        if(start_pos == None):
            break
        edgesUsed = dfsCycle(adjMat,start_pos,randomCycle,0,start_pos,visitedOnce)
        totalEdges -= edgesUsed
        print("Bookkeeping purposes: {}".format(randomCycle))
        current_all_cycle = performMerge(randomCycle,current_all_cycle)
        cyclePossible = True if (totalEdges >0) else False

    
    isCircular = False
    
    if(current_all_cycle[0] == current_all_cycle[-1]):
        isCircular = True
        current_all_cycle.pop()
    
    print(current_all_cycle)
    
    finalString = mapToBinary[current_all_cycle[0]][:-1]    
    for i in current_all_cycle:
        finalString+= mapToBinary[i][-1]

    end = finalString[-(k-1):]
    beg = finalString[:k-1]
    while(end != beg and len(end)>0 and len(beg)>0):
        end = end[1:]
        beg = beg[:-1]
    if(len(beg)>0):
        finalString = finalString[len(beg) - 1:]
    if(isCircular):
        finalString+="c"
    return finalString
       
        
    '''
    1. perform random cycle
    2. store cycle traversed into list
    3. repeat on nodes that have unused edges
    4. perform merge on list
    5. check for first and last element match (for circularity)
    6. postprocess result 
    '''
    return True

if __name__=="__main__":    
    plt.plot()
    k = int(input("Enter the K-universal value"))
    plt.title('De-Bruijn graph for k = {}'.format(k))
    adjList,G,mapToBinary = createGraph(k)
    pos = drawGraph(G)
    plt.show()
    
    component = [None] * len(adjList)
    _componentNumber = 0
    postOrderMap = SCC(adjList)
    _postorder = list(postOrderMap.keys())
    _pos = len(_postorder) - 1
    while(len(list(filter(lambda x: x == None,component))) > 0):
        while(_pos >=0 and component[postOrderMap[_postorder[_pos]]] != None):
            _pos -= 1
        sccDFS(adjList,postOrderMap[_postorder[_pos]],component,_componentNumber)
        _componentNumber+=1
            
    if(_componentNumber==1 and verifyEulerian(adjList)):
        print("Graph has FSCC and passes Eulerian Verification")
        final_k_universal = createCompleteEulerianCycle(adjList,k,0,mapToBinary)
        print("Required value: {}".format(final_k_universal))
    else:
        print("Graph doesn't have FSCC or Cannot perform Eulerian Cycle")
        exit(0)
        
    #createEulerianCycle(res,k)  #instead of a hamiltonian path, we utilize 
    # !!we know that for our k-universal value Fully-SCC in directed graphs exists. however for other graphs first we need to run FSCC

