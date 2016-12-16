
def findInitialKmer(kmerArray):
    for kmer in kmerArray:
        counter = 0
        k = len(kmerArray[0])
        for i in range(len(kmerArray)):
            if kmer[1:] == kmerArray[i][0:k - 2]:
                counter += 1
                break
    if counter == 0:
        return kmer


def ReconstructString(kmerArray):
    k = len(kmerArray[0])
    dna = findInitialKmer(kmerArray)
    kmerArray.remove(dna)
    #  while(len(kmerArray) > 1):
    length = len(kmerArray)
    while len(kmerArray) > 0 :
        for elem in range(len(kmerArray)):
            newKmer = kmerArray[elem]
            if kmerArray[elem][1:] == dna[0:k - 1]:
                dna = newKmer[0] + dna
                kmerArray.remove(kmerArray[elem])

    return dna

def OverlapGraph(kmerArray):
    k = len(kmerArray)
    result = dict.fromkeys(kmerArray)
    for key in result:
        zmienna = next( (i for i in kmerArray if key.endswith(i[:-1]) ), None)
        result[key] = zmienna
        if not zmienna:
            lastElem = key
        else:
            kmerArray.remove(zmienna)
    del result[lastElem]
    return kmerArray[0], result

def DeBruijn(Text):
    textArray = [elem[:-1] for elem in Text]
    result = dict.fromkeys(textArray)
    for key in result:
        zmienna = [i[1:] for i in Text if key.endswith(i[:-1])]
        zmienna.sort()
        result[key] = zmienna
    return result

def DeBruijn(k, Text):
  result = dict()
  result = ({Text[i:i+k-1]: None for i in range(len(Text) - k + 2)})
  for key in result:
    searchArr = [Text[i:(i+k)] for i in range(len(Text) - k+1)]
    for elem in searchArr:
      if key.endswith(elem[0:-1]):
        if result[key]:
          result[key].append(elem[:-1])
        else:
          result[key] = [elem[:-1]]
  return result

def EulerianCycle(graph_dict):
    currentNode = list(graph_dict.keys())[0]
    path = [currentNode]
    while True:
        path.append(list(graph_dict[currentNode])[0])
        if len(graph_dict[currentNode]) == 1:
            del graph_dict[currentNode]
        else:
            graph_dict[currentNode] = graph_dict[currentNode][1:]
        if path[-1] in graph_dict:
            currentNode = path[-1]
        else:
            break
    while len(graph_dict) > 1:
        for i in range(len(path)):
            if path[i] in graph_dict:
                currentNode = path[i]
                middleCycle = [currentNode]
                while True:
                    middleCycle.append(list(graph_dict[currentNode])[0])
                    if len(graph_dict[currentNode]) == 1:
                        del graph_dict[currentNode]
                    else:
                        graph_dict[currentNode] = graph_dict[currentNode][1:]
                    if middleCycle[-1] in graph_dict:
                        currentNode = middleCycle[-1]
                    else:
                        break
                path = path[:i] + middleCycle + path[i+1:]
    return path

def EulerianCycle(graph_dict, firstKey):
    currentNode = list(graph_dict[firstKey])[0]
    graph_dict[firstKey] = graph_dict[firstKey][1:]
    path = [firstKey, currentNode]
    while True:
        path.append(list(graph_dict[currentNode])[0])
        if len(graph_dict[currentNode]) == 1:
            del graph_dict[currentNode]
        else:
            graph_dict[currentNode] = graph_dict[currentNode][1:]
        if path[-1] in graph_dict:
            currentNode = path[-1]
        else:
            break
    while len(graph_dict) > 1:
        for i in range(len(path)):
            if path[i] in graph_dict:
                currentNode = path[i]
                middleCycle = [currentNode]
                while True:
                    middleCycle.append(list(graph_dict[currentNode])[0])
                    if len(graph_dict[currentNode]) == 1:
                        del graph_dict[currentNode]
                    else:
                        graph_dict[currentNode] = graph_dict[currentNode][1:]
                    if middleCycle[-1] in graph_dict:
                        currentNode = middleCycle[-1]
                    else:
                        break
                path = path[:i] + middleCycle + path[i+1:]
    return path


def EulerianPath(graph_dict):
    first = findUnbalancedNode(graph_dict)
    #del graph_dict[first]
    #del graph_dict[last]
    path = EulerianCycle(graph_dict, first)
    return path

def findUnbalancedNode(graph):
    inDegree = -1
    values = []
    for i in graph:
        for value in graph[i]:
            values.append(value)
    keys = set(graph.keys())
    for key in keys:
        valueCounter = values.count(key)
        if valueCounter < len(graph[key]):
            inDegree = key
    return inDegree
