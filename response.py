import database
import re

def getResponse(msg,id,isWhatsappCall) :
    searchBy = ""
    commands = ["AS","MD","CP","LN","LD","AD","MS","GD","DG","ID","#","as","md","cp","ln","ld","ad","ms","gd","dg","id"]
    if(msg not in commands):
        if msg.isnumeric():
            if len(msg) > 0 and len(msg) <= 7:
                searchBy = "id"
            elif len(msg) >= 10:
                if isValidMobile(msg):
                    searchBy = "mobile"
                else :
                    return "Please enter valid input <br><br> Enter any one of these App ID / Mobile / Email / Pan to start the bot"
            else :
                return "Please enter valid input <br><br> Enter any one of these App ID / Mobile / Email / Pan to start the bot"
        elif isValidEmail(msg):
            searchBy = "email"

        elif isValidPan(msg):
            searchBy = "pan"
        else:
            return "Please enter valid input <br><br> Enter any one of these App ID / Mobile / Email / Pan to start the bot"
        # match_list = re.findall(r'id|email|mobile|pan', msg, re.IGNORECASE)
        # print("entry")
        # print(any(match_list))
        # print("exit")
        
        if searchBy != "" and len(msg) > 0 :
            try :
                # arr = msg.split('-')
                # searchBy = ""
                # value = str(arr[1])
                value = msg
                print(searchBy, value)
                checkIfExists,value = database.checkIfExists(searchBy, value)
                print(checkIfExists)
                if checkIfExists == "exists" and value != "" :
                    status = "start"
                    resp = database.botStart(value,status)
                    return resp
                elif checkIfExists == "choose" and value != "": 
                    resp = value
                    return resp
                else :
                    print(checkIfExists)
                    print(value)
                    return checkIfExists
            except : 
                return "Please enter valid input <br><br> Enter any one of these App ID / Mobile / Email / Pan to start the bot"

    elif msg.upper() == 'AS':
        if id != '':
            id = id
        else:
            resp = 'Please enter id first'
            return resp
        resp = database.getStatus(id)
        return resp

    elif msg.upper() == 'MD':
        if id != '':
            id = id
        else:
            resp = 'Please enter id first'
            return resp
        resp = database.getMerchant(id)
        return resp

    elif msg.upper() == 'CP':
        if id != '':
            id = id
        else:
            resp = 'Please enter id first'
            return resp
        resp = database.getCollectionPanel(id)
        return resp

    elif msg.upper() == 'LN':
        if id != '':
            id = id
        else:
            resp = 'Please enter id first'
            return resp
        resp = database.getLender(id)
        return resp

    elif msg.upper() == 'LD':
        if id != '':
            id = id
        else:
            resp = 'Please enter id first'
            return resp
        resp = database.getEmiDetails(id)
        return resp

    elif msg.upper() == 'AD':
        if id != '':
            id = id
        else:
            resp = 'Please enter id first'
            return resp
        resp = database.getAdvisor(id)
        return resp

    # elif msg.upper() == '7':
    #     if id != '':
    #         id = id
    #     else:
    #         resp = 'Please enter id first'
    #         return resp
    #     resp = database.getLoanDetails(id)
    #     return resp

    elif msg.upper() == 'MS':
        if id != '':
            id = id
        else:
            resp = 'Please enter id first'
            return resp
        resp = database.getScorecard(id)
        return resp
    
    elif msg.upper() == 'GD':
        if id != '':
            id = id
        else:
            resp = 'Please enter id first'
            return resp
        resp = database.getDocuments(id)
        return resp

    # elif msg.upper() == '10':
    #     if id != '':
    #         id = id
    #     else:
    #         resp = 'Please enter id first'
    #         return resp
    #     resp = database.getCollectionPanel(id)
    #     return resp
    

    elif msg.upper() == 'DG':
        if id != '':
            id = id
        else:
            resp = 'Please enter id first'
            return resp
        resp = database.getDigioDetails(id,isWhatsappCall)
        return resp

    elif msg.upper() == 'ID':
        if id != '':
            id = id
        else:
            resp = 'Please enter id first'
            return resp
        resp = database.insertDocument(id)
        return resp

    elif msg.upper() == '#':
        if id != '':
            id = id
        else:
            resp = 'Please enter id first'
            return resp
        status = "menu"
        resp = database.botStart(id,status)
        return resp
    # elif 'Hello' in msg or 'hi' in msg or 'hello' in msg or 'Hi' in msg:
    #     resp = 'Welcome ,<br> how may i help you ?'
    #     return resp

    else :
        response = "Please enter valid input <br><br> Enter any one of these App ID / Mobile / Email / Pan to start the bot"
        resp = str(response)
        return resp


def isValidEmail(msg):  
    if re.match(r"[^@]+@[^@]+\.[^@]+", msg):  
        return True
    return False  

def isValidMobile(msg):  
    if re.match(r"(0|91)?[6-9][0-9]{9}", msg):  
        return True
    return False
def isValidPan(msg):  
    if re.match(r"[A-Za-z]{5}\d{4}[A-Za-z]{1}", msg):  
        return True
    return False 
  
  