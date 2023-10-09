#kör "pip -m install" för att ladda ner modulerna 
#bs4 är oklart vad det är hehe. 
#beautifulsoup är en web-skrapare
#re är reg-ex. (regular expressions)
from bs4 import BeautifulSoup
#from discordwebhook import Discord 
import requests
import re 

#copy-pastea in din webhook från discord i url="" 
#discord = Discord(url="")

#URL länk till karolinskas restaurang
#denna funkar obviously inte på helger
url= 'https://jonsjacob.gastrogate.com/lunch'
response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')

lunchElements = soup.find("tbody", class_="lunch-day-content").text
lunchElements = re.sub('\s+',' ',lunchElements)
lunchElements = lunchElements.replace("105 kr", "- 105 kr" + "\n")

lunch1 = ""
lunch2 = ""
lunch3 = ""

count = 0
for i, x in enumerate(lunchElements):
    if x == "\n":
        count += 1
    if x != "\n" and count == 0:
        lunch1 += x
    elif x != "\n" and count == 1:
        lunch2 += x
    elif x != "\n" and count == 2:
        lunch3 += x

def handle_response(message) -> str:
    p_message = message.lower()

    if p_message == 'dagenslunch':
        lunch = lunchElements
        return "**Dagens utbud på Karolinska:** \n" + "-" + lunch1 + "\n" + "-" + lunch2 + "\n" + "-" + lunch3
    else:
        return 