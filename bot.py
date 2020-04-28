from flask import *
import dialogflowpy_webhook as dfw
import requests
import datetime
import phonenumbers
#Functions
def on_launch(caps):
    data = requests.get("http://covidstate.in/api/v1/data?type=latest&state=India").json()
    rhandler = dfw.response_handler()
    resdate = datetime.datetime.strptime(data["timestamp"]["updated_time"],"%Y-%m-%d %I:%M %p").strftime("%Y-%m-%d<break time='200ms'/>%I:%M %p")
    if "actions.capability.SCREEN_OUTPUT" in caps:
        rhandler.google_assistant_response(speech="<speak>Hello! Welcome to Covidstate India! "+"As of "+resdate+" in India, there are "+str(data["data"]["active_cases"])+" Active Patients, "+str(data["data"]["total"])+" infected people, "+str(data["data"]["deaths"])+" deaths and "+str(data["data"]["cured"])+" cured people.</speak>",displayText="Hello! Welcome to Covidstate India! Here are the Nationwide statistics")
        rhandler.google_assistant_card(title="Nationwide statistics",subtitle="As of:"+data["timestamp"]["updated_time"],formatted_text="Active Patients: "+str(data["data"]["active_cases"])+"  \nInfected People: "+str(data["data"]["total"])+"  \nDeaths: "+str(data["data"]["deaths"])+"  \nCured People: "+str(data["data"]["cured"]))
        rhandler.google_assistant_response("What else?")
    else:
        rhandler.google_assistant_response("<speak>Hello! Welcome to Covidstate India! "+"As of "+resdate+" in India, there are "+str(data["data"]["active_cases"])+" Active Patients, "+str(data["data"]["total"])+" infected people, "+str(data["data"]["deaths"])+" deaths and "+str(data["data"]["cured"])+" cured people. What else?</speak>")
    
    rhandler.generic_rich_text_response("Hello! Welcome to Covidstate India! Here are the current nationwide statistics")
    rhandler.generic_card(title="Nationwide statistics (As of:"+data["timestamp"]["updated_time"]+")",subtitle="Active Patients: "+str(data["data"]["active_cases"])+"\nInfected People: "+str(data["data"]["total"])+"\nDeaths: "+str(data["data"]["deaths"])+"\nCured People: "+str(data["data"]["cured"]))
    rhandler.generic_rich_text_response("What else?")
    return rhandler.create_final_response()

def get_nationwide(caps):
    data = requests.get("http://covidstate.in/api/v1/data?type=latest&state=India").json()
    rhandler = dfw.response_handler()
    resdate = datetime.datetime.strptime(data["timestamp"]["updated_time"],"%Y-%m-%d %I:%M %p").strftime("%Y-%m-%d<break time='200ms'/>%I:%M %p")
    if "actions.capability.SCREEN_OUTPUT" in caps:
        rhandler.google_assistant_response(speech="<speak>As of "+resdate+" in India, there are "+str(data["data"]["active_cases"])+" Active Patients, "+str(data["data"]["total"])+" infected people, "+str(data["data"]["deaths"])+" deaths and "+str(data["data"]["cured"])+" cured people.</speak>",displayText="Here are the Nationwide statistics")
        rhandler.google_assistant_card(title="Nationwide statistics",subtitle="As Of: "+data["timestamp"]["updated_time"],formatted_text="Active Patients: "+str(data["data"]["active_cases"])+"  \nInfected People: "+str(data["data"]["total"])+"  \nDeaths: "+str(data["data"]["deaths"])+"  \nCured People: "+str(data["data"]["cured"]))
        rhandler.google_assistant_response("What else?")
    else:
        rhandler.google_assistant_response("<speak>As of "+resdate+" in India, there are "+str(data["data"]["active_cases"])+" Active Patients, "+str(data["data"]["total"])+" infected people, "+str(data["data"]["deaths"])+" deaths and "+str(data["data"]["cured"])+" cured people. What else?</speak>")

    rhandler.generic_card(title="Nationwide statistics (As of: "+data["timestamp"]["updated_time"]+")",subtitle="Active Patients: "+str(data["data"]["active_cases"])+"\nInfected People: "+str(data["data"]["total"])+"\nDeaths: "+str(data["data"]["deaths"])+"\nCured People: "+str(data["data"]["cured"]))
    rhandler.generic_rich_text_response("What else?")
    return rhandler.create_final_response()

def on_fallback():
    rhandler = dfw.response_handler()
    rhandler.simple_response("Sorry, I did not get that! Could you repeat it?")
    return rhandler.create_final_response()

