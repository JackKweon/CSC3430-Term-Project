from fileinput import filename
from collections import deque
import re

dataList = []  # The file that has all the input value

classWpre = []  # classes with prerequisites -- [i][0] = classname & [i][j>0] = required classes
classWpreSorted = []  # classes with prerequisites, sorted by topology sort, forms what classes need to take first

classCode = []
degreeCheck = []
classWpreInfo = []
classWOpre = []  # classes without prerequisites

finalPlan = []


# Read File from user input file,
def readFile(fileName):
    try:
        data = open(fileName, 'r')
    except OSError:
        print("could not open/read the file: ", fileName)

    with data:
        line = data.readline()

        line_Numb = 0
        index = []
        tmp = ''
        inBracket = False

        while (line):
            dataList.append([])

            # save the data wihtout '[', ']', '\n', and ','(except ',' inside of [])
            for i in line:
                if i == '[':
                    inBracket = True
                if i == ',' and inBracket == False:
                    if tmp != '':
                        index.append(tmp)
                        tmp = ''
                if i == ']':
                    index.append(tmp)
                    inBracket = False
                    tmp = ''
                if i != ',' and inBracket == False:
                    if i != '\n' and i != ']':
                        tmp = tmp + i
                if inBracket == True:
                    if i != '[' and i != ']':
                        tmp = tmp + i

            for i in range(len(index)):
                dataList[line_Numb].append(index[i])
            index.clear()
            line = data.readline()
            line_Numb += 1


# This function will divide the dataList into classWpre(prerequisit, later use for topology sort) and classWOpre
def seperateClass():
    # Save the name of the class and name of prerequisit classes from the dataList to tmp
    tmp = []
    tmpExtra = []
    valCount = 0

    # If prerequisit exsits, save the class code, prerequisit class codes into the tmp list
    for i in range(len(dataList)):
        if dataList[i][3] != " ":
            tmp.append([])
            tmp[valCount].append(dataList[i][0])
            tmp[valCount].append(dataList[i][3])
            valCount += 1

        # If does not exist, then save the class code to the tmpExtra
        elif dataList[i][3] == " ":
            tmpString = dataList[i][0].replace(' ', '')
            tmpExtra.append(tmpString)

    # Save the prerequisit information seperated by comma, and deliver those elements to classWpre list
    tmp2 = []
    for i in range(len(tmp)):
        tmp2 = tmp[i][1].split(',')
        del tmp[i][1]
        for j in range(len(tmp2)):
            tmp[i].append(tmp2[j])
        tmp2.clear

        # After seperated by comma, remove all whitespace betweeen class code
    for i in range(len(tmp)):
        classWpre.append([])
        for j in range(len(tmp[i])):
            tmpString = ''
            tmpString = tmp[i][j].replace(' ', '')
            classWpre[i].append(tmpString)

            # have all the classCode -- ex)csc1230
    for i in range(len(classWpre)):
        for j in range(len(classWpre[i])):
            if classWpre[i][j] not in classCode:
                classCode.append(classWpre[i][j])
    numbClass = len(classCode)

    for i in range(len(classCode)):
        degreeCheck.append(0)

    for i in range(len(classWpre)):
        for j in range(len(classWpre[i])):
            if j > 0:
                # if j has prerequisit, add one to degreeCheck
                degreeCheck[classCode.index(classWpre[i][0])] += 1

    count = 0
    for i in range(len(dataList)):
        checkClass = ''
        checkClass = dataList[i][0].replace(' ', '')
        if checkClass in classCode:
            classWpreInfo.append([])
            classWpreInfo[count].append(checkClass)  # 0. CSC 1230
            classWpreInfo[count].append(False)  # 1. TAKEN? => TRUE OR FALSE
            classWpreInfo[count].append(dataList[i][4])  # 2. Quarter => 1,2,3
            classWpreInfo[count].append(dataList[i][2])  # 3. Credit => 5
            checkPrerequisite = dataList[i][3].replace(' ', '')
            if checkPrerequisite != '':  # 4. Prerequisite Taken?
                classWpreInfo[count].append(False)
            elif checkPrerequisite == '':
                classWpreInfo[count].append(True)
            count += 1

            # Find the common value between classWpre and tmpExtra, save those element into tmp4
    tmp4 = []
    for i in range(len(classCode)):
        for j in range(len(tmpExtra)):
            if classCode[i] == tmpExtra[j]:
                tmp4.append(classCode[i])

    # Remove the element from tmpExtra that is already in classWpre
    for i in range(len(tmp4)):
        tmpExtra.remove(tmp4[i])

    count = 0
    for i in range(len(dataList)):
        checkClass = ''
        checkClass = dataList[i][0].replace(' ', '')
        if checkClass in tmpExtra:
            classWOpre.append([])
            classWOpre[count].append(checkClass)  # UCOR 3000
            classWOpre[count].append(False)  # TAKEN? => TRUE OR FALSE
            classWOpre[count].append(dataList[i][4])  # Quarter => 1,2,3
            classWOpre[count].append(dataList[i][2])  # Credit => 5
            count += 1


