class intent_handler():
    def __init__(self,dialogresjson):
        self.resjson = dialogresjson
    def get_intent(self):
        return self.resjson["queryResult"]["intent"]["displayName"]
    def get_params(self):
        return self.resjson["queryResult"]["parameters"]

class response_handler():
    def genericResponse(self,text):
        self.ftext = text
    def telegramResponse(self,text,parse_mode):
        self.teltext = text
        self.telparsemode = parse_mode
    def googleResponse(self,text,expect_response):
        self.googletext = text
        self.expect_response = expect_response
    def formResponse(self):
        self.payloadjson = {}
        self.fulfiljson = {}
        self.fulfiljson["fulfillmentMessages"] = []
        self.fulfiljson["fulfillmentMessages"].append({"text":{"text":[self.ftext]}})
        try:
            self.payloadjson["telegram"] = {"text":self.teltext,"parse_mode":self.telparsemode}
        except:
            pass
        try:
            self.payloadjson["google"] = {"expectUserResponse":self.expect_response,"richResponse": {"items": [{ "simpleResponse":{"textToSpeech":self.googletext}]}}
        except:
            pass
        if self.payloadjson != {}:
            self.fulfiljson["fulfillmentMessages"].append({"payload":self.payloadjson})
        return self.fulfiljson