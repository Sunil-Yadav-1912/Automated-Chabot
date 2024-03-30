import mysql.connector
import config
import requests
from s3_functions import s3_upload
import queries
from datetime import datetime, timedelta
from utils.php_encrypt_decrypt import decrypt,encrypt

def connect():
    mydb = mysql.connector.connect(
    host = config.DBHOSTNAME,
    user = config.DBUSERNAME,
    password = config.DBPASSWORD,
    database = config.DBNAME
    )
    return mydb

def checkIfExists(searchBy, value):
    mydb = connect()
    mycursor = mydb.cursor()
    if searchBy == "id" : 
        mycursor.execute(queries.CHECKIFEXISTSBYID.format(value))
        myresult = mycursor.fetchall()
    elif searchBy == "mobile" : 
        enc_mobile = encrypt(str(value))
        print(queries.CHECKIFEXISTSBYPHONE.format(enc_mobile))
        mycursor.execute(queries.CHECKIFEXISTSBYPHONE.format(enc_mobile))
        myresult = mycursor.fetchall()
        print(myresult)

    elif searchBy == "pan" : 
        enc_pan = encrypt(str(value))
        print(queries.CHECKIFEXISTSBYPAN.format(enc_pan))
        mycursor.execute(queries.CHECKIFEXISTSBYPAN.format(enc_pan))
        myresult = mycursor.fetchall()
        print(myresult)

    elif searchBy == "email" : 
        enc_email = encrypt(str(value))
        print(queries.CHECKIFEXISTSBYMAIL.format(enc_email))
        mycursor.execute(queries.CHECKIFEXISTSBYMAIL.format(enc_email))
        myresult = mycursor.fetchall()
        print(myresult)
    else : 
        print("Enter in a proper format")
        return "Enter in a proper format", ""

    print(myresult)
    if len(myresult) == 0 or myresult == "" :
        return 'No Data Found', ""
    elif len(myresult) > 0 and searchBy == 'mobile':
        print(queries.GETBYPHONE.format(enc_mobile))
        mycursor.execute(queries.GETBYPHONE.format(enc_mobile))
        myresult2 = mycursor.fetchall()
  
        print(len(myresult2))
        resp = "Below are the applications with this Mobile number<br><br>Choose your application<br><br>"
        if len(myresult2) > 0:
            for result in myresult2 :
                print(result)
                if result[0] != 0 and result[1] != "": 
                    resp = resp + '<span class="option-command" data-id="{0}" data-type="application-status">{1}<br><br></span>'.format(result[0],result[1])
                else :
                    resp = resp + ""
            if resp != "":
                return "choose", resp
        else:
            print("This Phone number not exists")
            return "This Phone number not exists",''
    elif len(myresult) > 0 and searchBy == 'email':
        print(queries.GETBYMAIL.format(enc_email))
        mycursor.execute(queries.GETBYMAIL.format(enc_email))
        myresult2 = mycursor.fetchall()

        print(len(myresult2))
        resp = "Below are the applications with this Email<br><br>Choose your application<br><br>"
        if len(myresult2) > 0:
            for result in myresult2 :
                print(result)
                if result[0] != 0 and result[1] != "": 
                    resp = resp + '<span class="option-command" data-id="{0}" data-type="application-status">{1}<br><br></span>'.format(result[0],result[1])
                else :
                    resp = resp + ""
            if resp != "":
                return "choose", resp
        else:
            print("This Email not exists")
            return "This Email not exists",''
    elif len(myresult) > 0 and searchBy == 'pan':
        print(queries.GETBYPAN.format(enc_pan))
        mycursor.execute(queries.GETBYPAN.format(enc_pan))
        myresult2 = mycursor.fetchall()

        print(len(myresult2))
        resp = "Below are the applications with this Pan number<br><br>Choose your application<br><br>"
        if len(myresult2) > 0:
            for result in myresult2 :
                print(result)
                if result[0] != 0 and result[1] != "": 
                    resp = resp + '<span class="option-command" data-id="{0}" data-type="application-status">{1}<br><br></span>'.format(result[0],result[1])
                else :
                    resp = resp + ""
            if resp != "":
                return "choose", resp
        else:
            print("This Pan number not exists")
            return "This Pan number not exists",''
    else :
        id = str(myresult[0][1])
        return 'exists', id
        

