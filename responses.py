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

def get_lunches():
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    lunch_day_content = soup.find(class_="lunch-day-content")

    lunches = {}
    for i, div in enumerate(lunch_day_content.find_all("td", class_="td_title")):
        lunches[i] = div.text.strip()
    
    return lunches

def handle_response(message) -> str:
    p_message = message.lower()
    lunches = get_lunches()

    for i, value in enumerate(lunches.values()):
        if i == 0:
            lunch1 = value
        elif i == 1:
            lunch2 = value
        elif i == 2:
            lunch3 = value 

    if p_message == 'dagenslunch':
        return "**Dagens utbud på Karolinska:** \n" + "- " + lunch1 + "\n" + "- " + lunch2 + "\n" + "- " + lunch3
    else:
        return 