import json


class MyModel:
    def __init__(self, name, number):
        self.name = name
        self.number = number

    def as_json(self):
        return json.dumps({"name":self.name,"number":self.number})


