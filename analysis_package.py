import pandas as pd
from tkinter import filedialog
from tkinter import *
import matplotlib.pyplot as plt
import os



def reader():
    root = Tk()
    root.filename = filedialog.askopenfilename(initialdir="/", title="Select file",
                                               filetypes=(("CSV files", "*.csv"), ("all files", "*.*")))
    fileName = root.filename
    data = pd.read_csv(fileName)
    #print(data.head(20))
    return data

# returns all relevant information to construct pie chart
def undergradGrad(data):
    length = len(data.index)
    labels = ['Undergraduate', 'Graduate', 'Unknown']
    dataSizes = [0,0,0]
    valueList = list(data['dupsacadcareerdescc1'])
    #print(valueList)
    for value in valueList:
        #Check for NaN value
        if value != value:
            dataSizes[2] += 1
            continue
        # Check for Undergraduates
        if (value == 'Undergraduate'):
            dataSizes[0] += 1
            continue
        # Check for Graduates
        else:
            dataSizes[1] += 1

    ret = [dataSizes, labels]
    return ret

# returns all relevant information to construct pie chart
def undergradDist(data):
    labels = ['Freshmen', 'Sophomore', 'Junior', 'Senior', 'Unknown']
    dataSizes = [0,0,0,0,0]   #freshmen, sophomore, junior, senior, unknown
    valueList = list(data['dupsexpgradtermc1'])
    cond = list(data['dupsacadcareerdescc1'])

    for i in range(0, len(valueList)-1):
        if cond[i] != 'Undergraduate':
            continue

        # Check for NaN value and update the unknown size
        if valueList[i] != valueList[i]:
            dataSizes[4] += 1
            continue

        temp = valueList[i].split()[0]
        if temp == '2023':
            dataSizes[0] += 1
        elif temp == '2022':
            dataSizes[1] += 1
        elif temp == '2021':
            dataSizes[2] += 1
        elif temp == '2020':
            dataSizes[3] += 1

    ret = [dataSizes, labels]
    return ret


# returns all relevant information to construct pie chart
def graduateDist(data):
    valueList = list(data['dupsacadcareerdescc1'])
    valueSet = set(valueList)

    #Set up dictionary for different graduate school entries
    valueSet.discard('Undergraduate')
    dict1 = {}
    #initialize dict1
    for value in valueSet:
        if value != value:
            dict1['Unknown'] = 0
            continue
        dict1[value] = 0

    for value in valueList:
        if value == 'Undergraduate':
            continue
        if value != value:
            dict1['Unknown'] += 1
            continue
        dict1[value] += 1
    dataSizes = []
    labels = []
    for key, value in dict1.items():
        labels.append(key)
        dataSizes.append(value)

    ret = [dataSizes, labels]
    return ret


def drawPie(drawData, title, bigLegend):
    #Clean values with 0
    for i in range(0, len(drawData[0])):
        if drawData[0][i] == 0.0:
            del drawData[0][i]
            del drawData[1][i]

    labels = drawData[1]
    pie = plt.pie(drawData[0], autopct='%1.1f%%')
    plt.axis('equal')

    if (bigLegend):
        plt.legend(pie[0], labels, bbox_to_anchor=(1, 0.5), loc="center right", fontsize=10,
                   bbox_transform=plt.gcf().transFigure)
        plt.subplots_adjust(left=0.0, bottom=0.1, right=0.5)
        titleAdjust = plt.title(title)
        titleAdjust.set_ha("left")
    else:
        plt.legend(pie[0], labels, bbox_to_anchor=(0.85, 0.5), loc="center right", fontsize=10,
                   bbox_transform=plt.gcf().transFigure)
        plt.subplots_adjust(left=0.0, bottom=0.1, right=0.5)
        titleAdjust = plt.title(title)
        titleAdjust.set_ha("left")


    fileName = title + '.png'
    #plt.show()
    plt.savefig(fileName)
    plt.clf()


if __name__ == '__main__':
    data = reader()

    drawData = undergradGrad(data)
    title = "Undergraduate vs Graduate Attendance"
    drawPie(drawData, title, False)

    drawData = undergradDist(data)
    title = "Undergraduate Student Distribution"
    drawPie(drawData, title, False)

    drawData = graduateDist(data)
    title = "Graduate Student Distribution"
    drawPie(drawData, title, True)