def checkIfUserExists(id):
    mydb = connect()
    mycursor = mydb.cursor()
    mycursor.execute(queries.CHECKIFUSEREXISTS.format(id))
    myresult = mycursor.fetchall()
    # print(myresult)
    if myresult[0][0] == 0 :
        resp = 'Invalid ID'
    else :
        resp = 'exists'
    return resp

def botStart(id,status):
    mydb = connect()
    mycursor = mydb.cursor()

    mycursor.execute(queries.GETNAME.format(id))
    myresult = mycursor.fetchall()

    applicationDetails = getApplicantDetails(id)
    # print(myresult)
    if len(myresult) == 0 :
        resp = 'No name found<br><br><span class="option-command" data-id="#" data-type="main-menu">Main menu</span>'
    else :
        resp = 'Welcome {0}~{1}~{2}~, <br><br>{3}<br><br><span class="option-command" data-id="AS" data-type="application-status">AS - Application Status <br><br></span> <span class="option-command" data-id="MD" data-type="merchant-status">MD - Merchant Details <br><br> </span><span class="option-command" data-id="CP" data-type="collection-panel">CP - Collection Panel<br><br></span><span class="option-command" data-id="LN" data-type="lender-details">LN - Lender Name </span><br><br><span class="option-command" data-id="LD" data-type="loan-details">LD - Loan Details <br><br></span> <span class="option-command" data-id="AD" data-type="advisor-details">AD - Advisor Details <br><br></span><span class="option-command" data-id="MS" data-type="mini-scorecard">MS - Mini Scorecard</span><br><br><span class="option-command" data-id="GD" data-type="get-documents">GD - Get Documents</span><br><br><span class="option-command" data-id="DG" data-type="digio-details">DG - Digio Details</span><br><br><span class="option-command" data-id="ID" data-type="insert-document">ID - Insert Document</span><br><br><a href="{4}/admin/consumer-applications/edit/{5}"  target="_blank">Edit Customer</a>'.format(str(myresult[0][0]),id,status,applicationDetails,config.URL,id)
    return resp

def getAdvisor(id):
    mydb = connect()
    mycursor = mydb.cursor()
    mycursor.execute(queries.GETADVISOR.format(id))
    myresult = mycursor.fetchall()
    # print(myresult)
    if len(myresult) == 0 :
        resp = 'Advisor not found<br><br><span class="option-command" data-id="#" data-type="main-menu">Main menu</span>'
    else :
        resp = 'Your advisor name is {0} <br>Phone - {1} <br>Email - {2} <br><br><span class="option-command" data-id="#" data-type="application-status">Main menu</span>'.format(str(myresult[0][0]),str(myresult[0][1]),str(myresult[0][2]))
    return resp

def getLoanDetails(id):
    mydb = connect()
    mycursor = mydb.cursor()
    mycursor.execute(queries.GETLOANDETAILS.format(id))
    myresult = mycursor.fetchall()
    # print(myresult)
    
    if len(myresult) == 0 :
        resp = 'Loan not found<br><br><span class="option-command" data-id="#" data-type="main-menu">Main menu</span>'
    else :
        resp = 'Loan amount - {0} <br>Approved amount - {1} <br>Tenure - {2} <br><br><span class="option-command" data-id="#" data-type="application-status">Main menu</span>'.format(str(myresult[0][0]),str(myresult[0][1]),str(myresult[0][2]))
    return resp

def getEmiDetails(id):
    mydb = connect()
    mycursor = mydb.cursor()
    mycursor.execute(queries.GETEMIDETAILS.format(id))
    myresult = mycursor.fetchall()
    # print(myresult)
    if len(myresult) == 0 :
        resp = 'EMI Schedule not found<br><br><span class="option-command" data-id="#" data-type="main-menu">Main menu</span>'
    else :
        resp = 'Emi - {0} <br>Advance Emi - {1} <br>Interest Rate - {2} <br>Tenure - {3} <br>Remaining Emi - {4} <br>Subvention - {5} <br>Processing fee - {6} <br><br><span class="option-command" data-id="#" data-type="application-status">Main menu</span>'.format(str(myresult[0][9]),str(myresult[0][5]),str(myresult[0][6]),str(myresult[0][3]),str(myresult[0][4]),str(myresult[0][7]),str(myresult[0][8]))
    return resp

