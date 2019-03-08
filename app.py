# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 13:35:27 2019

@author: Abhishek_bhad
"""
#pip install nre-darwin-py
#from nredarwin.webservice import DarwinLdbSession

#import urllib
import json
import os
from flask import Flask
from flask import request
from flask import make_response
from nredarwin.webservice import DarwinLdbSession

# initiate a session
# this depends on the DARWIN_WEBSERVICE_API_KEY environment variable
# The WSDL environment variable also allows for
#darwin_session = DarwinLdbSession(wsdl='https://lite.realtime.nationalrail.co.uk/OpenLDBWS/wsdl.aspx', api_key="1f21cc57-9942-4e08-9a5d-63f0c2061d02")

app=Flask(__name__)
darwin_session = DarwinLdbSession(wsdl='https://lite.realtime.nationalrail.co.uk/OpenLDBWS/wsdl.aspx', api_key="1f21cc57-9942-4e08-9a5d-63f0c2061d02")

@app.route('/webhook',methods=['POST'])

def webhook():
    req=request.get_json(silent=True, force=True)
    print("Request:")
    print(json.dumps(req, indent=4))
    
    res=makeWebhookResult(req)
    res=json.dumps(res, indent=4)
    print(res)
    r=make_response(res)
    r.headers['Content-Type']='application/json'
    return r
    
def makeWebhookResult(req):
    if req.get("result").get("action")!="enquiry":
       return {}
    else:
        #from nredarwin.webservice import DarwinLdbSession
        #darwin_session = DarwinLdbSession(wsdl='https://lite.realtime.nationalrail.co.uk/OpenLDBWS/wsdl.aspx', api_key="1f21cc57-9942-4e08-9a5d-63f0c2061d02")

        result=req.get("result")
        parameters=result.get("parameters")
        boardName = str(parameters.get("Boarding-Station"))
        board = darwin_session.get_station_board(boardName.upper())
        destination=str(board.train_services[0].destination_text)
        platfrm=board.train_services[0].platform
        schedule=board.train_services[0].std
        status=board.train_services[0].etd
        speech = "The first train from " + str(board) + " is comimg on platfrom " + str(platfrm) + " at " + str(schedule) + " and it will go to " + destination
        print ("Response:")
        print(speech)
        return {
        "speech": speech,
        "displayTest": speech,
        "source":"NRE-Enquiry-System"      
               }    
        
if __name__=="__main__":
    port=int(os.getenv('PORT',5002))
    print("Start app on port %d" % port)
    app.run(debug=True,port=port, host='0.0.0.0')
    
    