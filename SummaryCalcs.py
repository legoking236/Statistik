import math
import Tkinter

def mean(PassDataList):
    if len(PassDataList) == 0:
        return "N/A"
    total = 0
    for item in PassDataList:
        total += item
    return round(total / len(PassDataList), 3)
def median(PassDataList):
    if len(PassDataList) == 0:
        return "N/A"
    FindMed = sorted(PassDataList)
    if len(FindMed)%2 == 0 and len(FindMed) > 1:
        return (FindMed[int(len(FindMed)/2)-1] + FindMed[int(len(FindMed)/2)])/2
    elif len(FindMed) == 1:
        return FindMed[0]
    else:
        return FindMed[int((len(FindMed)-1)/2)]
def mode(PassDataList):
    if len(PassDataList) == 0:
        return "N/A"
    return max(set(PassDataList), key=PassDataList.count)
def minimum(PassDataList):
    if len(PassDataList) == 0:
        return "N/A"
    mini = PassDataList[0]
    for item in PassDataList:
        if item < mini:
            mini = item
        else:
            continue
    return mini
def maximum(PassDataList):
    if len(PassDataList) == 0:
        return "N/A"
    maxi = PassDataList[0]
    for item in PassDataList:
        if item > maxi:
            maxi = item
        else:
            continue
    return maxi
def calRange(PassDataList):
    if len(PassDataList) == 0:
        return "N/A"
    elif len(PassDataList) == 1:
        return "N/A"
    return maximum(PassDataList) - minimum(PassDataList)
def stadard(PassDataList):
    if len(PassDataList) == 0:
        return "N/A"
    SDmean = mean(PassDataList)
    variance = []
    for item in PassDataList:
        variance.append(item - SDmean)
    varTot = 0
    for item in variance:
        varTot += (item * item)
    varTot = varTot/len(variance)
    return round(math.sqrt(varTot), 3)
def quar1(PassDataList):
    if len(PassDataList) == 0:
        return "N/A"
    elif len(PassDataList) % 2 == 0:
        FindMed = sorted(PassDataList)
        quar1maxI = int(len(FindMed)/2)
        calQuar1 = []
        for x in range(0, quar1maxI):
            calQuar1.append(FindMed[x])
        return median(calQuar1)
    elif len(PassDataList) == 1:
        return 0.0
    else:
        FindMed = sorted(PassDataList)
        medIndex = int((len(FindMed)-1)/2)
        calQuar1 = []
        for x in range(0, medIndex):
            calQuar1.append(FindMed[x])
        return median(calQuar1)
def quar3(PassDataList):
    if len(PassDataList) == 0:
        return "N/A"
    elif len(PassDataList) % 2 == 0:
        FindMed = sorted(PassDataList)
        quar3minI = int(len(FindMed)/2)
        calQuar3 = []
        for x in range(quar3minI, len(FindMed)):
            calQuar3.append(FindMed[x])
        return median(calQuar3)
    elif len(PassDataList) == 1:
        return 0.0
    else:
        FindMed = sorted(PassDataList)
        medIndex = int((len(FindMed)-1)/2)
        calQuar3 = []
        for x in range(medIndex+1, len(FindMed)):
            calQuar3.append(FindMed[x])
        return median(calQuar3)
def calIQR(PassDataList):
    if len(PassDataList) == 0:
        return "N/A"
    else:
        return quar3(PassDataList) - quar1(PassDataList)
