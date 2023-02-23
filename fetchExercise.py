import sys
import csv

def negPoints(currList, currIndex, negNumPoints):
    for i in range(len(currList)):
        if i == currIndex:
            continue
        points = currList[i]["points"]
        
        if points >= abs(negNumPoints):
            currList[i]["points"] = points - abs(negNumPoints)
            currList[currIndex]["points"] = 0
            break
        else:
            currList[currIndex]["points"] = points - abs(negNumPoints)
            negNumPoints = points - abs(negNumPoints)
            currList[i]["points"] = 0
    return currList

if __name__ == "__main__":
    totalNumPoints = int(sys.argv[1])
    filename = str(sys.argv[2])
    
    #read through the provided csv file and append each payer to pointList
    pointList = [] #holds all the payers from the provided csv file
    with open(filename) as pointData:
        csv_reader = csv.DictReader(pointData)
        for person in csv_reader:
            pointList.append(person)
            person["points"] = int(person["points"])
    #sort pointList based on their timestamp, oldest are first
    pointList = sorted(pointList, key=lambda x: x["timestamp"], reverse=False)

    #iterate through pointList to spend totalNumPoints
    index = 0 #used to help change pointList values
    for person in pointList:
        currPoints = person["points"] #number of points current payer has, cast to int as it is a string right now

        if currPoints < 0: #current payer's number of points is negative, call negPoints to deal with this
            pointList = negPoints(pointList, index, currPoints)
        else:
            if currPoints >= totalNumPoints: #current point total greater than total number of points to spend
                pointList[index]["points"] = (currPoints - totalNumPoints)
                totalNumPoints = 0
                break #all points spent, exit for loop
            else:
                totalNumPoints = totalNumPoints - currPoints
                pointList[index]["points"] = 0 
        index += 1

    #print out payers and their point values in correct format
    outputDict = dict()
    for person in pointList:
        if person["payer"] in outputDict.keys():
            outputDict[person["payer"]] += person["points"]
        else:
            outputDict[person["payer"]] = person["points"]
    print(outputDict)