import pandas
from contacts.models import Contact

def extract_headers(contacts: list[dict[str, any]]) -> list[str]:
    """
    Extracts the unique headers from a list of contacts.

    Args:
        contacts: A list of dictionaries representing contacts.

    Returns:
        A list of unique headers from the contact dictionaries.
    """
    headers = {key for contact in contacts for key in contact['contact_info']}
    return list(headers)
    
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

## Parsing file functions
def getContactsFromFile(f, header_sample):
    return parseContactsFromFile(f, header_sample).to_dict('records') #Convert to dict


def findEmail(contact_info, key_mail):
    email = contact_info[key_mail]
    if not email or not "@" in email:
        email = findFirstEmail(contact_info)
    return email

def findFirstEmail(contact_info):
    email = [val for key, val in contact_info.items() if isinstance(val, str) and '@' in val][0]
    return email
def parseContactsFromFile(input_file, header_sample):
    try:
        input_list = pandas.read_html(input_file)
        file = HtmlFile(input_list,header_sample)
    except:
        input_list=pandas.read_excel(input_file, header=None, sheet_name=None, dtype=str) 
        print("INPUT", input_list)
        file = ExcelFile(input_list,header_sample)
    finally: 
        return file.parseSheet()

class File(object):
    sheets = []
    sheet = []
    def __init__():
        pass
    
    def selectSheet(self, header):
        sheets=self.sheets
        
        def containsElementInElement(df,e):
            return df.isin([e]).any().any()

        def findSheet():
            for i in range(self.n_sheets):
                sheet=sheets[i]
                if containsElementInElement(sheet, header):
                    return sheet
            raise Exception("Sorry, header sample \""+header+"\" not found in list")
            
        sheet = findSheet()
        return sheet
    def parseSheet(self):
        print("PARSING SHEET")
        header = self.header
        sheet = self.sheet
        
        def containsElement(df,e):
            return df.isin([e]).any()

        def splitDataframe(df, index):
            return pandas.DataFrame(df.values[index+1:], columns=df.values[index])
            
        def replaceNaNforNull(df):
            return df.where(df.notna(), None)

        def header_check(df, h):
            for i in df:
                if containsElement(df[i],h):
                    return df[i].isin([h]).array
                if header == i:
                    return df[i]
            raise Exception("Header \""+h+"\" Not Found in dataframe")

        def extract_index(booleanArray):
            return [i for i, x in enumerate(booleanArray) if x][0]

        header_check_list = header_check(sheet, header)
        index = extract_index(header_check_list)
        result = replaceNaNforNull(splitDataframe(sheet, index))
        return result

class HtmlFile(File):
    
    def __init__(self, input_list, header):
        self.sheets = input_list
        self.n_sheets=len(self.sheets)
        self.header = header
        self.sheet = self.selectSheet(header)



class ExcelFile(File):
    
    def __init__(self, input_list, header):
        self.sheets = input_list
        self.sheet = self.selectSheet(header)
        self.n_sheets=len(self.sheets)
        self.header = header
        
    def selectSheet(self, header):
        sheets=self.sheets
        
        def containsElementInElement(df,e):
            return df.isin([e]).any().any()

        def findSheet():
            for i in sheets:
                if containsElementInElement(sheets[i], header):
                    return sheets[i]
            raise Exception("Sorry, header sample \""+header+"\" not found in list")
            
        sheet = findSheet()
        return sheet