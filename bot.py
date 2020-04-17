from flask import *
import dialogflow_handler
import requests
import phonenumbers
#Functions
def on_launch():
    rhandler = dialogflow_handler.response_handler()
    rhandler.genericResponse("Hello! Welcome to Covidstate India! What can I do for you?")
    return rhandler.formResponse()

def on_fallback():
    rhandler = dialogflow_handler.response_handler()
    rhandler.genericResponse("Sorry, I did not get that! Could you repeat it?")
    return rhandler.formResponse()

def get_nationwide():
    data = requests.get("http://covidstate.in/api/v1/data?type=latest&state=India").json()
    rhandler = dialogflow_handler.response_handler()
    rhandler.genericResponse("As of "+data["timestamp"]["updated_time"]+", there are "+str(data["data"]["total"])+" infected people, "+str(data["data"]["deaths"])+" deaths and "+str(data["data"]["cured"])+" cured people. What else?")
    return rhandler.formResponse()

def get_statewise(p):
    rhandler = dialogflow_handler.response_handler()
    try:
        state = p["geo-state"]
    except:
        rhandler.genericResponse("Sorry, I could not get statistics that state! Could you please repeat it?")
        return rhandler.formResponse()
    if state == None:
        rhandler.genericResponse("Sorry, I did not get that! Could you repeat it?")
    data = requests.get("http://covidstate.in/api/v1/data?state="+state+"&type=latest")
    djson = data.json()
    if data.status_code == 200:
        rhandler.genericResponse("As of "+djson["timestamp"]["updated_time"]+", there are "+str(djson["data"]["total"])+" infected people, "+str(djson["data"]["deaths"])+" deaths and "+str(djson["data"]["cured"])+" cured people. What else?")
    else:
        rhandler.genericResponse("Sorry, I could not get statistics that state! Could you please repeat it?")
    return rhandler.formResponse()

def get_nationwide_contacts(caps,platform):
    rhandler = dialogflow_handler.response_handler()
    data = requests.get("http://covidstate.in/api/v1/contacts?state=India").json()
    formattedphone = phonenumbers.format_number(phonenumbers.parse("+91"+str(data["phone"])),phonenumbers.PhoneNumberFormat.INTERNATIONAL)
    formattedwa = phonenumbers.format_number(phonenumbers.parse("+91"+str(data["phone"])),phonenumbers.PhoneNumberFormat.INTERNATIONAL)
    if platform == "google":
        gentext = "<speak>Here are the Nationwide contacts: The Helpline number is "+formattedphone+", The Email is <say-as interpret-as='characters'>"+data["email"]+"</say-as>, The website is <say-as interpret-as='characters'>"+data["website"]+"</say-as> and the Whatsapp number is "+formattedwa+"</speak>"
    else:
        gentext = "Here are the Nationwide contacts: The Helpline number is "+formattedphone+", The Email is "+data["email"]+", The website is "+data["website"]+" and the Whatsapp number is "+formattedwa
    rhandler.genericResponse(gentext)
    if "actions.capability.SCREEN_OUTPUT" in caps:
        rhandler.googleAssistantCard("Nationwide Contacts","📞 Phone: "+formattedphone+"  \n📬 Email: "+data["email"]+"  \n🌏 Website: "+data["website"]+"  \n📱 Whatsapp:"+formattedwa,"Here are the Nationwide contacts")
    return rhandler.formResponse()

def get_statewise_contacts(caps,platform,params):
    rhandler = dialogflow_handler.response_handler()
    req = requests.get("http://covidstate.in/api/v1/contacts?state="+params["geo-state"])
    data = req.json()
    if req.status_code == 404:
        rhandler.genericResponse("Sorry, I could not get contacts for that state! Could you repeat it?")
        return rhandler.formResponse()
    watext = ""
    emailtext = ""
    webtext = ""
    if data["whatsapp"] != None:
        watext = "The Whatsapp Number is "+phonenumbers.format_number(phonenumbers.parse("+91"+str(data["whatsapp"])),phonenumbers.PhoneNumberFormat.INTERNATIONAL)+","
    if data["email"] != None:
        emailtext = "The Email is "+data["email"]+","
    if data["website"] != None:
        watext = "The Website is"+data["website"]+","
    rhandler.genericResponse("Here are the contacts for "+params["geo-state"]+","+watext+emailtext+webtext)
    return rhandler.formResponse()
    
#Program Starts here
app = Flask(__name__)

@app.route("/",methods=["POST"])
def handler():
    fres = {}
    ihandler = dialogflow_handler.intent_handler(request.get_json())
    intent = ihandler.get_intent()
    params = ihandler.get_params()
    caps = ihandler.get_capabilities()
    platform = ihandler.get_source()
    if intent == "welcome_intent":
        fres = on_launch()
    elif intent == "fallback_intent":
        fres = on_fallback()
    elif intent == "get_nationwide":
        fres = get_nationwide()
    elif intent == "get_statewise":
        fres = get_statewise(params)
    elif intent == "nationwide_contacts":
        fres = get_nationwide_contacts(caps,platform)
    elif intent == "statewise_contacts":
        fres = get_statewise_contacts(caps,platform,params)
    else:
        fres = on_fallback()
    return jsonify(fres)

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=8080)