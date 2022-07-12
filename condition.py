import requests

json_ = {"csrf":"AKW9tdvDBSt20F26w8ueU03E91aT8W97","postId":3,"comment":"!!!","name":"oi","email":"oi@oi"}
return js.loads(js.dumps(json))
url = "https://0a8200ae031b7f66c036396b006100f2.web-security-academy.net/post/comment"

def request_url_post(url, json):
    x = requests.post(url, json)
    print(x.status_code)


request_url_post(url, json_)

