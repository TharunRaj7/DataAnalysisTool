import pandas as pd
from tkinter import filedialog
from tkinter import *
import os


fileName = ""
def reader():
    root = Tk()
    root.filename = filedialog.askopenfilename(initialdir="/", title="Select file",
                                               filetypes=(("CSV files", "*.csv"), ("all files", "*.*")))
    global fileName
    fileName = root.filename
    data = pd.read_csv(fileName, sep = ', ', engine = 'python', header = None, nrows = 7)
    headerIndex = 0
    for index, row in data.head(10).iterrows():
        rowList = list(row)
        #Find index to set the appropriate header
        if "First Name" in rowList[0]:
            headerIndex = index
            break

    data = pd.read_csv(fileName, header = headerIndex)
    df = pd.DataFrame(data)
    #print(data.head())
    email_list = df["Campus Email"].tolist()

    return email_list

def dataCleaner(email_list):
    netID_list = []
    for item in email_list:
        # skip NaN values
        if item != item:
            continue
        temp = item.split("@")
        netID_list.append(temp[0])
    return netID_list

def writer(netID_list, name):
    file_dir = os.path.dirname(os.path.abspath(__file__))
    name = "NetID" + name
    file_path = os.path.join(file_dir, name)
    df = pd.DataFrame(netID_list, columns = ["NetID"])
    df.to_csv(file_path, index = False, header=True)



if __name__ == '__main__':
    email_list = reader()
    netID_list = dataCleaner(email_list)
    writer(netID_list, fileName[-20:])