def getScorecard(id):
    mydb = connect()
    mycursor = mydb.cursor()
    mycursor.execute(queries.GETSCORECARD.format(id))
    myresult = mycursor.fetchall()
    # print(myresult)
    if len(myresult) == 0 :
        resp = 'Scorecard values not found<br><br><span class="option-command" data-id="#" data-type="main-menu">Main menu</span>'
    else :
        resp = '<b>Score-Card</b><br><br>Monthly Income - {0} <br> Company Name - {1} <br> Credit Score : {2} <br><br><span class="option-command" data-id="#" data-type="application-status">Main menu</span>'.format(str(myresult[0][0]),str(myresult[0][1]),str(myresult[0][2]))
    return resp

def getStatus(id):
    mydb = connect()
    mycursor = mydb.cursor()
    mycursor.execute(queries.GETSTATUS.format(id))
    myresult = mycursor.fetchall()
    # print(myresult)
    if len(myresult) == 0 :
        resp = 'Your application not found<br><br><span class="option-command" data-id="#" data-type="main-menu">Main menu</span>'
    else :
        resp = 'Your application is in {0} state <br><br><span class="option-command" data-id="#" data-type="application-status">Main menu</span>'.format(str(myresult[0][0]))
    return resp

def getLender(id):
    mydb = connect()
    mycursor = mydb.cursor()
    mycursor.execute(queries.GETLENDER.format(id))
    myresult = mycursor.fetchall()
    # print(myresult)
    if len(myresult) == 0 :
        resp = 'Lender not found<br><br><span class="option-command" data-id="#" data-type="main-menu">Main menu</span>'
    else :
        resp = 'Your application is in {0} state <br><br><span class="option-command" data-id="#" data-type="application-status">Main menu</span>'.format(str(myresult[0][0]))
    return resp

def getMerchant(id):
    mydb = connect()
    mycursor = mydb.cursor()
    mycursor.execute(queries.GETMERCHANT.format(id))
    myresult = mycursor.fetchall()
    # print(myresult)
    if len(myresult) == 0 :
        resp = 'Merchant not found<br><br><span class="option-command" data-id="#" data-type="main-menu">Main menu</span>'
    else :
        if (myresult[0][2] is None or myresult[0][2] == ''): 
            decrypt_email = 'Email not found'
        else : 
            decrypt_email = decrypt(str(myresult[0][2]))
            # print('Decrypted email successfully') 
        resp = 'Merchant Name - {0} <br> Mobile - {1} <br> Email - {2} <br><br><span class="option-command" data-id="#" data-type="application-status">Main menu</span>'.format(str(myresult[0][0]),str(myresult[0][1]),decrypt_email)
    return resp

def insertDocument(id):
    document_names = ["File Aadhar Card","File Aadhar Card Back","File Pan Card","Aadhar Card","Aadhar Card Back","Advance Amount Receipt","Agreement","Applicant Customer Photo","Bank Statement 1","Bank Statement 2","Bank Statement 3","Bank Statement 6","BUREAU Report","Call Recording","CPV","Credit Appraisal Memo","Gas Bill","Electricity Bill","Finbit Analysis","FOIR","GST Certificate","Insurance Payment Receipt","ITR","MCA","Nach","Pan Card","Pan Validation","Passbook Copy","Passport Front","Passport Back","Processing Fee Receipt","Prode42","Rent Agreement","Salary Slip","Security Cheques","Sale Deed","Self Attested","Self Attested Aadhar","Self Attested PAN","Sanction Letter","Shop Act","Two Reference","Udyog Aadhaar Certificate","Utility Bill Validation","Driving License","Votar ID Front","Votar ID Back","Virtual Account","Other","Co-Applicant Aadhar Card","Co-Applicant Aadhar Card Back","Co-Applicant Bank Statement","Co-Applicant BUREAU Report","Co-Applicant Customer Photo","Co-Applicant Pan Card","Co-Applicant GST","Co-Applicant ITR","OSV","Quotation Bill / Disbursement Advice","Signed Disbursement Advice"]
    documents_string = ', '.join(document_names)

    resp = documents_string
    return resp

