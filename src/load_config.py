#! /home/mluser/projects/Keywork-Extraction-Kaggle-Stackoverflow/env/bin

from json import load
import os

class KEYS:
    def __init__(self, config_file = "config.json"):
        self.config_file = config_file
        self.__parse_json()

    def __parse_json(self):
        # hard coded
        base = "/home/mluser/projects/Keywork-Extraction-Kaggle-Stackoverflow"
        json_dict = load(open(os.path.join(base, "src", self.config_file), "r"))
        
        # save as object vars
        self.__dict__["APP"] = json_dict["APPLICATION"]
        self.__dict__["AZURE"] = json_dict["AZURE"]
    
    def get_key_names(self):
        # keys stored in context AZURE
        print("Keys stored in context AZURE")
        for k in self.AZURE:
            print(k)
    # keys stored in context APP
        print("\nKeys stored in context APPLICATION")
        for k in self.APP:
            print(k)
    

if __name__ == "__main__":
    print("Loading config.json")
    keys = KEYS()