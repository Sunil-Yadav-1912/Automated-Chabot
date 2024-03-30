from flask import Flask, render_template, request, jsonify
import config
import automate
import response
# import middleware
from token_validation import token_required
from baselogger import logger

#Flask initialization
app = Flask(__name__)
app.secret_key = "super secret key"
app.config['SECRET_KEY'] = "super secret key"

# app.wsgi_app = middleware.Middleware(app.wsgi_app)

@app.route("/")
def index():
    return render_template("chatbot.html")

@app.route("/get-response", methods=["post"])
# @token_required
def ChatbotResponse():
    msg = request.form["msg"]
    id = request.form["id"]
    isUpdateCall = request.form["isUpdateCall"]
    isCreateCall = request.form["isCreateCall"]
    isWhatsappCall = request.form["isWhatsappCall"]
    isDocumentCall = request.form["isDocumentCall"]

    if isWhatsappCall == "1" :
        # name = request.form["name"]
        # email = request.form["email"]
        # mobile = request.form["mobile"]
        # tenure = request.form["tenure"]
        # amount = request.form["amount"]
        if isCreateCall == "1" :
            # msg = '''name : Sunil Y Testing Whatsapp,email : sunil.yadav@creditfair.in,mobile : 9028027397,tenure : 8 years,dob : 2003/12/19,amount : 100000, purpose = testing, pan - BMFPY7175Q, aadhar : 9102919398293'''
            resp = automate.createApplication(msg,isWhatsappCall)
            print(resp)
        elif isUpdateCall == "1":
            # msg = '''name : Sunil Y Testing Whatsapp update, email : sunil@creditfair.in,mobile : 9028027397,tenure : 8 months,dob : 2004/12/19,amount : 200000, purpose : testing, pan : BMFPY7175Q, aadhar : 9102919398293'''
            if id == "" :
                resp = "Please enter the id first"
            else :
                resp = automate.updateApplication(msg,id,isWhatsappCall)
        elif isDocumentCall == "1":
            # msg = '''name : Sunil Y Testing Whatsapp update, email : sunil@creditfair.in,mobile : 9028027397,tenure : 8 months,dob : 2004/12/19,amount : 200000, purpose : testing, pan : BMFPY7175Q, aadhar : 9102919398293'''
            if id == "" :
                resp = "Please enter the id first"
            else :
                resp = automate.updateDocument(msg,id,isWhatsappCall)
        elif msg.upper() == "DG" :
            resp = automate.getDigioDetails(id,isWhatsappCall)
        else :
            resp = {
                'status' : 'FAIL',
                'message' : 'Invalid Command',
                'id':0
            }
        res = MakeResponseWhatsapp(resp)
    else:
        if isCreateCall == "1" :
            resp = automate.createApplication(msg,isWhatsappCall)
            print(resp)
        elif isUpdateCall == "1" :
            if id == "" :
                resp = "Please enter the id first"
            else :
                resp = automate.updateApplication(msg,id,isWhatsappCall)
        elif isDocumentCall == "1" :
            if id == "" :
                resp = "Please enter the id first"
            else :
                resp = automate.updateDocument(msg,id,isWhatsappCall)
        else :
            resp = response.getResponse(msg,id,isWhatsappCall)
        
        res = MakeResponse(resp)

    logger.info("App_ID : {0}, Request : {1}, Response : {2}".format(id,msg,resp))
    return res

@app.route("/create-loan", methods=["post"])
# @token_required
def createLoan():
    msg = request.get_json()
    isWhatsappCall = "1"
    # msg = '''name : Sunil Y Testing Whatsapp,email : sunil.yadav@creditfair.in,mobile : 9028027397,tenure : 8 years,dob : 2003/12/19,amount : 100000, purpose = testing, pan - BMFPY7175Q, aadhar : 9102919398293'''
    resp = automate.createApplication(msg,isWhatsappCall)
    print(resp)

    logger.info("App_ID : {0}, Request : {1}, Response : {2}".format(id,msg,resp))
    res = MakeResponseWhatsapp(resp)
    return res


@app.route("/upload-doc", methods=["post"])
# @token_required
def uploadDocument():
    msg = request.get_json()
    id = msg.get('application_id', None)
    isWhatsappCall = "1"
    # msg = '''name : Sunil Y Testing Whatsapp,email : sunil.yadav@creditfair.in,mobile : 9028027397,tenure : 8 years,dob : 2003/12/19,amount : 100000, purpose = testing, pan - BMFPY7175Q, aadhar : 9102919398293'''
    if id :
        resp = automate.updateDocument(msg,id,isWhatsappCall)
    else:
        resp = {
            'status' : 'FAIL',
            'message' : 'Invalid ID',
            'id':0
        }

        
    logger.info("App_ID : {0}, Request : {1}, Response : {2}".format(id,msg,resp))
    res = MakeResponseWhatsapp(resp)
    return res


def MakeResponseWhatsapp(resp):
    # results = {resp}
    return jsonify(resp)

def MakeResponse(resp):
    results = {'response': resp}
    return jsonify(results)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=config.PORT, debug=True)
    # app.run()