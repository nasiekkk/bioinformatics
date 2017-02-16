import complementarity
def ProteinTranslation(rna, geneticCode):
  result = ""
  for i in range(0, len(rna) - 2, 3):
    codon = rna[i:i+3]
    aminoacid = geneticCode.get(codon)
    if aminoacid != []:
        result = result + aminoacid
    else:
      break
  return result

def PeptideEncodingOneStrand(dna, peptide, geneticCode):
  rna = dna.replace("T", "U")
  l = 3*len(peptide)
  aminoacids = [rna[i:i+l] for i in range(len(rna)-l+1) if ProteinTranslation(rna[i:i+l], geneticCode) == peptide]
  return aminoacids

def ConvertRnaToDna(rna):
    return rna.replace("U", "T")

def PeptideEncoding(dna, peptide, geneticCode):
    result = []
    oneStrandRna = PeptideEncodingOneStrand(dna, peptide, geneticCode)
    oneStrandDna = [ConvertRnaToDna(oneStrandRna[i]) for i in range(len(oneStrandRna))]
    complementary = complementarity.find_complementary(dna)
    complStrandRna = PeptideEncodingOneStrand(complementary, peptide, geneticCode)
    complStrandDna = [ConvertRnaToDna(complStrandRna[i]) for i in range(len(complStrandRna))]
    transArr = [complementarity.find_complementary(complStrandDna[i]) for i in range(len(complStrandDna))]
    result.append(oneStrandDna)
    result.append(transArr)
    return result

def ReadCodonTable(name):
    with open(name, 'r') as f:
        return {line[0:3]:line[4] for line in f.readlines()}

def ReadMassTable(name):
    with open(name, 'r') as f:
        return {line[0]:line[2:-1] for line in f.readlines()}

def CountSubpeptides(n):
    return n*n(-1)

def LinearSpectrum(peptide, aminoAcid, aminoAcidMass):
    prefixMass = [0]
    for i in range(0, len(peptide)):
        for j in range(0, 20):
            a = aminoAcid[j]
            if aminoAcid[j] == peptide[i]:
                prefixMass.append(prefixMass[i] + aminoAcidMass[j])
    linearSpectrum = [0]
    for i in range(0, len(prefixMass)-1):
        for j in range(i+1, len(prefixMass)):
            linearSpectrum.append(prefixMass[j] - prefixMass[i])
    linearSpectrum.sort()
    return linearSpectrum

def CyclicSpectrum(peptide, aminoAcid, aminoAcidMass):
    prefixMass = [0]
    for i in range(0, len(peptide)):
        for j in range(0, 20):
            a = aminoAcid[j]
            if aminoAcid[j] == peptide[i]:
                prefixMass.append(prefixMass[i] + aminoAcidMass[j])
    peptideMass = prefixMass[len(peptide)]
    cyclicSpectrum = [0]
    for i in range(0, len(prefixMass)-1):
        for j in range(i+1, len(prefixMass)):
            cyclicSpectrum.append(prefixMass[j] - prefixMass[i])
            if i > 0 and j < len(peptide):
                cyclicSpectrum.append(peptideMass - (prefixMass[j] - prefixMass[i]))
    cyclicSpectrum.sort()
    return cyclicSpectrum

def CountPeptidesWithGivenMass(mass, aminoAcidMassTable):
    counter = 0
    peptides = []
    for i in aminoAcidMassTable:
        if mass < aminoAcidMassTable[0]:
            break
        if mass - i == 0:
            counter += 1
        if mass > i:
            counter += CountPeptidesWithGivenMass(mass-i, aminoAcidMassTable)
    return counter

def CountPeptidesGitHub(mass, aminoAcidMassTable):
    mass += 1
    aminoAcidMassTable = [v for i, v in enumerate(aminoAcidMassTable)
              if i == 0 or i > 0 and aminoAcidMassTable[i - 1] != v]
    peptides = [0 for i in range(mass)]
    for i in range(mass):
        for k in aminoAcidMassTable:
            if i - k > 0:
                peptides[i] += peptides[i - k]
            elif i - k == 0:
                peptides[i] += 1
    print(peptides[-1])

def CountLinearSubpeptide(m):
    return ((m*(m+1))/2)+1

# def Expand(peptides):
#     return peptides
#
# def CyclopeptideSequencing(spectrum, massTable, aminoAcidTable):
#     peptides = [0]
#     while peptides:
#         Expand(peptides)
#         for peptide in range(len(peptides)):
#             if massTable[peptide] == spectrum[-1]:
#                 if CyclicSpectrum(peptide, aminoAcidTable, massTable)

