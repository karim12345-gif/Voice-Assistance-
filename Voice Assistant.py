from __future__ import print_function
import time
import warnings
import news_module as news
import pyttsx3 # text to speech
import speech_recognition as sr
from gtts import gTTS  # text to speech from google
import playsound # will play the sound for us from alexa
import os # operating system
import calendar # calendar
import random # random choices
import wikipedia
import webbrowser # to open broswers for us
import ctypes # provides data types and calling functions
import winshell
import subprocess
import smtplib
import requests
import json # json files
import datetime
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from twilio.rest import Client
import wolframalpha # a website that we use the API to get all kinda of different information from there, such as Math, personal health , people, money , hobbies and so on


warnings.filterwarnings("ignore")


engine = pyttsx3.init()
voices = engine.getProperty('voices')       #getting details of current voice
engine.setProperty('voice', voices[0].id)  #changing index, changes voices. o for male
# engine.setProperty('voice', voices[1].id)   #changing index, changes voices. 1 for female


# alexa will talk to us
def talk(audio):
    engine.say(audio)
    engine.runAndWait() # whatever we pass soemthing it will say this to us

talk("hello i am your assistant, and im here to help you ? ")



def rec_audio():
    recog= sr.Recognizer() # will recognizer out text through a microphone

    with sr.Microphone() as source: # using the mic to be able to speak
        recog.energy_threshold = 100000
        recog.adjust_for_ambient_noise(source, 1.2)
        print("I am listening to your commands...... ")
        audio = recog.listen(source)
        data = " "

    try:
        data = recog.recognize_google(audio)
        print("you said:" + data)

    except sr.UnknownValueError:
        print("Assistant could not understand the audio")


    except sr.RequestError as ex:
        print("Request Errror from google speech Recogniton " + ex)


    return data

rec_audio()


def response(text):
    print(text)

    tts= gTTS(text = text, lang="eng")

    audiosound = "Audio.mp3" # saving the audio
    tts.save(audiosound) # save
    playsound.playsound(audiosound) # play the sound of the audio we are passing

    os.remove(audiosound) # we will delete it , because every time we play i, it will be saved so its better to delete it







# here you can give your name of the asssistan
def call(text):
    action_call = "alexa"

    text = text.lower()


# if alex is in the text then we return the name and true
    if action_call in text:
        return True

    return False



def today_date():
    now = datetime.datetime.now() # this will give you year month nand date and mintues and seconds
    date_now = datetime.datetime.today() # will give you the present date and time
    week_now = calendar.day_name[date_now.weekday()] # will give us the day of the week
    month_now = now.month() # will give the current month
    day_now = now.day() # will give the current day


    months = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "Agust",
        "September",
        "October",
        "November",
        "December",
    ]
    ordinals = [
        "1st",
        "2nd",
        "3rd",
        "4th",
        "5th",
        "6th",
        "7th",
        "8th",
        "9th",
        "10th",
        "11th",
        "12th",
        "13th",
        "14th",
        "15th",
        "16th",
        "17th",
        "18th",
        "19th",
        "20th",
        "21st",
        "22nd",
        "23rd",
        "24th",
        "25th",
        "26th",
        "27th",
        "28th",
        "29th",
        "30th",
        "31th",
    ]
    return f'Today is {week_now}, {months[month_now -1]} the {ordinals[day_now - 1]}.' # -1 because the month starts from zero and not 1


#
#
# #greetings
def greetings(text):
    greet= ["hi","hey","hola","greetings","wassup","hello","godday","hey there"]
    response = ["hi","hey","hola","greetings","wassup","hello","godday","hey there"]

    for word in text.split(): # we use the split to convert a string too a list of invidauls statemnts
        # it has to be lower
        if word.lower() in greet:
            return random.choice(response) + "." # returns a ramdom string from the lis greet
    return " "


