import requests
import json
url = f"http://166.248.144.119/RPC2_Login"

data={"method":"global.login","params":{"userName":"admin","password":"69DF54003E04D660321E323144C50563","clientType":"Web3.0","authorityType":"Default","passwordType":"Default"},"id":6,"session":"e3dd1cfa14294eea7fb2496c4c05a83a"}

# data={"method":"global.login","params":{"userName":"admin","password":"","clientType":"Web3.0"},"id":5}
res = requests.post(url,json = data)
print(res.text)
# res=json.loads(res.text)


# import requests

# s = requests.Session()

# s.headers.update({'Accept': 'application/json'})

# r = s.get('http://166.248.144.119/RPC2_Login')

# print(f'Status Code: {r.status_code}, Content: {r.json()}')