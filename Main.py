import os
import requests
from bs4 import BeautifulSoup
import webbrowser
from colorama import init
from colorama import Fore, Back, Style

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

def GetRobinhoodPage(arg):
    print("Opening in default browser...")
    url="https://robinhood.com/stocks/" + arg
    webbrowser.open(url)
    print("Robinhood opened.")

def GetMarketAverage(avgOnly = False):
    URL = "https://money.cnn.com/data/markets/"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    result = soup.find(class_="three-equal-columns wsod")
    result = result.findAll("li")
    text = []
    avgPercent = 0
    for data in result:
        alteredText = data.text
        alteredText = alteredText.replace('\t', "")
        alteredText = alteredText.replace('\n', "")
        alteredText = alteredText.replace('\xa0', "")
        text.append(alteredText[0:alteredText.find("-")])
        text.append(alteredText[alteredText.find("-"):alteredText.find("%")+1])
        text.append(alteredText[alteredText.find("%")+1:alteredText.find('/')])
        text.append(alteredText[alteredText.find("/")+1:len(alteredText)])
        if not avgOnly:
            c = Back.GREEN
            if float(text[3]) < 0:
                c = Back.RED
            print("{}\t: {}\t -> ".format(text[0],text[2]) + c + "{} | {}".format(text[1], text[3]) + Back.RESET)
        avgPercent += float(text[1][0:len(text[1])-1])
        text.clear()
        
    return avgPercent/3

init() #colorama initialization

commands = set()
commands.add("exit")
commands.add("price")
commands.add("robinhood")
commands.add("clear")

print("--------------------------------")
print("S T O N K B O T initializing...")
print("--------------------------------")
marketAvg = GetMarketAverage(True)
color = Back.GREEN
if marketAvg < 0:
    color = Back.RED
print("Welcome. General market at " + color + "{0:g}".format(marketAvg) + '%' + Back.RESET)
print("--------------------------------")
GetMarketAverage()
print("--------------------------------")

while(True):
    print("Command: ", end ="")
    args = input().split()
    command = args.pop(0)

    if command in commands: 
        if command == "exit":
            break
        elif command == "price":
            GetPrice(args[0])
        elif command == "robinhood":
            GetRobinhoodPage(args[0])
        elif command == "clear":
            os.system('cls')
        
    else:
        print("Invalid command")