def getDocuments(id):
    mydb = connect()
    mycursor = mydb.cursor()
    mycursor.execute(queries.GETDOCUMENTS.format(id))
    myresult = mycursor.fetchall()
    # print(myresult)
    if len(myresult) == 0 :
        resp = 'Documents not found'
    else :
        resp = '<b>Documents</b><br>'
        document_type = ["file_aadhaar_card","file_aadhaar_card_back","file_pan_card","aadhar_card","aadhar_card_back","advance_amount_receipt","agreement","customer_photo","bank_statement","bank_statement_2","bank_statement_3","bank_statement_6","equifax_report","call_recording","cpv","credit_appraisal_memo","1","1","finbit_analysis","foir","gst_certificate","insurance_payment_receipt","itr","mca","nach","pan_card","panvalidation","passbook_copy","passport_front","passport_back","processing_fee_receipt","prode42","rent_agreement","salary_slip","security_cheques","sale_deed","self_attested","self_attested_aadhar","self_attested_pan","sanction_letter","shop_act","reference","udyog_aadhaar_certificate","utilitybillvalidation","driving_license","votar_id_front","votar_id_back","virtual_account","other","co_applicant_aadhar_card","co_applicant_aadhar_card_back","co_applicant_bank_statement","co_applicant_equifax_report","co_applicant_customer_photo","co_applicant_pan_card","co_applicant_gst","co_applicant_itr","original_seen_verified","proforma","pro_forma_invoice"]
        document_name = ["File Aadhar Card","File Aadhar Card Back","File Pan Card","Aadhar Card","Aadhar Card Back","Advance Amount Receipt","Agreement","Applicant Customer Photo","Bank Statement 1","Bank Statement 2","Bank Statement 3","Bank Statement 6","BUREAU Report","Call Recording","CPV","Credit Appraisal Memo","Gas Bill","Electricity Bill","Finbit Analysis","FOIR","GST Certificate","Insurance Payment Receipt","ITR","MCA","Nach","Pan Card","Pan Validation","Passbook Copy","Passport Front","Passport Back","Processing Fee Receipt","Prode42","Rent Agreement","Salary Slip","Security Cheques","Sale Deed","Self Attested","Self Attested Aadhar","Self Attested PAN","Sanction Letter","Shop Act","Two Reference","Udyog Aadhaar Certificate","Utility Bill Validation","Driving License","Votar ID Front","Votar ID Back","Virtual Account","Other","Co-Applicant Aadhar Card","Co-Applicant Aadhar Card Back","Co-Applicant Bank Statement","Co-Applicant BUREAU Report","Co-Applicant Customer Photo","Co-Applicant Pan Card","Co-Applicant GST","Co-Applicant ITR","OSV","Quotation Bill / Disbursement Advice","Signed Disbursement Advice"]
        for document in myresult :
            print(document[2])
            if document[1] in document_type :
                index = document_type.index(document[1])
                name = document_name[index]
            else :
                name = document[1]
            print(document[1])
            print(name)

            resp = resp + '<br><a href="{0}/admin/consumer-application/get-documents/{1}" target="_blank">{2}</a>'.format(config.URL,str(document[2]),name)
        resp = resp + '<br><br><span class="option-command" data-id="#" data-type="application-status">Main menu</span>'
    return resp

def getCollectionPanel(id):

    url = "{0}/api/loans/{1}".format(config.URL,str(id))

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    if response.status_code == 200 :
        resp = response.json()
        print(resp)

        # print(resp["payments"][0])
        # name = ""
        if resp == [] :
            response = 'No Data Yet<br><br><span class="option-command" data-id="#" data-type="main-menu">Main menu</span>'
        else :
            response = '<b>Collection Panel</b><br>'
            name            = resp["application"]["name"] 
            total_amount_due = resp["application"]["application_element"]["total_amount_due"]
            processing_due  = resp["processing_fee_due"]
            advance_due     = resp["advance_amount_due"]
            emi_due         = resp["application"]["application_element"]["emi_pending"]
            over_payment    = resp["over_payment"] 
            amount_paid     = resp["amount_paid"]
            emi_paid        = resp["application"]["application_element"]["emi_paid"]
            amount_pending  = resp["application"]["application_element"]["total_amount_due"] 
            last_emi_date   = resp["application"]["application_element"]["last_emi_date"] 
            max_payable     = resp["max_payable"]
            foreclosure_amount  = resp["foreclosure_amount"]

            response = response + '<br>Name : {0}<br>Total Amount Due : {1}<br>Processing Due : {2}<br>Advance Due : {3}<br>EMI Due : {4}<br>Over Payment : {5}<br>Amount Paid : {6}<br>EMI Paid : {7}<br>Amount Pending : {8}<br>Last EMI Date : {9}<br>Max Payable : {10}<br>Foreclosure Amount : {11}<br><br><span class="option-command" data-id="#" data-type="application-status">Main menu</span>'.format(name, str(total_amount_due), str(processing_due), str(advance_due), str(emi_due), str(over_payment), str(amount_paid), str(emi_paid), str(amount_pending), str(last_emi_date),str(max_payable),str(foreclosure_amount))
        return response
    else :
        return 'No Data found<br><br><span class="option-command" data-id="#" data-type="main-menu">Main menu</span>'

