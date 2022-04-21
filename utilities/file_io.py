from csv import reader, writer

"""General-purpose functions.

This module provides general file reading or writing functions that can
be used by any part of the program. 

"""

def str_to_nb(number: str):
    """Exception-safe casting function. (Therrien Jun/21/2019)

    This function converts an str object to a float or an int, or
    returns an str object if no conversion is possible.

    Args:
        number (str): The str character to cast to int or float

    Returns:
        float or int if convertible, str if not.

    """

    try:
        if "." in number:
            return float(number)
        return int(number)
    except ValueError:
        return number

def read_csv_index_table(file_name: str, separator: str=';') -> dict:
    """csv index file reader. (Therrien Jun/21/2019)

    This function reads csv tables formated from the 3GPP releases that
    assign an index to a number. It is used to read backoff indicators,
    MCS to TBS tables, etc. The first element of the csv table will be
    used as the dictionary's key while the other(s) element(s) of the 
    row will become that key's corresponding value (a single variable 
    if there is one value, or a list of values if there is more than 
    one element).

    Args:
        file_name (str): The path and name of the csv file to read.
        separator (str): The character used in the csv file to
            delimitate values (normally ';').

    Returns:
        dict: 
            The formatted csv table.

    Raises:
        FileNotFoundError: The function could not find and/or open
            file_name.

    """
    table = {}
    try:
        with open(file_name, newline='') as csvfile:
            file_reader = reader(csvfile, delimiter=separator)
            for row in file_reader:
                if len(row) == 2: #assign a single value
                    index, value = row
                    index = str_to_nb(index)
                    value = str_to_nb(value)
                    table[index] = value
                else: #assign a list of values if more than 1 element
                    key = str_to_nb(row[0])
                    table[key] = []
                    for element in row[1:]: #[1:] to skip the first column
                        table[key].append(str_to_nb(element))
    except FileNotFoundError as error:
        print("\n" + type(error).__name__ + ": The file '" + file_name 
              + "' was not found during the execution of the function " 
              + "'read_csv_index_table' in module utilities.file_io.py. "
              + " Please ensure that the file path refers to a valid "
              + "file. Exiting the program...")
        raise FileNotFoundError
           
    return table