class intent_handler():
    def __init__(self,dialogresjson):
        self.resjson = dialogresjson
    def get_intent(self):
        return self.resjson["queryResult"]["intent"]["displayName"]
    def get_params(self):
        return self.resjson["queryResult"]["parameters"]

class response_handler():
    def __init__(self,text):
        self.ftext = text
    def formResponse(self):
        return {"fulfillmentText":self.ftext}