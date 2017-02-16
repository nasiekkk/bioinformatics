from itertools import product
import math

def findLastKmer(kmerArray):
    for kmer in kmerArray:
        counter = 0
        k = len(kmerArray[0])
        for i in range(len(kmerArray)):
            aaa = kmerArray[i]
            if kmer[1:] == aaa[0:k - 1]:
                counter += 1
                break
    if counter == 0:
        return kmer

def ReconstructString(kmerArray):
    k = len(kmerArray[0])
    dna = findLastKmer(kmerArray)
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

def DeBruijnFromArray(Text):
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

def EulerianCycle(graph_dict, firstKey):
    currentNode = list(graph_dict.keys())[0]
    #graph_dict[firstKey] = graph_dict[firstKey][1:]
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

def EulerianPath(graph):
  result = []
  result.append(list(graph.keys())[0])
  while graph:
    currentKey = result[-1]
    if graph[currentKey]:
      result.append(graph[currentKey])
      if len(graph[currentKey] > 1):
        del graph[currentKey]
      currentKey = result[-1]
  return result

def FindFirstKey(kmerArray):
    for kmer in kmerArray:
        counter = 0
        k = len(kmerArray[0])
        for i in range(len(kmerArray)):
            if kmer[:k-1] == kmerArray[i][1:]:
                counter += 1
                break
        if counter == 0:
            return kmer

def StringReconstructionUsingEulerDeBruijn(k, kmerArray):
    result = ""
    firstKey = FindFirstKey(kmerArray)
    graph = DeBruijnFromArray(kmerArray)
    sortedKmers = EulerianCycle(graph, firstKey[:-1])
    for i in range(len(sortedKmers)-1):
        result = result + sortedKmers[i][0]
    return result + sortedKmers[len(sortedKmers)-1]

def UniversalCircularString(k):
    graph = {}
    for kmer in [''.join(item) for item in product('01', repeat=k)]:
        if kmer[:-1] in graph:
            graph[kmer[:-1]].append(kmer[1:])
        else:
            graph[kmer[:-1]] = [kmer[1:]]
    #firstKey = list(graph.keys())[0]
    path = EulerianCycle(graph, '0')
    result = path[0][0]
    for i in range(1, len(path)):
        result = result + path[i][:-1]
    return result + path[len(path)-1][:-1]

def StringSpelledByGappedPatterns(k, d, patternArray):
    result = ''
    i = 0
    for i in range(0, len(patternArray), k):
        result = result + patternArray[i][0]
    result = result[:-(i-d)]
    for j in range(0, len(patternArray), k):
        result = result + patternArray[j][1]
    return result