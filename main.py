#kör "pip -m install" för att ladda ner modulerna 
#bs4 är oklart vad det är hehe. 
#beautifulsoup är en web-skrapare
#re är reg-ex. (regular expressions)
from bs4 import BeautifulSoup
from discordwebhook import Discord 
import requests
import re 

#copy-pastea in din webhook från discord i url="" 
discord = Discord(url="")

#URL länk till karolinskas restaurang
url= 'https://jonsjacob.gastrogate.com/lunch/'
response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')

lunchElements = soup.find_all('td', class_='td_title' )

lunches = str(lunchElements)

#regEx för att radera fula "HTML" strings som råkar komma med i response
#mer om regex här: https://www.w3schools.com/python/python_regex.asp



x = re.sub('/td>, <td class="td_title">', " ", lunches)
y = re.sub('<td class="td_title">', " ", x)
z = re.sub('/td>', "", y)

print(z)

