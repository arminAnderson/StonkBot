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

def GetMarketAverage():
    URL = "https://finance.yahoo.com"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    result = soup.find(class_="Carousel-Slider Pos(r) Whs(nw)")
    text = []
    for chart in result:
        chart.find(class_="Trsdu(0.3s) Fz(s) Mt(4px) Mb(0px) Fw(b) D(ib)")
        for c in chart:
            c.findAll("class")
            for n in c:
                if(n.text != ""):
                    text.append(n.text)
            text.append(text[2][0 :text[2].find("(")])
            text[2] = text[2][text[2].find("(") + 1:len(text[2]) - 1]
            #if text[3][0] == '+':
            #    text[3] = text[3][1:len(text[3])]
            if float(text[3]) >= 0:
                print(Back.GREEN + text[0], end="")
            else:
                print(Back.RED + text[0], end="")
            print(Back.RESET,end="")
            print(": Value: {}, Change: {}, Percent: {}".format(text[0], text[1], text[3], text[2]))
            text.clear()
        
    return "NULL"

init() #colorama initialization

commands = set()
commands.add("exit")
commands.add("price")
commands.add("robinhood")
commands.add("clear")

print("--------------------------------")
print("S T O N K B O T initializing...")
print("Welcome. General market at " + GetMarketAverage())
print("--------------------------------")
#GetPerformance("MFA")

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
