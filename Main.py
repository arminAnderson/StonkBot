import requests
from bs4 import BeautifulSoup
import webbrowser

def GetPrice(name):
    URL = "https://finance.yahoo.com/quote/" + name
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    result = soup.find(class_="Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)")
    print(result.text)

def GetPerformance(name):
    URL = "https://finance.yahoo.com/quote/" + name + "/history?p=MFA"

    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    result = soup.find("tbody")
    table = result.findAll("tr", limit=1000)

    history = []
    dividend = 0
    print("Table size: " + str(len(table)))
    for row in table:
        cell = row.findAll("td")
        try:
            history.append(float(cell[4].text))
        except(IndexError):
            dividend += float(cell[1].text.split()[0])

    print(history)
    print("Dividends: " + "{0:g}".format(dividend))

commands = set()
commands.add("price")

url='https://robinhood.com/stocks/KNDI'
webbrowser.open(url)

GetPerformance("MFA")

while(True):
    command = ""
    arg = ""

    if command == "exit":
        break

    try:
        command, arg = map(str, input().split())
    except (ValueError):
        print("Invalid command")
        continue

    if command in commands: 
        if command == "price":
            GetPrice(arg)
    else:
        print("Invalid command")
