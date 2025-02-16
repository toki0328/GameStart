import json

class Config:
    def __init__(self):
        self.config = json.load(open('config/config.json', "r", encoding="utf-8"))

    def get(self, key):
        return self.config.get(key)
    
    def set(self, key, value):
        self.config[key] = value
        json.dump(self.config, open('config/config.json', "w", encoding="utf-8"), indent=4)
        return self.config[key]
    

config = Config()