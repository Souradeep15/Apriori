from itertools import combinations
import pandas as pd

def database(data, minsupport, minlen):
    ts=pd.get_dummies(data.unstack().dropna()).groupby(level=1).sum()
    collen, rowlen  =ts.shape
    pattern = []
    for colnum in range(minlen, rowlen+1):
        for cols in combinations(ts, colnum):

            patsum = ts[list(cols)].all(axis=1).sum()
            pattern.append([",".join(cols), patsum])
    sdf = pd.DataFrame(pattern, columns=["Pattern", "Support"])
    results=sdf[sdf.Support >= minsupport]
    freqset = results.reset_index(drop=True).values
    return freqset

def frequentItemSets(frequentSets):
    sets=[]
    for value,key in frequentSets:
        lens = str(value).split(',')
        freq=[]
        #print(lens)
        if len(lens)>1:
            for j in range(len(lens)):
                freq.append("".join(list(lens[j])))
            sets.append(freq)
            sets.append(key)
        else:
            sets.append([",".join(lens)])
            sets.append(key)
    return sets
def defassociationRule(associationSets):
    associationRule = []
    for item in associationSets:
        if isinstance(item, list):
            if len(item) != 0:
                length = len(item) - 1
                while length > 0:
                    combination = list(combinations(item, length))
                    temp = []
                    for Rkey in combination:
                        Lkey = set(item) - set(Rkey)
                        temp.append(list(Lkey))
                        temp.append(list(Rkey))
                        associationRule.append(temp)
                        temp = []
                    length = length - 1
    return associationRule
def confidenceSets(rules_for_association,data,minimumConfidence):
    Output = []
    noOfTransactions = len(data)
    for rule in rules_for_association:
        supportOfX = 0
        supportOfXinPercentage = 0
        supportOfXandY = 0
        supportOfXandYinPercentage = 0
        for transaction in data:

            if set(rule[0]).issubset(set(transaction)):
                supportOfX = supportOfX + 1
            if set(rule[0] + rule[1]).issubset(set(transaction)):
                supportOfXandY = supportOfXandY + 1
        supportOfXinPercentage = (supportOfX * 1.0 / noOfTransactions) * 100
        supportOfXandYinPercentage = (supportOfXandY * 1.0 / noOfTransactions) * 100
        confidence = (supportOfXandYinPercentage / supportOfXinPercentage) * 100
        if confidence >= minimumConfidence:
            supportOfXAppendString = str(rule[0])+":"+ str(round(supportOfXinPercentage, 2))
            supportOfXandYAppendString = str(rule[0])+" & "+str(rule[1])+": " + str(round(supportOfXandYinPercentage))
            confidenceAppendString = str(round(confidence))
            returnAprioriOutput=[]
            returnAprioriOutput.append(supportOfXAppendString)
            returnAprioriOutput.append(supportOfXandYAppendString)
            returnAprioriOutput.append(confidenceAppendString)
            returnAprioriOutput.append(str(rule[0])+"-->"+str(rule[1]))
            Output.append(returnAprioriOutput)
    return Output

print("Select from the following dataset: ")
print("1. Office Products")
print("2. Groceries")
print("3. Electronics")
print("4. Clothes")
print("5. Kitchen Utensils")
print("\n")
fileNameInput = input("Enter File Number: ")
minSupport = input("Enter Minimum Support: ")
minConf = input("Enter Minimum Confidence: ")

if fileNameInput == '1':
    fileName = 'Office_depot.txt'
if fileNameInput == '2':
    fileName = 'Walmart.txt'
if fileNameInput == '3':
    fileName = 'Amazon.txt'
if fileNameInput == '4':
    fileName = 'Asos.txt'
if fileNameInput == '5':
    fileName = 'Target.txt'
read_file = pd.read_csv(fileName, index_col=0)
dataSet = read_file.values
minSupport = (int(minSupport))*20/100
minConf = int(minConf)
transform_dataset = database(read_file,minSupport, 1)
frequent = frequentItemSets(transform_dataset)
rules_association = defassociationRule(frequent)
output = confidenceSets(rules_association,dataSet,minConf)
counter = 1
if len(output) == 0:
    print("There are no association rules for this support and confidence.")
else:
    pd.set_option('display.max_columns',None)
    df= pd.DataFrame(output,columns=["Support(X)","Support(XUY)", "Confidence", "Rule"])
    print(df)




