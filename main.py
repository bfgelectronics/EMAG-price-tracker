import requests
from datetime import datetime
from os import system
from time import sleep
from termcolor import colored
from bs4 import BeautifulSoup

#Configs
pages=["https://www.emag.ro/procesor-amd-ryzentm-7-3700x-36mb-4-4-ghz-cu-wraith-prism-cooler-100-100000071box/pd/D8Y10RBBM/?path=procesor-amd-ryzentm-7-3700x-36mb-4-4-ghz-cu-wraith-prism-cooler-100-100000071box/pd/D8Y10RBBM"] #here you should add links to products you want to monitor. ex: ["link1","link2","link3"]
terminal_monitor=True    #use True if you want to see the prices on the terminal (works best on linux, on windows terminal will look bad)
file_log=True    #use True if you want to log the prices to a file
request_sleep=0    #adjust the delay between page requests (in seconds) ,  adjust this and the next variable to not trigger the anti-bot verification (the higher the values, the better)
execution_sleep=600    #adjust the delay between updates (in seconds)
file_log_path="./"    #the path to the log file
#End configs

if pages==[]:
    print("Err: You forgot to add product links in the pages variable")
    exit()

if not(file_log) and not(terminal_monitor):
    print ("Err: Why you want to run this program without file logging or terminal monitoring?")
    exit()

if terminal_monitor:
    system("clear")
    print("     Loading ...")

if file_log:
    filename="session_"+str(datetime.today())+".txt"
    filename=filename.replace(":","_")
    file=open(file_log_path+filename,"x")
    file.write("Product links:\n")
    k=0
    for page in pages:
        file.write(str(k)+". "+page+"\n")
        k=k+1 
    file.close()

while True:
    i=0
    names=[]
    prices=[]
    oldprices=[]
    maxPriceLenght=0
    for page in pages:
        r = requests.get(page)
        soup = BeautifulSoup(r.content, "html.parser")
        names.append(soup.find(class_="page-title").prettify().replace('<h1 class="page-title">\n ',"").replace("</h1>\n","").replace("\n"," "))
        prices.append(soup.find(class_="product-new-price").prettify().replace('<p class="product-new-price">\n ',"").replace("</p>","").replace("\n <sup>\n  ",".").replace("\n </sup>\n <span>\n ","").replace("\n </span>\n\n",""))
        oldprices.append(soup.find(class_="product-old-price").prettify().replace('<p class="product-old-price">\n <s>\n  ',"").replace("</p>","").replace("\n  <sup>\n   ",".").replace("\n  </sup>\n  <span>\n  ","").replace("\n  </span>\n </s>","").replace('\n <span class="product-this-deal">\n  ('," ").replace("                                                                            ","").replace("\n","").replace("                                    )","").replace(" </span>",""))
        sleep(request_sleep)
    for price in prices:
        if len(price)>maxPriceLenght:
            maxPriceLenght=len(price)
    today = datetime.today()
    if file_log:
        file=open(file_log_path+filename,"a")
        file.write("\n["+str(today).replace(":","_")+"]\n")
    if terminal_monitor:
        system("clear")
        print('\033[1m',colored("  Updating at: "+str(today), 'yellow'))
    for name in names:
        if terminal_monitor:
            preetySpace="    "
            if len(prices[i])!=maxPriceLenght:
                diff=maxPriceLenght-len(prices[i])
                for j in range(diff):
                    preetySpace=preetySpace+" "
            print('\033[1m',colored("-","blue"),'\033[1m',colored(name,"green")+"\n",'\033[1m',"      ",colored(prices[i],"yellow"),preetySpace, '\033[1m'+colored(" "+oldprices[i],"red"))
        if file_log:
            file.write(name+": "+prices[i]+" | "+oldprices[i]+"\n")
        i=i+1
    if file_log:    
        file.close()
    sleep(execution_sleep)