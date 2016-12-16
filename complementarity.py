def find_complementary(dna):
    result = ""
    for i in range(len(dna)):
        if dna[i] == "A":
            result = result + "T"
        if dna[i] == "T":
            result = result + "A"
        if dna[i] == "G":
            result = result + "C"
        if dna[i] == "C":
            result = result + "G"
    res = revert(result)
    return res

def revert(str):
    result = ""
    for i in range(len(str)):
        result = result + str[len(str)-i-1]
    return result