def getApplicantDetails(id):
    mydb = connect()
    mycursor = mydb.cursor()
    mycursor.execute(queries.GETAPPLICANT.format(id))
    myresult = mycursor.fetchall()
    # print(myresult)
    if len(myresult) == 0 :
        resp = 'Applicant not found<br><br><span class="option-command" data-id="#" data-type="main-menu">Main menu</span>'
    else :
        if (myresult[0][2] is None or myresult[0][2] == ''): 
            decrypt_email = 'Email not found'
        else : 
            decrypt_email = decrypt(str(myresult[0][2]))
            # print('Decrypted email successfully') 
        if (myresult[0][1] is None or myresult[0][1] == ''): 
            decrypt_phone = 'Phone not found'
        else : 
            decrypt_phone = decrypt(str(myresult[0][1]))
            # print('Decrypted phone successfully')
        resp = 'Applicant Name - {0} <br> Mobile - {1} <br> Email - {2}'.format(str(myresult[0][0]),decrypt_phone,decrypt_email)
    return resp


def getDigioDetails(id,isWhatsappCall):
    mydb = connect()
    mycursor = mydb.cursor()
    mycursor.execute(queries.GETDIGIODETAILS.format(id))
    myresult = mycursor.fetchall()
    if isWhatsappCall == "1" :
        if len(myresult) == 0 :
            resp = {
                'status' : "FAIL",
                'message' : "Digio details not found"
            }
        else :
            resp = {
                'status' : "OK",
                'Link': str(myresult[0][3]),
                'Journey': myresult[0][5],
                'Status': myresult[0][6],
            }    
    else :
        # print(myresult)
        if len(myresult) == 0 :
            resp = 'Digio details not found<br><br><span class="option-command" data-id="#" data-type="main-menu">Main menu</span>'
        else :
            resp = '<b>Applicant Digio</b> <br><br> Link - {0} <br> Journey - {1} <br> Status - {2}'.format(str(myresult[0][3]),myresult[0][5],myresult[0][6])
    return resp


# Whatsapp APIs 

# Creating an application in consumer applications

