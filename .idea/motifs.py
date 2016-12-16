import skew_diagram
import math
from random import randint

def calcProbability(dna):
    length = len(dna)
    countA = sum([a == 'A' for a in dna])
    countC = sum([c == 'C' for c in dna])
    countG = sum([g == 'G' for g in dna])
    countT = sum([t == 'T' for t in dna])
    result = [countA / length, countC / length, countG / length, countT / length]
    return result

def calcProbabilityWithSuccession(dna):
    length = len(dna) + 4
    countA = sum([a == 'A' for a in dna])+1
    countC = sum([c == 'C' for c in dna])+1
    countG = sum([g == 'G' for g in dna])+1
    countT = sum([t == 'T' for t in dna])+1
    result = [countA / length, countC / length, countG / length, countT / length]
    return result

def calcProfiles(stringArr):
    scores = []
    for index in range(0, len(stringArr[0])):
        score = calcProbability([i[index] for i in stringArr])
        scores.append(score)
    return scores

def calcProfilesWithSuccession(stringArr):
    scores = []
    for index in range(0, len(stringArr[0])):
        score = calcProbabilityWithSuccession([i[index] for i in stringArr])
        scores.append(score)
    return scores

def DistanceBetweenPatternAndString(pattern, dna):
    k = len(pattern)
    distance = 0
    for text in dna:
        hammingDistance = k+10000
        for j in range(len(text)-len(pattern)+1):
            pattern_p = text[j:j+k]
            currentHammingDistance = skew_diagram.findHammingDistance(pattern, pattern_p)
            hammingDistance = min(hammingDistance, skew_diagram.findHammingDistance(pattern, pattern_p))
        distance = distance + hammingDistance
    return distance

def MedianString(dna, k):
    distance = len(dna)+1000
    median = []
    for i in range(0, pow(4,k)):
        pattern = skew_diagram.numberToPattern(i,k)
        currentDistance = DistanceBetweenPatternAndString(pattern, dna)
        if distance > currentDistance:
            distance = currentDistance
            median.append(pattern)
    return median

def MostProbableKMer(dna, k, profileArr):
    kmers = []
    probability = []
    A = profileArr[0:k]
    C = profileArr[k:2*k]
    G = profileArr[2*k:3*k]
    T = profileArr[3*k:]
    for i in range(len(dna)-k):
        text = dna[i:i+k]
        kmers.append(text)
        prob = 1
        for j in range(0, k):
            if text[j] == 'A':
                prob *= A[j]
            elif text[j] == 'C':
                prob *= C[j]
            elif text[j] == 'G':
                prob *= G[j]
            else:
                prob *= T[j]
        probability.append(prob)
    maxProbabilityInd = probability.index(max(probability))
    return kmers[maxProbabilityInd]

def ScoreMotif(profiles):
    score = 0
    for elem in profiles:
        score += 1 - max(elem)
    return score

def GreedyMotifSearch(dna, k, t):
    profiles = []
    bestMotifs = [i[0:k] for i in dna]
    bestMotifsScore = k
    motifs = []
    for i in range(len(dna[0])-k):
        motifs.append(dna[0][i:i+k])
        for j in range(1,t):
            p = calcProfilesWithSuccession(motifs)
            profiles.append(p)
            new_motif = MostProbableKMer(dna[j], k, transposeProfile(p))
            motifs.append(new_motif)
        p = calcProfilesWithSuccession(motifs)
        score = ScoreMotif(p)
        if score < bestMotifsScore:
            bestMotifs = motifs[:]
            bestMotifsScore = score
        motifs.clear()
    return bestMotifs

def transposeProfile(profile):
    result = []
    for i in range(len(profile[0])):
        for j in range(len(profile)):
            result.append(profile[j][i])
    return result

def calcEntropy(probArr):
  res = 0
  for i in range(0, 4):
    if probArr[i] == 0:
      res += 0
    else:
      res =  res + (probArr[i] * math.log(probArr[i],2))
    print(i)
  return -res

def RandomizedMotifSearch(dna, k, t):
    bestMotifs = []
    bestMotifScore = k
    for _ in range(1000):
        motifs = []
        for i in range(0, t):
            index = randint(0, len(dna[0]) - k)
            motifs.append(dna[i][index: index + k])

        profile = calcProfilesWithSuccession(motifs)
        motifs = [MostProbableKMer(d, k, transposeProfile(profile)) for d in dna ]
        currentProfile = calcProfilesWithSuccession(motifs)
        currentScore = ScoreMotif(currentProfile)

        if currentScore < bestMotifScore:
            bestMotifs = motifs[:]
            bestMotifScore = currentScore

    print(bestMotifScore)
    return bestMotifs

def RandomizedMotifSearch2(dna, k, t):
    motifs = []
    for i in range(0, t):
        index = randint(0, len(dna[0]) - k)
        motifs.append(dna[i][index: index + k])
    bestMotifs = motifs[:]
    bestMotifScore = k
    for _ in range(1000):
        profile = calcProfilesWithSuccession(motifs)
        motifss = [MostProbableKMer(d, k, transposeProfile(profile)) for d in dna ]
        motifs.append(motifss)
        currentProfile = calcProfilesWithSuccession(motifs)
        currentScore = ScoreMotif(currentProfile)

        if currentScore < bestMotifScore:
            bestMotifs = motifs[:]
            bestMotifScore = currentScore

    print(bestMotifScore)
    return bestMotifs

