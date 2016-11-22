import operator

def amount_kmers(looking, dna):
    result = 0
    for i in range(len(dna) - len(looking)):
        if dna[i:i+len(looking)] == looking:
            result = result+1
    return result

def longest_kmer(length, dna):
    freq_kmer = dict()
    for i in range(len(dna) - length):
        mer = dna[i:i+length]
        if mer in freq_kmer:
            freq_kmer[mer] = freq_kmer[mer] + 1
        else:
            freq_kmer[mer] = 1
    sorted_freq = sorted(freq_kmer.items(), key=operator.itemgetter(1))
    ii = sorted_freq.index(max(sorted_freq, key=operator.itemgetter(1)))
    return sorted_freq[ii:]

def find_indexes(dna, looking):
    result = []
    for i in range(len(dna) - len(looking)):
        if dna[i:i+len(looking)] == looking:
            result.append(i)
    return result

looking = "AA"
dna = "CGGAGGACTCTAGGTAACGCTTATCAGGTCCATAGGACATTCA"

a = longest_kmer(3, dna)
print(a)
