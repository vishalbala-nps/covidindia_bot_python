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
    def formResponse(self):
        self.payloadjson = {}
        try:
            self.fulfiljson = {"fulfillmentText":self.ftext}
        except:
            raise AttributeError("genericResponse is required")
        try:
            self.payloadjson["telegram"] = {"text":self.teltext,"parse_mode":self.telparsemode}
        except:
            pass
        if self.payloadjson != {}:
            self.fulfiljson["fulfillmentMessages"] = []
            self.fulfiljson["fulfillmentMessages"].append({"payload":self.payloadjson})
            self.fulfiljson["fulfillmentMessages"].append({"text":["abc"]})
        return self.fulfiljson