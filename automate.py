import re
import database
import base64
import json

def extract_loan_information(message):
    loan_amount_pattern = re.compile(r'(?i)\b(?:loan[-\s]*amount|amount|loan)\b[-:\s]*([\d,.]+)')
    tenure_pattern = re.compile(r'(?i)\b(?:tenure|term)\b[-:\s]*([\d.]+)\s*(months|years|year)')
    name_pattern = re.compile(r'(?i)\b(?:name)\b[-:\s]*([A-Za-z\s]+)')
    email_pattern = re.compile(r'(?i)\b(?:email)\b[-:\s]*([a-zA-Z0-9._%+-]+@[-a-zA-Z0-9.-]+\.[a-zA-Z]{2,})')
    mobile_number_pattern = re.compile(r'(?i)\b(?:mobile[-\s]*number|phone[-\s]*number|mobile)\b[-:\s]*([\d\s-]+)')
    dob_pattern = re.compile(r'(?i)\b(?:dob|date[-\s]*of[-\s]*birth)\b[-:\s]*([\d]{4}[-/\s][\d]{1,2}[-/\s][\d]{1,2})')
    purpose_pattern = re.compile(r'(?i)\b(?:purpose)\b[-:\s]*([A-Za-z\s]+)')
    pan_pattern = re.compile(r'(?i)\b(?:pan)\b[-:\s]*([A-Z]{5}[-\d]{4}[A-Z]{1})')
    aadhar_pattern = re.compile(r'(?i)\b(?:aadhar)\b[-:\s]*([\d\s-]+)')

    loan_amount_match = loan_amount_pattern.search(message)
    tenure_match = tenure_pattern.search(message)
    name_match = name_pattern.search(message)
    email_pattern = email_pattern.search(message)
    mobile_number_pattern = mobile_number_pattern.search(message)
    dob_pattern = dob_pattern.search(message)
    purpose_pattern = purpose_pattern.search(message)
    pan_pattern = pan_pattern.search(message)
    aadhar_pattern = aadhar_pattern.search(message)


    my_list = {}

    my_list['loan_amount'] = loan_amount_match.group(1) if loan_amount_match else None
    my_list['tenure_value'] = tenure_match.group(1) if tenure_match else None
    my_list['tenure_unit'] = tenure_match.group(2) if tenure_match else None
    my_list['name'] = name_match.group(1) if name_match else None
    my_list['email'] = email_pattern.group(1) if email_pattern else None
    my_list['mobile'] = mobile_number_pattern.group(1) if mobile_number_pattern else None
    my_list['dob'] = dob_pattern.group(1) if dob_pattern else None
    my_list['purpose'] = purpose_pattern.group(1) if purpose_pattern else None
    my_list['pan'] = pan_pattern.group(1) if pan_pattern else None
    my_list['aadhar'] = aadhar_pattern.group(1) if aadhar_pattern else None

    # name = name_match.group(1) if name_match else None

    print(my_list)

    return my_list

def createApplication(msg,isWhatsappCall):
    my_list = {}
    if isWhatsappCall == "1" :
        my_list = msg         
    else :
        my_list = extract_loan_information(msg)
    return database.createLoanApplication(my_list,isWhatsappCall)


def updateApplication(msg,id,isWhatsappCall):
    my_list = {}
    if isWhatsappCall == "1" :
        my_list = msg
    else :
        my_list = extract_loan_information(msg)    
    return database.updateLoanApplication(my_list,id,isWhatsappCall)

def updateDocument(msg,id,isWhatsappCall):
    my_list = {}
    base64_value = ""
    doc_name = ""
    doc_content = ""

    if isWhatsappCall == "1" :
        doc_name = msg.get('doc_type')
        base64_value = msg["image"][0]["base64"]

    else :
        pattern = re.compile(r'^(.*?)\s*=\s*(.*)$')

        match = re.search(pattern, msg)

        if match:
            doc_name = match.group(1).strip()
            base64_value = match.group(2).strip()
            
            # print(f'{"content"}: {doc_content}')
    if base64_value != "" and doc_name != "":      
    # Decode the base64-encoded value
        doc_content = base64.b64decode(base64_value)

        # Determine the file format
        file_format = get_file_format(doc_content)
        
        my_list['doc_name'] = doc_name
        my_list['doc_content'] = base64_value
        my_list['doc_format'] = file_format

    return database.updateDocument(my_list,id,isWhatsappCall)

def get_file_format(decoded_content):

    file_signatures = {
        b'\xff\xd8\xff\xe0': 'JPEG',
        b'\x89PNG\r\n\x1a\n': 'PNG' ,
        b'%PDF-': 'PDF',
        # Add more signatures as needed
    }

    for signature, file_format in file_signatures.items():
        if decoded_content.startswith(signature):
            return file_format


    return  {
                'status' : 'FAIL',
                'message' : 'Invalid Format',
                'id':0
            }


def getDigioDetails(id,isWhatsappCall):
    return database.getDigioDetails(id,isWhatsappCall)


