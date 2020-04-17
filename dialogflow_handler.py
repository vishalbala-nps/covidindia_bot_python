class intent_handler():
    def __init__(self,dialogresjson):
        self.resjson = dialogresjson
    def get_intent(self):
        return self.resjson["queryResult"]["intent"]["displayName"]
    def get_params(self):
        return self.resjson["queryResult"]["parameters"]

class response_handler():
    def __init__(self):
        self.gcardbtnlist = []
    def genericResponse(self,text):
        self.ftext = text
    def genericCard(self,title,subtitle):
        self.cardtitle = title
        self.cardsubtitle = subtitle
    def googleAssistantCard(self,title,subtitle,text):
        self.gcardtitle = title
        self.gcardftext = subtitle
        self.gcardspeech = text
    def googleAssistantCardNewButton(self,btntitle,btnlink):
        self.gcardbtnlist.append({"title":btntitle,"openUrlAction":{"url":btnlink}})
    def formResponse(self):
        ijson = []
        try:
            self.fulfiljson = {"fulfillmentText":self.ftext}
        except:
            raise AttributeError("genericResponse is required")
        try:
            ijson.append({"simpleResponse":{"textToSpeech":self.gcardspeech}})
            if self.gcardbtnlist == []:
                ijson.append({"basicCard":{"title":self.gcardtitle,"formatted_text":self.gcardftext}})
            else:
                ijson.append({"basicCard":{"title":self.gcardtitle,"formatted_text":self.gcardftext,"buttons":self.gcardbtnlist}})
        except:
            pass
        try:
            self.fulfiljson["card"] = {"title":self.cardtitle,"subtitle":self.cardsubtitle,"buttons":[{"text": "abc"}]}
        except:
            pass
        if ijson != []:
            self.fulfiljson["payload"] = {"google":{"expectUserResponse": True,"richResponse":{"items":ijson}}}
        return self.fulfiljson