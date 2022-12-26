
def isConsistentPositive(d, Item):
    for i in range(0, len(Item)):
        if(Item[i] != d[i] and Item[i] != '?'):
            return False
    return True


def isConsistentNegative(d, item):
    return not isConsistentPositive(d, item)


def minimalGeneralizationOfS(d, SItem):
    SItem = [d[i] if SItem[i] == "0" or SItem[i] ==
             d[i] else "?" for i in range(0, len(SItem))]

    return SItem


def minimalSpecializationOfG(d, GItem, all_values):
    specializations = []
    for i in range(0, len(GItem)):
        if(GItem[i] == "?"):
            for value in all_values[i]:
                if(value != d[i]):
                    temp = GItem[:]
                    temp[i] = value
                    specializations.append(temp)

    return specializations


def isMoreGeneralThan(SItem, G):
    length = len(SItem)
    for GItem in G:
        NoMGS = 0  # number_of_more_general_statments in s than G
        for i in range(0, length):
            if(SItem[i] == GItem[i] or SItem[i] == "?"):
                NoMGS += 1
        if(NoMGS == length):
            return True
    return False


def getAllPosibleValues(examples, number_of_columns):
    all_possible_values = [[] for i in range(0, number_of_columns)]

    last_index = number_of_columns
    for d in examples:
        for i in range(0, last_index):
            try:
                all_possible_values[i].index(d[i])
            except ValueError as ve:
                all_possible_values[i].append(d[i])
    return all_possible_values


def CandidateElimination(examples, all_possible_values=False):

    number_of_columns = len(examples[0])-1
    G = [['?', ]*number_of_columns]
    S = [['0', ]*number_of_columns]
    if(all_possible_values == False):
        all_possible_values = getAllPosibleValues(
            examples[1:], number_of_columns)

    for d in examples[1:]:  # for every example
        if(d[-1] == "Y"):  # positive examples
            tempG = []
            for item in G:  # Remove from G any inconsistent hypothesis
                if isConsistentPositive(d, item):
                    tempG.append(item)
            G = tempG[:]
            tempS = []
            for item in S:  # Remove from S any inconsistent hypothesis

                if isConsistentPositive(d, item):
                    tempS.append(item)
                else:
                    # minmal generalization of the removed s
                    newS = minimalGeneralizationOfS(d, item)
                    if(isMoreGeneralThan(item, G) == False):
                        tempS.append(newS)

            S = tempS[:]
            tempS = []
            for item in S:
                if(isMoreGeneralThan(item, tempS) == False):
                    tempS.append(item)
            S = tempS[:]

        else:  # Negative Examples
            tempS = []
            for item in S:  # Remove from S any inconsistent hypothesis
                # we consider it a positive example. if it's consistent with a statment, then it's Actually inconsistent

                if isConsistentNegative(d, item):
                    tempS.append(item)
            S = tempS[:]

            tempG = []
            for item in G:
                if isConsistentNegative(d, item):
                    tempG.append(item)
                else:
                    temp = minimalSpecializationOfG(
                        d, item, all_possible_values)
                    tempG = tempG + temp
            G = tempG[:]
            tempG = []
            for g in G:
                if(isMoreGeneralThan(g, S) and isMoreGeneralThan(g, G)):
                    tempG.append(g)

            G = tempG[:]

    V = [G, S]
    return V