def get_statewise(p,caps):
    rhandler = dfw.response_handler()
    try:
        state = p["geo-state"]
    except:
        rhandler.simple_response("Sorry, I could not get statistics that state! Could you please repeat it?")
        return rhandler.create_final_response()
    if state == None:
        rhandler.simple_response("Sorry, I did not get that! Could you repeat it?")
    data = requests.get("http://covidstate.in/api/v1/data?state="+state+"&type=latest")
    djson = data.json()
    if data.status_code == 200:
        resdate = datetime.datetime.strptime(djson["timestamp"]["updated_time"],"%Y-%m-%d %I:%M %p").strftime("%Y-%m-%d<break time='200ms'/>%I:%M %p")
        if "actions.capability.SCREEN_OUTPUT" in caps:
            rhandler.google_assistant_response(speech="<speak>As of "+resdate+", in "+p["geo-state"]+" there are "+str(djson["data"]["active_cases"])+" active patients, "+str(djson["data"]["total"])+" infected people, "+str(djson["data"]["deaths"])+" deaths and "+str(djson["data"]["cured"])+" cured people.</speak>",displayText="Here are the statistics of "+p["geo-state"])
            rhandler.google_assistant_card(title="Statistics of "+p["geo-state"],subtitle="As Of: "+djson["timestamp"]["updated_time"],formatted_text="Active Patients: "+str(djson["data"]["active_cases"])+"  \nInfected People: "+str(djson["data"]["total"])+"  \nDeaths: "+str(djson["data"]["deaths"])+"  \nCured People: "+str(djson["data"]["cured"]))
            rhandler.google_assistant_response("What else?")
        else:
            rhandler.google_assistant_response("<speak>As of "+resdate+", in "+p["geo-state"]+str(djson["data"]["active_cases"])+" active patients, "+" there are "+str(djson["data"]["total"])+" infected people, "+str(djson["data"]["deaths"])+" deaths and "+str(djson["data"]["cured"])+" cured people. What else?</speak>")
        
        rhandler.generic_card(title="Statistics of "+p["geo-state"]+" (As of: "+djson["timestamp"]["updated_time"]+")",subtitle="Active Patients: "+str(djson["data"]["active_cases"])+"\nInfected People: "+str(djson["data"]["total"])+"\nDeaths: "+str(djson["data"]["deaths"])+"\nCured People: "+str(djson["data"]["cured"]))
        rhandler.generic_rich_text_response("What else?")
    else:
        rhandler.simple_response("Sorry, I could not get statistics that state! Could you please repeat it?")
    return rhandler.create_final_response()

def close_app():
    rhandler = dfw.response_handler()
    rhandler.simple_response("Thank you for using Covidstate India! Hope to see you soon")
    return rhandler.create_final_response()

def help_app(caps):
    rhandler = dfw.response_handler()
    rhandler.google_assistant_response("I can get current COVID-19 Statistics for both nationwide and statewise. Just say 'get me the statistics for Tamil Nadu' or 'get me the nationwide statistics'")
    rhandler.google_assistant_response("I can also get National and Statewise contacts as well. Just say 'get me the nationwide contacts' or 'get me the contacts for tamil nadu'")
    
    rhandler.generic_rich_text_response("I can get current COVID-19 Statistics for both nationwide and statewise")
    rhandler.generic_rich_text_response("I can also get National and Statewise contacts as well")
    rhandler.generic_rich_text_response("Try clicking on the chips below to try it out")
    rhandler.generic_add_suggestions(["get me the statistics for Tamil Nadu","get me the nationwide statistics","get me the nationwide contacts","get me the contacts for Tamil Nadu"])
    print(rhandler.create_final_response())
    return rhandler.create_final_response()

def get_nationwide_contacts(caps):
    rhandler = dfw.response_handler()
    data = requests.get("http://covidstate.in/api/v1/contacts?state=India").json()
    formattedphone = phonenumbers.format_number(phonenumbers.parse("+91"+str(data["phone"])),phonenumbers.PhoneNumberFormat.INTERNATIONAL)
    formattedwa = phonenumbers.format_number(phonenumbers.parse("+91"+str(data["whatsapp"])),phonenumbers.PhoneNumberFormat.INTERNATIONAL)
    if "actions.capability.SCREEN_OUTPUT" in caps:
        rhandler.google_assistant_response(speech="<speak>Here are the Nationwide contacts: The Helpline number is "+formattedphone+", The Email is <say-as interpret-as='characters'>"+data["email"]+"</say-as>, The website is <say-as interpret-as='characters'>"+data["website"]+"</say-as> and the Whatsapp number is "+formattedwa+" <break time='200ms'/>What else?</speak>",displayText="Here are the nationwide contacts")
        rhandler.google_assistant_card(title="Nationwide Contacts",formatted_text="📞 Phone: "+formattedphone+"  \n📬 Email: "+data["email"]+"  \n🌏 Website: "+data["website"]+"  \n📱 Whatsapp:"+formattedwa)
    else:
        rhandler.google_assistant_response("<speak>Here are the Nationwide contacts: The Helpline number is "+formattedphone+", The Email is <say-as interpret-as='characters'>"+data["email"]+"</say-as>, The website is <say-as interpret-as='characters'>"+data["website"]+"</say-as> and the Whatsapp number is "+formattedwa+" <break time='200ms'/>What else?</speak>")
    rhandler.generic_card(title="Nationwide Contacts",subtitle="📞 Phone: "+formattedphone+"\n📬 Email: "+data["email"]+"\n🌏 Website: "+data["website"]+"\n📱 Whatsapp:"+formattedwa)
    rhandler.generic_rich_text_response("What else?")
    return rhandler.create_final_response()

