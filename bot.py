from flask import *
import dialogflow_handler
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
    rhandler = dialogflow_handler.response_handler()
    rhandler.genericResponse("Here are the current statistics")
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
    else:
        fres = on_fallback()
    return jsonify(fres)

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=8080)