# Load libraries 
import os
import pandas as pd
from zipfile import ZipFile
import shutil

# Run functions

def lai_df(name_ZIP_file, listOfvariables):
    # Extract all the contents of zip file in current directory
    with ZipFile('./' + name_ZIP_file + '.zip', 'r') as zipObj:

       zipObj.extractall()

    ## get the list of files to process
    path = './' + name_ZIP_file + '/'

    # read the list of txt files
    files = os.listdir(path)

    # create the dataframe
    dataFrame = pd.DataFrame(columns = listOfvariables)

    numberRows = 0

    # read each file in the directoryc
    for file in files:

        # open each file
        tempDataFrame = pd.DataFrame()

        with open(path + file, 'r') as reader:

            lines = reader.readlines()

            numberColumn = 0

            # read each line of the file
            for line in lines[0:len(lines)-1]:

                line_list = line.split()

                # avoid empty lines
                if len(line_list) >= 1:

                    # select lines that are in the list of variables            
                    if line_list[0] in listOfvariables :                

                        # if the variable does not hava a value store empty
                        if len(line_list) == 1:

                            tempDataFrame.insert(numberColumn, line_list[0], '', True)
                            numberColumn += 1

                        # if the variable is date, also store the date 
                        elif len(line_list) == 3 and line_list[0] == 'DATE':  

                            tempDataFrame.insert(numberColumn, line_list[0], [line_list[1]], True)
                            numberColumn += 1

                            tempDataFrame.insert(numberColumn, 'TIME', [line_list[2]], True)
                            numberColumn += 1

                        else:

                            tempDataFrame.insert(numberColumn, line_list[0], [line_list[1]], True)

                            numberColumn += 1         

        #if numberRows == 0:

            #dataFrame = tempDataFrame

        #else:

            #[dataFrame.columns.tolist()] is used to keep the column order unchanged
        dataFrame = pd.concat([dataFrame, tempDataFrame], axis=0, ignore_index=True)[dataFrame.columns.tolist()]

        numberRows += 1 

    shutil.rmtree(name_ZIP_file)

    dataFrame.sort_values(by=['TIME'])

    dataFrame.to_csv(name_ZIP_file + '.csv', index=False)
    
    return print('Dataframe created successfully!')