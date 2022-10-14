# Load libraries 
import os
import pandas as pd
from zipfile import ZipFile
import shutil
import configparser
import errno
import yaml

def get_yml_item_value(file, item_input):
    # Function that opens the yaml file and returns the value that the item has

    # transform the argument values into lowcase or uppercase
    file = file.lower()
    item_input = item_input.upper()

    with open(file, 'r') as file:

        configuration = yaml.full_load(file)

        for item, value in configuration.items():

            if item == item_input:
                value_output = value

                return value_output


def csv_file_to_df(file, item_input):
    # Function that reads a csv file using config file that it name and path location is declared in a YAML config file.

    # get the path of the template folder from the YAML config file
    values_template_imput = get_yml_item_value(file, item_input).values()

    if any(s.startswith('./') and s.endswith('/') for s in values_template_imput):

        if any(s.endswith('.csv') for s in values_template_imput):

            for value in values_template_imput:

                if os.path.isdir(value):

                    folder_path = value

                else:

                    file_name = value

            name_file_read = folder_path + file_name

            # read the base template
            base_template = pd.read_csv(name_file_read)

            # transform column names into lowcase to make them case insensitive
            base_template.columns = base_template.columns.str.lower()

            return base_template

        else:
            print('ERROR! = File name does not have .CSV extension!')

    else:

        print('ERROR! = Path should be like: ./input/')


def lai_txt_to_df(config_file_name, item_VARIABLES_EXTRACT_FROM_TXT_FILE, item_NAME_ZIP_FILES, ZIP_file_name):
    # Function that extract the variables from the LAI txt files and stores them into a data frame

    ## ~~ 1. List of variables to extract from LAI TXT files
    # get the list of variables to extract from the txt files
    listOfvariables = get_yml_item_value(config_file_name, item_VARIABLES_EXTRACT_FROM_TXT_FILE)
    listOfvariables = [s.upper().replace(' ', '') for s in listOfvariables]
    # in case any alement in the list is lowercase it will transformed into uppercase

    # add DATE and TIME to the list of variables if they are not in the list
    if 'DATE' not in listOfvariables:
        listOfvariables.insert(2, 'DATE')

    if 'TIME' not in listOfvariables:
        listOfvariables.insert(3, 'TIME')

    ## ~~ 2. Zip file

    # Extract all the contents of zip file in current directory
    with ZipFile('./input/' + ZIP_file_name + '.zip', 'r') as zipObj:

        zipObj.extractall()

    ## get the list of files to process
    path = './' + ZIP_file_name + '/'

    # read the list of txt files
    files = os.listdir(path)

    # create the dataframe
    dataFrame = pd.DataFrame(columns=listOfvariables)

    numberRows = 0

    # read each file in the directoryc
    for file in files:

        # open each file
        tempDataFrame = pd.DataFrame()

        with open(path + file, 'r') as reader:

            lines = reader.readlines()

            numberColumn = 0

            # read each line of the file
            for line in lines[0:len(lines) - 1]:

                line_list = line.split()

                # avoid empty lines
                if len(line_list) >= 1:

                    # select lines that are in the list of variables
                    if line_list[0] in listOfvariables:

                        # if the variable does not have a value store empty
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

        # concatenate the new rows to the dataframe
        dataFrame = pd.concat([dataFrame, tempDataFrame], axis=0, ignore_index=True)[dataFrame.columns.tolist()]

        numberRows += 1

    shutil.rmtree(ZIP_file_name)

    # sort the data frame rows by time values
    dataFrame.sort_values(by=['TIME'])

    return dataFrame

def save_dataFrame_to_csv(dataFrame, ZIP_file_name):
# create the folder where the output file will be stored
        try:
            os.makedirs('output')

        except OSError as e:

            if e.errno != errno.EEXIST:

                raise

        # create and save the file
        dataFrame.to_csv('./output/' + ZIP_file_name + '.csv', index=False)

        print('Dataframe ' + './output/' + ZIP_file_name + '.csv' + ' created successfully!')

def matching_elements_two_lists(first_list, second_list):
# Function that compares two lists and returns the elements that exist in both of them

    # compare the template colums vs subset columns from config file and return NOT matches
    not_matching_elements = list(set(first_list).difference(second_list))

    if len(not_matching_elements) > 0:

        print('ATTENTION! The following columns do not exist in the data frame:', not_matching_elements)

    # Remove 'columns' form the list that does no exist in the template
    return [element for element in first_list if element not in not_matching_elements]


