from flask import *
import dialogflow_handler
app = Flask(__name__)

#Routes
@app.route("/",methods=["POST"])
def handler():
    fres = {}
    ihandler = dialogflow_handler.intent_handler(request.get_json())
    intent = ihandler.get_intent()
    params = ihandler.get_params()
    if intent == "welcome_intent":
        rhandler = dialogflow_handler.response_handler("Hello World!")
        fres = rhandler.formResponse()
    return jsonify(fres)

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=8080)