def createLoanApplication(loan_information,isWhatsappCall):
    try:
        last_inserted_id = None
        status = "form completed"
        mydb = connect()
        mycursor = mydb.cursor()
        if 'email' in loan_information and loan_information['email'] is not None :
            if len(loan_information['email']) > 0 :
                loan_information['email'] = encrypt(loan_information['email'])
        if 'mobile' in loan_information and loan_information['mobile'] is not None :
            if len(loan_information['mobile']) > 0 :
                loan_information['mobile'] = encrypt(loan_information['mobile'])
        if 'pan' in loan_information and loan_information['pan'] is not None :
            if len(loan_information['pan']) > 0 :
                loan_information['pan'] = encrypt(loan_information['mobile'])
        if 'aadhar' in loan_information and loan_information['aadhar'] is not None :
            if len(loan_information['aadhar']) > 0 :
                loan_information['aadhar'] = encrypt(loan_information['mobile'])
        
        consumerApplicationValues = (
            loan_information.get('name', None),
            float(loan_information.get('loan_amount', None).replace(',', '')) if loan_information.get('loan_amount') else None,
            float(loan_information.get('tenure_value', None)) if loan_information.get('tenure_value') else None,
            loan_information.get('email', None),
            loan_information.get('mobile', None),
            loan_information.get('dob', None),
            loan_information.get('purpose', None),
            loan_information.get('pan', None),
            loan_information.get('aadhar', None),
            status
        )

        mycursor.execute(queries.CREATE_APPLICATION_ENTRY,consumerApplicationValues)

        mydb.commit()
        mycursor.execute("SELECT LAST_INSERT_ID()")
        last_inserted_consumer_id = mycursor.fetchone()[0]
        usersValues = (
            loan_information.get('name', None),
            loan_information.get('email', None),
            loan_information.get('mobile', None),
            loan_information.get('dob', None),
        )
        mycursor.execute(queries.CREATE_USER_ENTRY,usersValues)

        mydb.commit()
        mycursor.execute("SELECT LAST_INSERT_ID()")
        last_inserted_user_id = mycursor.fetchone()[0]

        statusLogValues = (
            last_inserted_consumer_id,
            last_inserted_user_id,
            status
        )
        mycursor.execute(queries.CREATE_STATUS_LOG_ENTRY,statusLogValues)
        mydb.commit()

        elementValues = (
            last_inserted_consumer_id,
        )
        mycursor.execute(queries.CREATE_ELEMENT_ENTRY,elementValues)
        mydb.commit()
 
    except mysql.connector.Error as e:
        print(f"Error: {e}")
        return "Something went wrong"
    finally:
        if mydb.is_connected():
            mycursor.close()
            mydb.close()
    print(f"Last Inserted ID: {last_inserted_consumer_id}")
    # return last_inserted_consumer_id
    if isWhatsappCall == "1" :
        if last_inserted_consumer_id == 0 :
            resp = {
                'status' : "FAIL",
                'message' : "Application not created",
                'id' : 0
            }
        else :
            resp = {
                'status' : "OK",
                'messge': "Application Created successfully",
                'id' : last_inserted_consumer_id
            }  
    else :
        # resp = {'applicationId': str(last_inserted_consumer_id)}
        resp = 'Created Application ✓ ID - {0}<br><br><span class="option-panel" id="isCreateIcon" data-type="isCreate">Create another</span><br><br><span class="option-panel" id="isHomeIcon" data-type="isHome">Go to Home</span>'.format(str(last_inserted_consumer_id))

    return resp

# Function to update the loan application

def updateLoanApplication(additional_info,app_id,isWhatsappCall):
    try:
        mydb = connect()
        mycursor = mydb.cursor()
        # Update query based on the provided additional information
        if additional_info['email'] is not None :
            if len(additional_info['email']) > 0 :
                additional_info['email'] = encrypt(additional_info['email'])
        if additional_info['mobile'] is not None :
            if len(additional_info['mobile']) > 0 :
                additional_info['mobile'] = encrypt(additional_info['mobile'])
        if additional_info['pan'] is not None :
            if len(additional_info['pan']) > 0 :
                additional_info['pan'] = encrypt(additional_info['mobile'])
        if additional_info['aadhar'] is not None :
            if len(additional_info['aadhar']) > 0 :
                additional_info['aadhar'] = encrypt(additional_info['mobile'])
        consumerApplicationValues = (
            additional_info.get('name', None),
            float(additional_info.get('loan_amount', None).replace(',', '')) if additional_info.get('loan_amount') else None,
            float(additional_info.get('tenure_value', None)) if additional_info.get('tenure_value') else None,
            additional_info.get('email', None),
            additional_info.get('mobile', None),
            additional_info.get('dob', None),
            additional_info.get('purpose', None),
            additional_info.get('pan', None),
            additional_info.get('aadhar', None),
            app_id
        )

        mycursor.execute(queries.UPDATE_APPLICATION,consumerApplicationValues)
        mydb.commit()

    except mysql.connector.Error as e:
        print(f"Error: {e}")
        return "Something went wrong"

    finally:
        if mydb.is_connected():
            mycursor.close()
            mydb.close()

    if isWhatsappCall == "1" :
        if app_id == 0 :
            resp = {
                'status' : "FAIL",
                'message' : "Application not Updated",
                'id' : 0
            }
        else :
            resp = {
                'status' : "OK",
                'message': "Updated application successfully",
                'id' : app_id

            }  
    else :
        resp = "Updated {0}".format(str(app_id))
    return resp

