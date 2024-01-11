from bs4 import BeautifulSoup
import requests
from icalendar import Calendar
import re 
import datetime
import random
import os
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

#URL länk till karolinskas restaurang
def generate_response(input_text):
    inputs = tokenizer.encode(input_text, return_tensors='pt')
    outputs = model.generate(inputs, 
                            max_length=200, 
                            do_sample=True,
                            num_return_sequences=1,  # Generate 3 responses at once
                            temperature=0.9, 
                            repetition_penalty=1.6,
                            top_k=100, 
                            top_p=0.7)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# Funktion för att hämta start- och slutdatum för aktuell vecka
def get_current_week_dates():
    today = datetime.date.today()
    start_week = today - datetime.timedelta(days=today.weekday())
    end_week = start_week + datetime.timedelta(days=6)
    return start_week, end_week

def dagens_meme():
    #memeurl
    memeurl = "https://programming-memes-images.p.rapidapi.com/v1/memes"

    #memeheaders
    headers = {
        "X-RapidAPI-Key": os.environ.get('X-RapidAPI-Key'),
        "X-RapidAPI-Host": "programming-memes-images.p.rapidapi.com"
    }
    response = requests.get(memeurl, headers=headers).json()
    image_links = [item['image'] for item in response]
    return random.choice(image_links)

def skolschemat(arg):
    
    start_week, end_week = get_current_week_dates()

    # URL till .ics-filen
    ics_url = "https://cloud.timeedit.net/nackademin/web/1/ri6925ZQ1Q21e4QZ05Q8dt9QZB8ZZ4891u1YZ6Qy575t2nDb1F7QA2889B3EFAE30451A0C8.ics"

    # Hämta .ics-filen
    response = requests.get(ics_url)
    response.raise_for_status()  # Kontrollera att nedladdningen lyckades

    # Läs in .ics-filen
    cal = Calendar.from_ical(response.text)
    # Samla alla relevanta händelser för veckan
    weekly_events = []
    for component in cal.walk():
        if component.name == "VEVENT":
            start_time = component.get('dtstart').dt
            if start_week <= start_time.date() <= end_week:
                summary = str(component.get('summary'))
                summary_parts = summary.split(',')
                event = {
                    "subject": summary_parts[2].strip(),
                    "teacher": summary_parts[1].strip(),
                    "start_time": start_time,
                    "end_time": component.get('dtend').dt,
                    "location": str(component.get('location'))
                }
                weekly_events.append(event)

    # Sammanfoga händelser som tillhör samma lektion
    combined_events = {}
    for event in weekly_events:
        key = (event["subject"], event["start_time"].date())
        if key not in combined_events:
            combined_events[key] = event
        else:
            combined_events[key]["end_time"] = max(combined_events[key]["end_time"], event["end_time"])

    # Skriv ut sammanfogade händelser
    veckansschema = ""
    dagensschema = ""
    dagensklassrum = ""
    for event in combined_events.values():
        veckansschema += f"> {event['start_time'].strftime('%A')} \n"
        veckansschema += f"> {event['subject']} - {event['teacher']} \n"
        veckansschema += f"> {event['start_time'].strftime('%H:%M')} - {event['end_time'].strftime('%H:%M')} \n"
        veckansschema += f"> {event['location']}\n\n"
    
    for event in combined_events.values():
        if event['start_time'].strftime('%Y-%m-%d') == str(datetime.date.today()):
            dagensschema += f"> {event['subject']} - {event['teacher']} \n"
            dagensschema += f"> {event['start_time'].strftime('%H:%M')} - {event['end_time'].strftime('%H:%M')} \n"
            dagensschema += f"> {event['location']}\n\n"
            dagensklassrum = f"> {event['location']}\n"

    if arg == "veckansschema":
        return veckansschema
    elif arg == "dagensschema":
        return dagensschema
    elif arg == "dagensklassrum":
        return dagensklassrum

def get_lunches():
    restaurangurl= 'https://jonsjacob.gastrogate.com/lunch'
    response = requests.get(restaurangurl)

    soup = BeautifulSoup(response.text, 'html.parser')

    lunchElements = soup.find("tbody", class_="lunch-day-content").text
    lunchElements = re.sub('\s+',' ',lunchElements)
    lunchElements = lunchElements.replace("115 kr", "\n")
    lunches = []
    current_lunch = ""
    for x in lunchElements:
        if x != "\n":
            current_lunch += x
        else:
            lunches.append(current_lunch)
            current_lunch = ""
    return lunches

get_lunches()
def handle_response(message) -> str:
    p_message = message.lower()
    lunches = get_lunches()
    if p_message == 'dagenslunch':
        if len(lunches) > 0:
            message = "**Dagens utbud på Karolinska:**\n" 
            for lunch in lunches:
                message += "-" + lunch + "\n"
            return message
    elif p_message == 'veckansschema':
        if len(skolschemat('veckansschema')) < 1:
            return "Inga lektioner denna vecka"
        else:
            return f"### Schema vecka {datetime.date.today().isocalendar()[1]} \n {skolschemat('veckansschema')}"
    elif p_message == 'dagensschema':
        if len(skolschemat('dagensschema')) < 1:
            return "Inga lektioner idag"
        else:
            return f"### {datetime.date.today().strftime('%A')} \n {skolschemat('dagensschema')}"
    elif p_message == 'dagensklassrum':
        if len(skolschemat('dagensklassrum')) < 1:
            return "Det är ingen lektion idag."
        else:
            return "### Dagens klassrum \n" + skolschemat('dagensklassrum')
    elif p_message == 'dagensmeme':
        return dagens_meme()
    elif p_message == 'dagensveg':
        message = "Todays lunches are"
        for lunch in lunches:
            message += " " + lunch 
        return generate_response(f"{message} and the vegetarian one is: ")
    else:
        return 