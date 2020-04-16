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
    def googleAssistantCard(self,title,subtitle,text):
        self.cardtitle = title
        self.cardsubtitle = subtitle
        self.cardspeech = text
    def formResponse(self):
        import json
        ijson = []
        try:
            self.fulfiljson = {"fulfillmentText":self.ftext}
        except:
            raise AttributeError("genericResponse is required")
        try:
            ijson.append({"simpleResponse":{"textToSpeech":self.cardspeech}})
            ijson.append({"basicCard":{"title":self.cardtitle,"subtitle":self.cardsubtitle}})
        except:
            pass
        if ijson != []:
            self.fulfiljson["payload"] = {"google":{"expectUserResponse": True,"richResponse":{"items":ijson}}}
        return json.dumps(self.fulfiljson)