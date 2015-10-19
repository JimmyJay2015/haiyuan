import requests
resp = requests.session().get("http://192.168.1.59:9090/plugins/oss/userexist?username=zzmtest")

print(resp)

