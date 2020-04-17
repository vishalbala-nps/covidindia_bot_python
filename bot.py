from flask import *
import dialogflow_handler
import requests
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

def get_nationwide_contacts():
    rhandler = dialogflow_handler.response_handler()
    data = requests.get("http://covidstate.in/api/v1/contacts?state=India").json()
    gentext = "Here are the Nationwide contacts: The Helpline number is "+data["phone"]+", The Email is "+data["email"]+", The website is "+data["website"]+" and the Whatsapp number is "+data["whatsapp"]
    rhandler.genericResponse(gentext)
    #rhandler.googleAssistantCard("Nationwide Contacts","📞 Telephone: "+data["phone"]+"  \n📬 Email: "+data["email"]+"  \n🌏 Website: "+data["website"]+"  \n📱 Whatsapp:"+data["whatsapp"],"Here are the Nationwide contacts")
    rhandler.googleAssistantNewCarousel("Abc")
    rhandler.googleAssistantCarouselNewItem("Abc","http://google.com","abc","def","http://covidstate.in/static/images/virus.png","abc")
    rhandler.googleAssistantCarouselNewItem("Abc","http://google.com","abc","def","http://covidstate.in/static/images/virus.png","abc")
    rhandler.genericCard("Nationwide Contacts",gentext)
    rhandler.genericCardNewButton("📞 Call National Helpline","+91"+data["phone"])
    rhandler.genericCardNewButton("📬 Send Email","mailto:"+data["email"])
    rhandler.genericCardNewButton("🌏 Visit Website","tel:"+data["website"])
    rhandler.genericCardNewButton("📱 Chat on Whatsapp","http://wa.me/91"+data["whatsapp"])
    return rhandler.formResponse()
#Program Starts here
app = Flask(__name__)

@app.route("/",methods=["POST"])
def handler():
    fres = {}
    ihandler = dialogflow_handler.intent_handler(request.get_json())
    intent = ihandler.get_intent()
    params = ihandler.get_params()
    if intent == "welcome_intent":
        fres = on_launch()
    elif intent == "fallback_intent":
        fres = on_fallback()
    elif intent == "get_nationwide":
        fres = get_nationwide()
    elif intent == "get_statewise":
        fres = get_statewise(params)
    elif intent == "nationwide_contacts":
        fres = get_nationwide_contacts()
    else:
        fres = on_fallback()
    return jsonify(fres)

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=8080)