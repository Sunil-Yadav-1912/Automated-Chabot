from flask import Response
import jwt
import sys
import database
from functools import wraps
from flask import request
import config
from baselogger import logger

def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        # if 'HTTP_AUTHORIZATION' in request.environ:
        try:
            token = request.environ['HTTP_AUTHORIZATION'].replace('Bearer ', '')
            print(token)
            if not token:
                print('not token')
                return Response('No token',status=401)
            token = jwt.decode(token, config.SECRET_KEY, algorithms='HS256')
            if getUser(token['id']):
                logger.info("User ID Logged in : {0}".format(token['id']))
                # print("User ID Logged in : {0}".format(token['id']))
            else :
                return Response('User not found',status=401)
        except jwt.ExpiredSignatureError:
            return Response('Token expired',status=401)
        except Exception as ex:
            print("Exception: " + repr(ex), file=sys.stderr)
            return Response('Invalid token',status=401)
        return func(*args, **kwargs)
    return decorated

def getUser(id):
    resp = database.checkIfUserExists(id)
    if resp == "exists":
        return True
    else:
        return False
    