# this code here will check who and is and to return the first and the last name
def wiki_person(text):
    list_wiki = text.split()
    for i in range(0, len(list_wiki)):
        if i + 3 <= len(list_wiki) - 1 and list_wiki[i].lower() == "who" and list_wiki[i+1].lower() == "is":
            return list_wiki[i+2] + " " + list_wiki[i+3]




def note(text):
    date = datetime.datetime.now()
    file_name = str(date).replace(":", "-" ) + "-note.txt"
    with open(file_name,"w") as f:
        f.write(text)

    subprocess.Popen(["notepad.exe", file_name])


def send_email(to, content):
    server = smtplib.SMTP("smt.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.login("karim991996@gmail.com","Kas@0055")
    server.sendmail("karim991996@gmail.com",to,content)
    server.close()




#this is from the google API calenedar
# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
def google_calendar():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)
    return service


def calendar_events(num,service):
    talk("Hey there!, hope you are doing fine today.These are the events to do for today. ")
    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    print(f'Getting the upcoming {num} events')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                          maxResults=num, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        events_today = (event['summary'])
        start_time = str(start.split("T")[1].split("-")[0])
        if int(start_time.split(':')[0]) < 12:
            start_time = start_time + "am"
        else:
            start_time= str(int(start_time.split(":")[0]) -12)
            start_time = start_time + "pm"
        talk(f'{events_today} at {start_time}')

try:
    service = google_calendar()
    # 10 evens and max
    calendar_events(10,service)

except:
    talk("i could not understand please ask me again ")








while True:
    try:
        text = rec_audio().lower()


        if call(text):

            speak = speak + greetings(text)


            if "date" in text or "day" in text or "month" in text:
                get_today = today_date() # will get the date of the day
                speak = speak + " " + get_today

            elif "time" in text:
                now = datetime.datetime.now()
                meridiem = ""
                if now.hour >= 12:
                    meridiem = "p.m"
                    hour = now.hour -12
                else:
                    meridiem = "a.m"
                    hour = now.hour
                if now.minute < 10:
                    minute = "0" + str(now.minute)
                else:
                    minute = str(now.minute)
                speak = speak + " " + " It is " + str(hour) + ":" + minute + " " + meridiem + " ."
            elif "wikipedia" in text or "Wikipedia" in text:
                if "who is " in text: # we say who is and siri will take it and search for the person on wikipedia
                    person = wiki_person(text)
                    wiki = wikipedia.summary(person,sentences =2)
                    speak = speak + " " + wiki
            elif "who are you " in text or " what is your name" in text or "define yourself" in text:
                speak = speak + """Hello, I am Alexa.Your assustant . I am here to make your life easier"""
            elif "your name" in text:
                speak = speak + "my name is alexa, how can i help you "

            elif " who am i then " in text or " do you know who i am " in text:
                speak = speak + " you are a human who gives me commands"

            elif " why do you exist " in text:
                speak = speak + " i was created to help blind individuals detect objects and help improve their lifes"

            elif " how are you today " in text or " how are you " in text:
                speak = speak + " im doing fine"
                speak = speak + "\n How are you?"

            elif "fine " in text or " good " in text:
                speak = speak + " i am glad to hear that, please let me know if i can help you with anything today "


# THIS WILL  open google chrome for the user
            elif "open " in text.lower():
                if "chrome" in text.lower():
                    speak = speak + "Opening Google Chrome "
                    os.startfile(
                        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
                    )
            elif " youtube" in text.lower():
                speak = speak + "Opening youtube for you in just a second..."
                webbrowser.open("youtube.com")


            elif " google" in text.lower():
                speak = speak + "Opening google "
                webbrowser.open("google.com")


            elif "open facebook" in text.lower():
                speak= speak + "Opening facebook"
                webbrowser.open("facebook.com")


            elif "open spotify" in text.lower():
                speak = speak + "Opening spotify"
                webbrowser.open("spotify.com")


            elif " play, No Guidance by drake and chris brown  " in text.lower():
                speak= speak + " playing drake"
                webbrowser.open("https://www.youtube.com/watch?v=6L_k74BOLag&ab_channel=ChrisBrownVEVO")

            elif " star" in text.lower():
                speak= speak + " playing The weekend"
                webbrowser.open("https://www.youtube.com/watch?v=34Na4j8AVgA&list=RD34Na4j8AVgA&start_radio=1")


            else:
                speak = speak + "Application is not available"