def updateDocument(my_list, app_id, isWhatsappCall):
    resp = ""
    try:
        # print(my_list)
        # file_name = config.DOC_PATH[my_list['doc_name']]
        if isWhatsappCall == "0":
            file_name = config.DOC_NAMES[my_list['doc_name']]            

        doc_size = (len(my_list['doc_content']) * 3) / 4
        doc_format = my_list['doc_format'].lower()
        doc_content = my_list['doc_content']

        if doc_size < 10000000 and doc_format in config.DOC_FORMAT:

            document_exists = checkDocument(app_id, file_name)
            if document_exists:
                s3_uploaded, path = s3_upload(app_id, file_name, doc_content,
                                                doc_format)  # True, '2258/pan_card.jpeg'
                if s3_uploaded:
                    flag = insertFile(app_id, file_name, path, isWhatsappCall)
                    if flag :
                        if isWhatsappCall == "1":
                            resp = {
                                'status' : "OK",
                                'message' : "Document Uploaded successfully",
                                'id' : int(app_id)
                            }
                        else:
                            resp = "Document Uploaded successfully<br><br><span class='option-command' data-id='#' data-type='main-menu'>Main menu</span>"
                else : 
                    print("Something went wrong while uploading")
                    if isWhatsappCall == "1" :
                        resp = {
                                    'status' : "FAIL",
                                    'message' : "Something went wrong while uploading",
                                    'id' : 0
                                }
                    else:
                        resp = "Something went wrong while uploading"

                return resp
            else:
                if isWhatsappCall == "1" :
                    resp = {
                                'status' : "FAIL",
                                'message' : "Document Already exists",
                                'id' : 0
                            }
                else:
                    resp = "Document Already exists<br><br><span class='option-command' data-id='#' data-type='main-menu'>Main menu</span>"

    except Exception as e:
        if isWhatsappCall == "1" :
            resp = {
                        'status' : "FAIL",
                        'message' : "Something went wrong",
                        'id' : 0
                    }
        else:
            resp = "Something went wrong<br><br><span class='option-command' data-id='#' data-type='main-menu'>Main menu</span>"

        return resp

def insertFile(app_id,doc_name,doc_path,isWhatsappCall):
    try:
        mydb = connect()
        mycursor = mydb.cursor()
        # Update query based on the provided additional information

        consumerFilesValues = (
            app_id,
            doc_name,
            doc_path,
            "1",
            107,
        )

        mycursor.execute(queries.INSERT_FILES,consumerFilesValues)
        mydb.commit()

    except mysql.connector.Error as e:
        print(f"Error: {e}")
        return False

    finally:
        if mydb.is_connected():
            mycursor.close()
            mydb.close()
        return True
        


def checkDocument(app_id, file_name):
    resp = True
    try:
        mydb = connect()
        mycursor = mydb.cursor()


        mycursor.execute(queries.CHECK_FILE, (app_id, file_name))
        myresult = mycursor.fetchall()

        if len(myresult) != 0:
            resp = False
        
    except mysql.connector.Error as e:
        print(f"Error: {e}")
        resp = False
        return resp
    except Exception as e:
        print(f"Error: {e}")
        resp = False
        return resp
    finally:
        if mydb.is_connected():
            mycursor.close()
            mydb.close()
        resp = True
        return resp


def check_duplicate(mobile_number=None, email=None, pan_card=None):
    mydb = connect()
    resp = False
    mycursor = mydb.cursor()
    curr_time = datetime.now()
    dedupe_period = curr_time - timedelta(days=90)
    mobile_status, email_status, pan_status = False, False, False

    if mobile_number:
        mycursor.execute(queries.CHECKBYPHONE, (mobile_number, dedupe_period))
        mobile_status = mycursor.fetchall()

        if len(mobile_status) != 0:
            resp = True
            return resp

        
    if email:
        mycursor.execute(queries.CHECKBYEMAIL, (email,  dedupe_period))
        email_status = mycursor.fetchall()

        if len(email_status) != 0:
            resp = True
            return resp

    if pan_card:
        mycursor.execute(queries.CHECKBYPAN, (pan_card, dedupe_period))
        pan_status = mycursor.fetchall()

        if len(pan_status) != 0:
            resp = True
            return resp

    return resp