def txtLAI_to_csvFile(config_file_name, item_NAME_ZIP_FILES, item_VARIABLES_EXTRACT_FROM_TXT_FILE):
    ##Function that extract the LAI values from txt files creates a data frame and export the
    ##created data frame into a CSV file

    ZIP_files_list = get_yml_item_value(config_file_name, item_NAME_ZIP_FILES)

    ## run the function for each ZIP file listed in the YAML file
    for ZIP_file_name in ZIP_files_list:
        dataFrame = lai_txt_to_df(config_file_name, item_VARIABLES_EXTRACT_FROM_TXT_FILE, item_NAME_ZIP_FILES,
                                  ZIP_file_name)

        save_dataFrame_to_csv(dataFrame, ZIP_file_name)


def information_from_file_name_column(config_file_name, item_NAME_ZIP_FILES, item_VARIABLES_EXTRACT_FROM_TXT_FILE,
                                      file_template, item_TEMPLATE_INPUT, item_COLUM_WITH_NAME, item_FILE_NAME,
                                      item_COMPLEMENTARY_INFO, item_SAMPLE_IDENTIFIER):
    # get the name of name_ZIP_file
    ZIP_files_list = get_yml_item_value(config_file_name, item_NAME_ZIP_FILES)

    ## run the function for each ZIP file listed in the YAML file
    for ZIP_file_name in ZIP_files_list:

        dataFrame = lai_txt_to_df(config_file_name, item_VARIABLES_EXTRACT_FROM_TXT_FILE, item_NAME_ZIP_FILES,
                                  ZIP_file_name)

        # save_dataFrame_to_csv(dataFrame)

        # get template using the function csv_file_to_df() file
        baseTemplate = csv_file_to_df(file_template, item_TEMPLATE_INPUT)

        # get the name of the column that contains the information code
        colum_with_name = get_yml_item_value(file_template, item_COLUM_WITH_NAME)

        # get the iformation to extract the name of new columns
        items_file_name = get_yml_item_value(file_template, item_FILE_NAME)
        items_file_name

        ## add the new columns and rows to the template dataframe
        numberColumn = 0
        for key_column in items_file_name:
            # get the value of the position form the template.yml file
            list_positions = items_file_name.get(key_column)

            # extract the part of the string from the column whit the file name
            column = dataFrame['LAI_FILE'].str[list_positions[0] - 1: list_positions[0] + list_positions[1] - 1]

            column = column.apply(pd.to_numeric, errors='coerce', downcast='integer').fillna(column)

            # insert the part of the string extracted from the 'LAI_FILE' column
            dataFrame.insert(numberColumn, key_column.lower(), column, True)

            # reemplace the values of each item by key in the column
            dataFrame.replace({key_column.lower(): get_yml_item_value(file_template, key_column.upper())}, inplace=True)

            numberColumn += 1

            ## get the complementary infor to add as column
        items_complementary_info = get_yml_item_value(file_template, item_COMPLEMENTARY_INFO)

        # create a new colum for each key of complementary information in the template.yml file
        for key_column in items_complementary_info:
            key_column_value = items_complementary_info.get(key_column)

            # insert the part of the string extracted from the 'LAI_FILE' column
            dataFrame.insert(numberColumn, key_column.lower(), key_column_value, True)

            numberColumn += 1

            ## Add column sample_id:
        # get the column names from the config file and make them lower case to create the id sample
        list_columns_id = [x.lower() for x in
                           [value for value in get_yml_item_value(file_template, item_SAMPLE_IDENTIFIER).values()][0]]

        first_list = list_columns_id

        # names of columns from the database into a list
        second_list = dataFrame.columns.tolist()

        # review if the columns to create the id exist in the data frame
        list_columns_id_select = matching_elements_two_lists(first_list, second_list)

        # get the name of the new column to create from the config file
        name_column_id = [value for value in get_yml_item_value(file_template, item_SAMPLE_IDENTIFIER).keys()][
            0].lower()

        # create the new column as id identifier for the sample and insert the id values
        ##base_template_subset_rep[name_column_id] = base_template_subset_rep[list_columns_id_select].astype(str).add('_').sum(axis = 1)
        dataFrame[name_column_id] = dataFrame[list_columns_id_select].astype(str).agg(
            '_'.join, axis=1)

        # move the'id_plot' column to the fist position of the data frame
        col = dataFrame.pop(name_column_id)
        dataFrame.insert(0, col.name, col)

        save_dataFrame_to_csv(dataFrame, ZIP_file_name)