# this will search for whatever the user ask to open on youtube
        elif " youtube" in text.lower():
            # this will put all words in lower letters and split the word and put it in index ex['y','o','u','t','u,'b','e']
            ind = text.lower().split().index("youtube")
            #will start at one at go the end of the word within the list
            search = text.split()[ind + 1:]
            webbrowser.open(
                "http://www.youtube.com/results?search_query=" +
                "+".join(search)
            )
            speak = speak + "opening " + str(search) + "on youtube "

        elif "search" in text.lower():
            ind = text.lower().split().index("search")
            search = text.split()[ind + 1:]
            webbrowser.open(
                "http://www.google.com/search?q=" +
                "+".join(search)
            )
            speak = speak + "Searching " + str(search) + "on google"

        elif "google" in text.lower():
            ind = text.lower().split().index("google")
            search = text.split()[ind + 1:]
            webbrowser.open(
                "http://www.google.com/search?q=" +
                "+".join(search)
            )
            speak = speak + "Searching " + str(search) + "on google"


        elif "change the background " in text or "change wallpaper " in text:
            #this is the folder than contuines all the different pictures
            img = r'C:\Users\karim.salim\Desktop\wallpaper'
            #this will put them in a list
            list_img = os.listdir(img)
            #this will pick a random picture to display on the background
            imgChoice = random.choice(list_img)
            # we are joining the directory iof the image to the list of images
            randomImg = os.path.join(img,list_img)
            # this line here is going to change the wallpaper
            ctypes.windll.user32.SystemParametersInfoW(20,0,randomImg,0)
            speak = speak + " background changed successfully "



# will play music for the user
        elif " play music "  in text or "play song " in text:
            talk("Here you go with music ")
            music_dir = r''
            songs = os.listdir(music_dir)
            d = random.choice(songs)
            # will choose random songs from the directory
            random = os.path.join(music_dir,d)
            playsound.playsound(random)


# resycle the bin
        elif " empty the bin" in text or " empty recycle bin" in text:
            winshell.recycle_bin().empty(
                confirm=True, show_progress=False, sound=True
            )

            speak = speak + " recycle bin has been emptied for you "


        elif "note" in text or "remember this " in text:
            talk("what would you like to write down for you?")
            # will recorde what the user said
            note_text = rec_audio()
            # will note it
            note(note_text)
            speak = speak + "I have made a note of that "


# this lcoation will find the place for you on google maps
        elif "where is" in text:
            ind = text.lower().split().index("is")
            location = text.split()[ind +1:]
            # using this link
            url= "https://www.google.com/maps/@23.6303783,58.0413241,15z" + "" .join(location)
            speak = speak + "this is where" + str(location) + "is."
            webbrowser.open(url)


        elif "email to computer " in text or " gmail to computer " in text or " email this person " in text :
            try:
                talk("What should i say in the email?")
                content = rec_audio()
                to= "Reciver's email address "
                send_email(to,content)
                speak = speak + "Email has been sent!"
            except Exception as e:
                print(e)
                talk("I am not able to send this email ")

        elif " mail" in text or "email" in text or "gmail" in text:
            try:
                talk("what shouldi say?")
                content = rec_audio()
                talk("Whom should i send an email to ?")
                to = input("Enter the email address here so i can send the email to that person: ")
                send_email(to,content)
                speak = speak + " Email has been sent to that person"
            except Exception as e:
                print(e)
                speak = speak + " I am not able to send this email to that person, please try again !"

