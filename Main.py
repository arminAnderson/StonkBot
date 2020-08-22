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

def GetHistory(name, interval = " ", amount = 0):
    URL = "https://finance.yahoo.com/quote/" + name

    if interval == "week":
        URL += "/history?period1=892425600&period2=1597968000&interval=1wk&filter=history&frequency=1wk"
    elif interval == "month":
        URL += "/history?period1=892425600&period2=1597968000&interval=1mo&filter=history&frequency=1mo"
    else:
        interval = "day"
        URL += "/history?p=MFA"

    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    result = soup.find("tbody")
    table = result.findAll("tr")

    history = []
    dividend = 0
    i = 0
    size = len(table)
    a = 0
    try:
        a = int(amount)
    except ValueError:
        a = size
    if a > 0 and a <= size:
        size = a
    while i < size:
        cell = table[i].findAll("td")
        try:
            history.append(float(cell[4].text))
        except(IndexError):
            dividend += float(cell[1].text.split()[0])
        i += 1

    print("\nTime period: {} {}s. ".format(size, interval))
    print("Dividend sum: {0:g}".format(dividend))
    print("Price history:\n\t",end="")
    i = 0
    while i < len(history):
        color = Back.GREEN
        if i < len(history) - 1 and history[i] < history[i+1]:
            color = Back.RED
        print(color + str(history[i]) + Back.RESET + "\t",end="")
        if i < len(history) - 1 and (i + 1) % 10 == 0: 
            print("\n\t",end="")
        i += 1
    print()

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

        i = 0
        while(i < len(alteredText)):
            if alteredText[i] == '-':
                break
            try:
                tri = int(alteredText[i])
                break
            except ValueError:
                i += 1
            
        text.append(alteredText[0:i])
        text.append(alteredText[i:alteredText.find("%")+1])
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
commands.add("history")
commands.add("clear")

print("--------------------------------")
print("S T O N K B O T initializing ...")
marketAvg = GetMarketAverage(True)
color = Back.GREEN
if marketAvg < 0:
    color = Back.RED
print("Market average at " + color + "{0:g}".format(marketAvg) + '%' + Back.RESET)
print("--------------------------------")
GetMarketAverage()
print("--------------------------------")

while(True):
    print("Command: ", end ="")
    args = input().split()
    try:
        command = args.pop(0)
    except:
        print("Invalid -> NULL command")
        print("--------------------------------")
        continue

    if command in commands: 
        try:
            if command == "exit":
                print("Exiting ...")
                print("--------------------------------")
                break
            elif command == "price":
                GetPrice(args[0])
            elif command == "robinhood":
                GetRobinhoodPage(args[0])
            elif command == "history":
                GetHistory(args[0], args[1], args[2])
            elif command == "clear":
                os.system('cls')
        except IndexError:
            print("Invalid -> ",end="")
            print("'" + command + "', ",end="'")
            print(args,end="'\n")
    else:
        print("Invalid -> ",end="")
        print("'" + command + "', ",end="'")
        print(args,end="'\n")
    if command != "clear":
        print("--------------------------------")