def createPlan(quarter, credit, classTaken):
    currentQuarter = quarter
    maxCredit = int(credit)
    count = 0
    finishclass = 0
    while (finishclass):
        finalPlan.append([])  # new quarter
        currentCredit = 0
        tmpClass = []
        for i in range(len(classWpreInfo)):
            if classWpreInfo[i][1] == True:
                pass
            else:  # class not taken
                if currentQuarter in classWpreInfo[i][2]:  # quarter match
                    if currentCredit + int(classWpreInfo[i][3]) < maxCredit:  # enough credit to take
                        if classWpreInfo[i][4] == True:  # Prerequisite fullfilled
                            finalPlan[count].append(classWpreInfo[i][0])
                            currentCredit += (int(classWpreInfo[i][3]))
                            classWpreInfo[i][1] = True
                            tmpClass.append(classWpreInfo[i][0])

        for classCode in tmpClass:
            updatePrerequisite(classCode)
        del tmpClass

        for i in range(len(classWOpre)):
            if classWOpre[i][1]:
                pass
            else:  # class not taken
                if currentQuarter in classWOpre[i][2]:  # quarter match
                    if currentCredit + int(classWOpre[i][3]) < maxCredit:  # enough credit to take
                        finalPlan[count].append(classWOpre[i][0])
                        currentCredit += (int(classWOpre[i][3]))
                        classWOpre[i][1] = True


        if currentQuarter == '1':
            currentQuarter = '2'
        elif currentQuarter == '2':
            currentQuarter = '3'
        elif currentQuarter == '3':
            currentQuarter = '1'
        count += 1


def printPlan():
    for i in range(len(finalPlan)):
        print(i, ' : ')
        for j in range(len(finalPlan[i])):
            print(finalPlan[i][j], end=' ')
        print(' ')


def updatePrerequisite(className):
    current = className

    tmp = []  # store all the classes that has prerequised of current class
    for i in range(len(classWpre)):
        for j in range(len(classWpre[i])):
            if j > 0:
                if classWpre[i][j] == current:
                    tmp.append(classWpre[i][0])

    tmp2 = []  # store index of prerequisite
    # chagne class code to index number to calcualte the degreeCheck
    for i in tmp:
        tmp2.append(classCode.index(i))

    for i in tmp2:
        degreeCheck[i] -= 1

    tmp3 = []
    for i in range(len(degreeCheck)):
        if degreeCheck[i] == 0:
            tmp3.append(classCode[i])

    for i in range(len(classWpreInfo)):
        for j in range(len(tmp3)):
            if classWpreInfo[i][0] == tmp3[j]:
                classWpreInfo[i][4] = True


fName = input("Please type the file name: ")
readFile(fName)
seperateClass()
createPlan('2', '18', 0)
printPlan()
