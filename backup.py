from fileinput import filename
import re

#The file that has all the input value
#Has 2D shape, dataList[0][0] = csc 0000
dataList = []

#Read File from user input file, 
def readFile(fileName):
    try:
        data = open(fileName, 'r')
    except OSError:
        print("could not open/read the file: ", fileName)    
    
    with data:    
        line = data.readline()

        line_Numb = 0
        index=[]
        tmp=''
        inBracket = False   
        
        while(line):
            dataList.append([])
            
            #save the data wihtout '[', ']', '\n', and ','(except ',' inside of [])
            for i in line:
                if i=='[':
                    inBracket=True 
                if i==',' and inBracket==False:
                    if tmp != '':
                        index.append(tmp)
                        tmp=''                  
                if i==']':
                    index.append(tmp)
                    inBracket=False 
                    tmp=''        
                if i!=',' and inBracket==False:
                    if i!='\n' and i!=']':
                        tmp=tmp+i                
                if inBracket==True:
                    if i!='[' and i!=']':
                        tmp=tmp+i          

            for i in range(len(index)):
                dataList[line_Numb].append(index[i])
            index.clear()
            line = data.readline()
            line_Numb += 1  
    
        #print data [i][j] timess
        for i in range (len(dataList)):
            for j in range(len(dataList[i])):
                print (dataList[i][j])   

fName=input("Please type the file name: ")
readFile(fName)
