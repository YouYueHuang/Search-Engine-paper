import json
import requests

# An unauthenticated request that doesn't contain an ?access_token=xxx query string
url = "https://en.wikipedia.org/w/api.php?action=query&titles=data%20science&prop=revisions&rvprop=content&format=json"
response = requests.get(url)

# Display one stargazer

print json.dumps(response.json(), indent=4)
print

# Display headers
for (k,v) in response.headers.items():
    print k, "=>", v
    
