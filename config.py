from dotenv import dotenv_values
# from pathlib import Path
# from dotenv import load_dotenv

env = dotenv_values(".env")

php_path = 'static/php/'

# database
DBHOSTNAME = env['DBHOSTNAME']
DBUSERNAME = env['DBUSERNAME']
DBPASSWORD = env['DBPASSWORD']
DBNAME = env['DBNAME']
CLIENT_ID = env['X-Client-ID']
CLIENT_SECRET = env['X-Client-Secret']
SECRET_KEY = env['SECRET_KEY']
BASIC_AUTH_ROUTES = ['/get-response']
LOG_HANDLER = 'cloudwatch'
# LOG_HANDLER = env['LOG_HANDLER']
CLOUDWATCH_GROUP = env['CLOUDWATCH_GROUP']
CLOUDWATCH_STREAM = env['CLOUDWATCH_STREAM']
CLOUDWATCH_ACCESS_KEY = env['CLOUDWATCH_ACCESS_KEY']
CLOUDWATCH_SECRET_KEY = env['CLOUDWATCH_SECRET_KEY']
AWS_REGION_NAME = env['AWS_REGION_NAME']
AWS_ACCESS_KEY_ID = env['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = env['AWS_SECRET_ACCESS_KEY']
AWS_BUCKET = env['AWS_BUCKET']


# Formats


DOC_PATH = {
    'PAN': 'pan_card',
    'SECURITY_CHEQUE': 'security_cheques',
    'APPLICANT_PHOTO': 'customer_photo',
    'APPLICANT_AADHAAR_FRONT': 'aadhar_card',
    'APPLICANT_AADHAAR_BACK': 'aadhar_card_back',
    'ELECTRICITY_BILL': 'electricity_bill',
    'GAS_BILL': 'gas_bill',
    'PASSPORT': 'passport',
    'BANK_STATEMENT': 'bank_statement',
    'BANK_STATEMENT_2': 'bank_statement_2',
    'BANK_STATEMENT_3': 'bank_statement_3',
    'BANK_STATEMENT_4': 'bank_statement_4',
    'BANK_STATEMENT_5': 'bank_statement_5',
    'BANK_STATEMENT_6': 'bank_statement_6',
    'SALARY_SLIP': 'salary_slip',
    'ITR': 'itr',
    'MCA': 'mca',
    'UTILITY_BILL_VALIDATION': 'utilitybillvalidation',
    'CPV': 'cpv',
    'RENT_AGREEMENT': 'rent_agreement',
    'SALE_DEED': 'sale_deed',
    'SHOP_ACT': 'shop_act',
    'GST_CERTIFICATE': 'gst_certificate',
    'CO_APPLICANT_BANK_STATEMENT': 'co_applicant_bank_statement',
    'CO_APPLICANT_PAN': 'co_applicant_pan_card',
    'CO_APPLICANT_AADHAAR_FRONT': 'co_applicant_aadhar_card',
    'CO_APPLICANT_AADHAAR_BACK': 'co_applicant_aadhar_card_back',
    'CO_APPLICANT_PHOTO': 'co_applicant_customer_photo',
    'PASSBOOK': 'passbook_copy',
    'OTH': 'other',
    'PASSPORT_FRONT': 'passport_front',
    'PASSPORT_BACK': 'passport_back',
    'DRIVING_LICENSE': 'driving_license',
    'VOTAR_ID_FRONT': 'votar_id_front',
    'VOTAR_ID_BACK': 'votar_id_back',
    'SELFIE': 'selfie',
    'LOAN_AGREEMENT_ESIGN': 'loan_agreement_esign',
    'AADHAR_CARD': 'aadhar_card',
    'AADHAR_ZIP': 'aadhar_zip',
    'AADHAR_XML': 'aadhar_xml',
    'EPF_REPORT_KARZA': 'epf report karza',
    'EPF_REPORT': 'epf report',
}

DOC_NAMES = {
    'File Aadhar Card': 'file_aadhaar_card', 
    'File Aadhar Card Back': 'file_aadhaar_card_back', 
    'File Pan Card': 'file_pan_card', 
    'Aadhar Card': 'aadhar_card', 
    'Aadhar Card Back': 'aadhar_card_back', 
    'Advance Amount Receipt': 'advance_amount_receipt', 
    'Agreement': 'agreement', 
    'Applicant Customer Photo': 'customer_photo', 
    'Bank Statement 1': 'bank_statement', 
    'Bank Statement 2': 'bank_statement_2', 
    'Bank Statement 3': 'bank_statement_3', 
    'Bank Statement 6': 'bank_statement_6', 
    'BUREAU Report': 'equifax_report', 
    'Call Recording': 'call_recording', 
    'CPV': 'cpv', 
    'Credit Appraisal Memo': 'credit_appraisal_memo', 
    'Gas Bill': '1', 
    'Electricity Bill': '1', 
    'Finbit Analysis': 'finbit_analysis', 
    'FOIR': 'foir', 
    'GST Certificate': 'gst_certificate', 
    'Insurance Payment Receipt': 'insurance_payment_receipt', 
    'ITR': 'itr', 
    'MCA': 'mca', 
    'Nach': 'nach', 
    'Pan Card': 'pan_card', 
    'Pan Validation': 'panvalidation', 
    'Passbook Copy': 'passbook_copy', 
    'Passport Front': 'passport_front', 
    'Passport Back': 'passport_back', 
    'Processing Fee Receipt': 'processing_fee_receipt', 
    'Prode42': 'prode42', 
    'Rent Agreement': 'rent_agreement', 
    'Salary Slip': 'salary_slip', 
    'Security Cheques': 'security_cheques', 
    'Sale Deed': 'sale_deed', 
    'Self Attested': 'self_attested', 
    'Self Attested Aadhar': 'self_attested_aadhar', 
    'Self Attested PAN': 'self_attested_pan', 
    'Sanction Letter': 'sanction_letter', 
    'Shop Act': 'shop_act', 
    'Two Reference': 'reference', 
    'Udyog Aadhaar Certificate': 'udyog_aadhaar_certificate', 
    'Utility Bill Validation': 'utilitybillvalidation', 
    'Driving License': 'driving_license', 
    'Votar ID Front': 'votar_id_front', 
    'Votar ID Back': 'votar_id_back', 
    'Virtual Account': 'virtual_account', 
    'Other': 'other', 
    'Co-Applicant Aadhar Card': 'co_applicant_aadhar_card', 
    'Co-Applicant Aadhar Card Back': 'co_applicant_aadhar_card_back', 
    'Co-Applicant Bank Statement': 'co_applicant_bank_statement', 
    'Co-Applicant BUREAU Report': 'co_applicant_equifax_report', 
    'Co-Applicant Customer Photo': 'co_applicant_customer_photo', 
    'Co-Applicant Pan Card': 'co_applicant_pan_card', 
    'Co-Applicant GST': 'co_applicant_gst', 
    'Co-Applicant ITR': 'co_applicant_itr', 
    'OSV': 'original_seen_verified', 
    'Quotation Bill / Disbursement Advice': 'proforma', 
    'Signed Disbursement Advice': 'pro_forma_invoice'
}

DOC_FORMAT = ['jpg', 'gif', 'mp4', 'jpeg', 'png', 'bmp', 'tif', 'tiff', 'xlsx', 'xls', 'pdf', 'txt', 'odt', 'xml', 'zip']


URL = env['URL']


LEVEL = 'DEBUG'
PORT = 5006



