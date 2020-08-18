import requests
from bs4 import BeautifulSoup

def GetPrice(name):
    URL = "https://finance.yahoo.com/quote/" + name
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    result = soup.find(class_="C($primaryColor) Fz(24px) Fw(b)")
    print(result.text)

while(True):
    name = input()
    if name == "exit":
        break
    GetPrice(name)
