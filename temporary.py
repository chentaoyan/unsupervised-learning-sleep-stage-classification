import numpy as np

myFeature =np.loadtxt("resultOfMyModel/averageFeature.csv")
baselineFeature = np.loadtxt("resultOfBaselineModel/averageFeature.csv")
#
# print(myFeature)
# print(baselineFeature)
totalError = []
for feature in myFeature:
    error = []
    for baseFeature in baselineFeature:
        dist = np.linalg.norm(feature - baseFeature)
        error.append(dist)
    # print(error)
    totalError.append(error)


import itertools
choices = list(itertools.permutations([0, 1, 2, 3, 4]))
# print(choices)
final_choice = 0
minError = 10000000
for choice in choices:
    tempError = 0
    tempMatch = [0]*5
    for i in range(5):
        if choice[i] == 2 :  #S2
            tempMatch[choice[i]] = 2*totalError[i][choice[i]]
            tempError += 2*totalError[i][choice[i]]
        elif choice[i] == 4 :  #REM
            tempMatch[choice[i]] = 2*totalError[i][choice[i]]
            tempError += 2*totalError[i][choice[i]]
        else:
            tempMatch[choice[i]] = totalError[i][choice[i]]
            tempError += totalError[i][choice[i]]

    if tempError<=5212.28625859:
        print(tempMatch)
        print(tempError)
        print(choice)

    if tempError<minError:
        minError = tempError
        final_choice = choice
print(minError)
print(final_choice)
