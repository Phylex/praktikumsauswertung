import numpy as np
import pandas as pd


file_path="/home/davids/Dokumente/Uni/Praktikum/Versuche/Testversuch/"


#system functions

#function for reading in exesting experiments and returns a datalist with all the existing experiments
def programmstart():
  datalist=list()                                   #creating list for holding all the dataframes
  count_of_experiments=0                            #variable to track the number of dataframes/experiments
  while True:
    try:                                            #trying to read dataframe 
      data=pd.read_csv(str(file_path)+str(count_of_experiments+1)+".csv",index_col=False)
      print "           "+str(count_of_experiments+1)+" experiment:"
      print data
      datalist.append(data)
      count_of_experiments+=1
    except IOError:                                 # if failing to read break the loop and returns the datalist
      break
  
  print
  print str(count_of_experiments)+" experiments found"
  return datalist

#function that saves an list of the dataframes to seperate csv files
def update_csv(datalist):
  loopcounter=0
  while True:
    try:
      datalist[loopcounter].to_csv(str(file_path)+str(loopcounter+1)+".csv",index=False)  #tries to save one dataframe of the datalist as csv
      loopcounter+=1
    except IndexError:
      break


#assist functions

#function to convert the int dtype array in a string list for the csv file
def value_to_datatype(dtypelist):
  loopcounter=0
  
  #main loop for checking each index and converting it into the correct string
  while True:
    try:
      data=dtypelist[loopcounter]       
      if data==1:
        dtypelist[loopcounter]="float"      #if 1 replace with float
      else:
        dtypelist[loopcounter]="string"     #if 2 replace with string
    except IndexError:
      break                                 #breaks if index error, means the list was completly parsed
    loopcounter+=1
  return dtypelist                          #returns the same shaped list with strings

#function to create a headline for the dataframe of the experiments, returns 2 list, one with the names of the columns, one with the datatype
def headline_creation():
  headline=list()                                   #creating list for the columns names
  dtype=list()                                      #creating list for the colums datatypes
  loopcounter2=0                                       #variable for coutning the outer loop cycle
  bre=0
  
  print "Type column name and press enter, to continue type <continue> and press enter"
  #main loop for headline and dtype creation
  while True:
    
    #loop creating a column headline
    while True:
      line=str(raw_input(str(loopcounter2+1)+". column name: "))#raw input to name the column
      if line=="continue":                                      #checks if user wants to proceed to enter values
        if loopcounter2 == 0:                                   #checks if user actually created a column
          print "no columns created"
        else:                                                   #if yes breaks all loops
          bre=1
          break
      else:
        headline.append(line)                                   #appends column name to the headline list
        break
    if bre==1:
      break
    loopcounter=0                                               #creating variable for inner loop cycle
    
    #loop creating the dtype for a column
    while True:                                       
      if loopcounter > 0:                                       #if loop was cyled already ones it means user did something wrong
        print "type <1> or <2>"
      loopcounter+=1
      try:
        dtype_part=int(raw_input(str(loopcounter2+1)+". column data type(<1> for float, <2> for string): "))#expecting value 1 or 2
      except ValueError:                                                                                    #if value error he doesnt try to assign dtype a value
        pass
      try:
        if (dtype_part>0 and dtype_part<3):                                                                 #checks if value is 1 or 2 and tries to append it
          dtype.append(dtype_part)
      except ValueError:                                                                                    #if no dtype value exist pass
        pass  
      try:
        if (dtype[loopcounter2] >0 and dtype[loopcounter2]<3):                                              #if dtype value is actually existing between 1 and 2 it breaks the loop
          break
      except IndexError:                                                                                    #if the dtype list is empty it will result in a index error
        pass
    loopcounter2+=1
   
  
  return headline, value_to_datatype(dtype)                                                                 #retuns headline and the dtype list, dtype list was converter in string with the value_to_datatype function befor    


#function called by user