# weather , alex can tell you the weather news
        elif "weather" in text:
            #weather api key that live, we will use it to get live weather data or current weather data
            key= "c5e6786609f79c71809550be5e8cfce2"
            weather_url = "http://api.openweathermap.org/data/2.5/weather?"
            # choose the city after in , ex: what is the weather in london , we will take what comes after in
            ind = text.split().index("in")
            location = text.split()[ind + 1:]
            # we will get london on a form of a list so we need to convert it to a string
            location = "".join(location)
            url = weather_url + "appid=" + key + "&q=" + location
            # now we wanna get the url and convert it to JSON
            js = requests.get(url).json()
            if js["cod"] != "404":
                weather = js["main"]
                temperature = weather["temp"]
                # by default the tempearture is kelvin so we need to convert it to celsius
                temperature = temperature - 273.15
                #we need to add the humididty
                humidity = weather["humidity"]
                # we need description
                desc = js["weather"][0]["description"]
                weather_response = "The temperature in Celcius is " + str(temperature) + "The humidity is" + str(humidity) + "and weather description is " + str(desc)
                # now alex will speak
                speak = speak + weather_response
            else:
                # alex cant find the city
               speak = speak + " i cant find any information about this city, please try something else "




# Alexa can also tell you news about 50 countries in the world

        elif "news" in text:
            key="c5ab759769634308871f6ad1c1224515"
            url=('http://newsapi.org/gv2/top-healines?'
                'country=us&'
                 'apiKey='
                 )
            try:
                response = requests.get(url)
            except:
                talk("please check your connection something is wrong!")

            new = json.loads(response.text)


            for new in news["articles"]:
                print(str(new["tittle"]), "\n")
                talk(str(new["title"]))
                engine.runAndWait()

                print(str(new["description"]), "\n")
                talk(str(new["description"]))
                engine.runAndWait()


                #here alexa can send a message to the user through the sms
        elif "send message" in text or "message" in text or "send a message " in text:
            account_sid = "AC8713213a76de66cd16c625f527cb7e5d"
            auth_token = "494712730a5e7ae4d736e8439b45f08a"
            client = Client(account_sid, auth_token)

            talk("what should i send? ")
            message = client.messages.create(
                body = rec_audio(), from_=" ", to=" "
            )


            print(message.sid)
            speak = speak + "Message sent succesfully"



# the app id from wolframeapp
        elif "calculate " in text:
            app_id=" JRURVW-PXL7WAYLTA"
            client = wolframalpha.Client(app_id) # taking the app id into client
            ind = text.lower().split().index("calculate") # spliting the calculate into a list and each word will be split to an index ['c','a']
            text = text.split()[ind + 1:] # this will start from the first word onto the end of the list and display the rest of the ind
            res = client.query(" ".join(text)) # we are joining both the teh client with the text
            answer = next(res.results).text # this will get the final answer after the user ask Alexa the question
            speak = speak + " The answer  is  " + answer


        elif " what is " in text or "who is" in text:
            app_id = " JRURVW-PXL7WAYLTA"
            client = wolframalpha.Client(app_id)  # taking the app id into client
            ind = text.lower().split().index("is")
            text = text.split()[ind + 1:]  # this will start from the first word onto the end of the list and display the rest of the ind
            res = client.query(" ".join(text))  # we are joining both the teh client with the text
            answer = next(res.results).text  # this will get the final answer after the user ask Alexa the question
            speak = speak + " The answer  is  " + answer


            # add a command to stop alex from listening to what you say
        elif "don't listen" in text or "stop listening" in text or "do not listen" in text:
            talk("for how many seconds do you want me to sleep for ?")
            a= int(rec_audio()) # rec_audio will listen to what u say or the number and then add it in the a variable,
            time.sleep(a) # time is an imported libary that will will use sleep and make alexa sleep for the amount of time that was enterd by the user
            speak = speak + str(a) + " seconds completed "


            # another command to make alexa exit from the talk
        elif "exit" in text or "you can leave now" in text:
            exit() # exit will allow us to leave the chat and turn alex off
            response(speak)
    except:
        talk("i dont know what your saying ")