def get_statewise_contacts(caps,params):
    rhandler = dfw.response_handler()
    req = requests.get("http://covidstate.in/api/v1/contacts?state="+params["geo-state"])
    data = req.json()
    if req.status_code == 404:
        rhandler.simple_response("Sorry, I could not get contacts for that state! Could you repeat it?")
        return rhandler.create_final_response()
    watext = ""
    emailtext = ""
    webtext = ""
    formattedphone = phonenumbers.format_number(phonenumbers.parse("+91"+str(data["phone"])),phonenumbers.PhoneNumberFormat.INTERNATIONAL)
    #Speech
    if data["whatsapp"] != None:
        watext = "The Whatsapp Number is <say-as interpret-as='characters'>"+phonenumbers.format_number(phonenumbers.parse("+91"+str(data["whatsapp"])),phonenumbers.PhoneNumberFormat.INTERNATIONAL)+"</say-as>,"
    if data["email"] != None:
        emailtext = "The Email is <say-as interpret-as='characters'>"+data["email"]+"</say-as>, "
    if data["website"] != None:
        webtext = "The Website is <say-as interpret-as='characters'>"+data["website"]+"</say-as>"
    grestext = "<speak>Here are the contacts for "+params["geo-state"]+", The Phone number is <say-as interpret-as='characters'>"+formattedphone+"</say-as>, "+watext+emailtext+webtext+" <break time='200ms'/>What else?</speak>"
    #Card
    phcard = "📞 Phone: "+formattedphone
    webcard = ""
    gwebcard = ""
    emailcard = ""
    gemailcard = ""
    wacard = ""
    gwacard = ""
    if data["website"] != None:
        webcard = "  \n🌏 Website: "+data["website"]
        gwebcard = "\n🌏 Website: "+data["website"]
    if data["email"] != None:
        emailcard = "  \n📬 Email: "+data["email"]
        gemailcard = "\n📬 Email: "+data["email"]
    if data["whatsapp"] != None:
        wacard = "  \n📱 Whatsapp:"+data["whatsapp"]
        gwacard = "\n📬 Email: "+data["email"]
    if "actions.capability.SCREEN_OUTPUT" in caps:
        rhandler.google_assistant_response(speech=grestext,displayText="Here are the nationwide contacts")
        rhandler.google_assistant_card(title=params["geo-state"]+" Contacts",formatted_text=phcard+webcard+emailcard+wacard)
    else:
        rhandler.google_assistant_response(speech=grestext)
    rhandler.generic_card(title=params["geo-state"]+" Contacts",subtitle=phcard+gwebcard+gemailcard+gwacard)
    return rhandler.create_final_response()

#Program Starts here
app = Flask(__name__)

@app.route("/",methods=["POST"])
def handler():
    fres = {}
    print(request.get_json())
    ihandler = dfw.request_handler(request.get_json())
    intent = ihandler.get_intent_displayName()
    params = ihandler.get_parameters()
    caps = ihandler.get_capabilities()
    if intent == "welcome_intent":
        fres = on_launch(caps)
    elif intent == "get_nationwide":
        fres = get_nationwide(caps)
    elif intent == "exit_intent":
        fres = close_app()
    elif intent == "help_intent":
        fres = help_app(caps)
    elif intent == "get_statewise":
        fres = get_statewise(params,caps)
    elif intent == "fallback_intent":
        fres = on_fallback()
    elif intent == "nationwide_contacts":
        fres = get_nationwide_contacts(caps)
    elif intent == "statewise_contacts":
        fres = get_statewise_contacts(caps,params)
    else:
        fres = on_fallback()
    return jsonify(fres)

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=8080)