#function to put in new values for one of the new experiments(number)
def input_experiment(datalist):
  #loop to input the number of the experiment
  while True:
    try:
      number=int(raw_input("which experiment you want to start/continue?: "))
      if number > 0:
        break
      else:
        print "type an positiv integer number"
    except ValueError:
      print "type an integer number"
    
  #figuring out if the first experiment already exist
  try:
    data=pd.read_csv(str(file_path)+"1.csv")       #tries to read the first experiment
    if data.empty:                                 #checks if it is empty
      empty_condition=True
    else:
      empty_condition=False
  except IOError:                                  #if the first experiement doesnt exist it will result in an IOError
    empty_condition=True
  
  #creating headline and datatype
  if number == 1 and empty_condition:   #if first experient does not exist goes to headline creation
    print "No headlines for this experiment found."
    headline,datatype=headline_creation()
  else:                                            #else takes headline of first experiment as headline for other experiments
    headline=datalist[0].columns
    datatype=data.ix[0]
  
  #checking if the eperiment(number) already exists and if not it will create the columns and dtype
  try:
    data=pd.read_csv(str(file_path)+str(number)+".csv")
  except IOError:                                       #IOError when file does not exist already, if yes it will write headline and dtype to a new file
    datatypelist=list()
    datatypelist.append(datatype)
    data = pd.DataFrame(datatypelist,columns=headline)
    if number-1!=len(datalist):                         #checks if the number is actually the smallest number of experiment not existing, if not it will choose the smallest one
      print "experient "+str(len(datalist)+1)+" - "+str(number)+" do not exist, programm choses continues indexing"
      number=len(datalist)+1
    print "experient " + str(number) + " created"
  
  
  total=list()                                  #a list containing the a total line, resets every loop cycle
  number_of_columns= data.shape[1]              #checks the number of columbs of the data frame
  number_of_line=data.shape[0]                  #checks the number of lines of the data frame
  if number_of_line > 1:
    print "experient restored at line " + str(number_of_line)
  
  #main loop to input data in the data frame
  while True:
    linedata=np.zeros(number_of_columns,dtype=object)#creating empty array for the data of a line
    bre=0                                            #break variable, if 1 it will break all the loops
    
    #loop for the creation of a data line
    for a in range(number_of_columns):
      
      #loop for a single data value
      while True:
        linedatapart=raw_input(str(headline[a])+", line("+str(number_of_line)+(") = "))
        if str(linedatapart)=="exit": # checks if the line is the line to break the loop
          bre=1 #variable that indicates to break the outer loop
          break
        try: 
          float(linedatapart)                           #checks if data is the right datatype
          if str(data.iat[0,a])=="float":
            break
        except ValueError:
          if str(data.iat[0,a])=="string":
            break
          else:
            print "float value in this column expected"
        
      if bre==1:                                       #checks if the input was "exit" to break the loop 
        break
      else:
        linedata[a]=linedatapart                       #else the input will be transfered to data

    number_of_line+=1
    if bre == 1:                                       #checks if the main loop needs to stop
      break
    #appends list with next dataline
    total.append(linedata)                             #transfering the linedata array to a list, needed to be put in the dataframe
    data2=pd.DataFrame(total, columns=headline)        #creating second dataframe with the linedata
   
    #updates dataframe and export to csv
    data = data.append(data2,ignore_index=True)        #appends the second dataframe to the main one
    data.to_csv(str(file_path)+str(number)+".csv",index=False)#saves to csv file
    del total[:]                                       #deletes the line data to create a new set of line data in next loop clyce

#function that replaces a column headline in every csv file     
def headline_replace(datalist):
  headline=datalist[0].columns                      #reads old headline
  headlinearray=np.asarray(headline)                #creates an array for the new headline
  datatype=datalist[0].ix[0]                        #reads datatypes
  number_of_columns=datalist[0].shape[1]            #number of columbs
  for columns in range(number_of_columns):          
    print (columns+1), datalist[0].columns[columns], datalist[0].iat[0,columns]#displays existing column names and dtypes
  #loop for the replace column index input
  while True:
    try:
      replace_column=int(raw_input("which column tag you want to replace?: "))  #user enters column tag to replace
      if (replace_column > 0) and (replace_column < (number_of_columns+1)):     #checks if the coloumn exists
        break
      else:
        print "expects value between 1 and " +str(number_of_columns)      #if column doesnt exist doesnt break loop
    except ValueError:
      print "expects value between 1 and " +str(number_of_columns)        #if column index is not a integer doesnt break loop
  
  headlinearray[replace_column-1]=raw_input("new headline name: ")        #overwrite ccolumn tag
  headline_new=list()
  headline_new.append(headlinearray)
  loopcounter=0
  #loop for replacing the new headline in every data frame
  while True:
    try:
      datalist[loopcounter].columns=headline_new
      loopcounter+=1
    except IndexError:
      break
  update_csv(datalist)                  #updates csv file
  
    
  

#def continue_experiment():
function_list={1:input_experiment,2:headline_replace,3:programmstart}


#main loop
while True:
  datalist=function_list[3]()
  print "options: 1:input_experiment, 2:headline_replace"
  while True:
    try:
      programmselect=int(raw_input("Choose Option: "))
      if programmselect>0 and programmselect<3:
        break
      else:
        print "type value between 1 and 2"
    except ValueError:
      print "type value between 1 and 2"
  function_list[programmselect](datalist)

  





