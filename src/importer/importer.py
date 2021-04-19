import pandas
from contacts.models import Contact
def extractHeaders(contacts):
    headers=[]
    for contact in contacts:
        for key in contact['contact_info']:
            if key not in headers:
                headers.append(key)
    return headers
    
def fromDictToContact(input_dict):
    return Contact(**input_dict)

def prepareAndAppend(input_dict, input_item):
    prepared_dict = removeState(input_item)
    appendItem(input_dict, prepared_dict)

def fromContactToDict(input_item):
    return input_item.__dict__

def appendItem(input_dict, prepared_dict):
    input_dict.append(prepared_dict)

def removeId(input_dict):
    del input_dict["id"]
    return input_dict

def removeState(input_dict):
    del input_dict["_state"]
    return input_dict


def getContactsFromFile(f, header_sample):
    return parseContactsFromFile(f, header_sample).to_dict('records')


def findEmail(contact_info, key_mail):
    email = contact_info[key_mail]
    if not email or not "@" in email:
        email = findFirstEmail(contact_info)
    return email

def findFirstEmail(contact_info):
    email = [val for key, val in contact_info.items() if isinstance(val, str) and '@' in val][0]
    return email
def parseContactsFromFile(input, header_sample):
    print("input",filetype.guess(input))
    try:
        input_list = pandas.read_html(input)
        print("input_list",input_list)
    except:
        input_list=pandas.read_excel(input)
        print("input_list",input_list)
    return getParsedData(input_list, header_sample)


def selectDataframe(input_list, header_sample):
    try:
        dataframe = findDataframe(input_list, header_sample)
    except:
        dataframe = input_list
    return parseDataframe(dataframe,header_sample)

def getParsedData(input_list, header_sample):
    try:
        dataframe = findDataframe(input_list, header_sample)
    except:
        dataframe = input_list
    return parseDataframe(dataframe,header_sample)
        
def findDataframe(input_list, header_sample):
    for i in range(len(input_list)):
        df=input_list[i]
        if isHeaderInDataframe(df, header_sample):
            return df
    raise Exception("Sorry, header sample \""+header_sample+"\" not found in list")
    
def isHeaderInDataframe(df, header_sample):
    return df.isin([header_sample]).any().any()

def parseDataframe(df,header_sample):
    index = getIndexOfHeader(df, header_sample)
    result = splitDataframe(df, index)
    return replaceNaNforNull(result)

def splitDataframe(df, index):
    return pandas.DataFrame(df.values[index+1:], columns=df.values[index])


def replaceNaNforNull(df):
    return df.where(df.notna(), None)

def getIndexOfHeader(df, header_sample):
    header_column = headerColumn(df,header_sample)
    return extractIndex(header_column)

def extractIndex(booleanArray):
     return [i for i, x in enumerate(booleanArray) if x][0]

def headerColumn(df, header_sample):
    for i in df:
        if df[i].isin([header_sample]).any():
            return df[i].isin([header_sample]).array
        if header_sample == i:
            return df[i]
    raise Exception("Header \""+header_sample+"\" Not Found in dataframe")


class Importer(object):
    def __init__():
        pass

