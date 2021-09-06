import warnings
import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser

import wolframalpha
from gtts import gTTS  # text to speech from google
import playsound
import os
import os.path
import smtplib # for sending emails
import win32com.client as wincl
import time
import json
import news_module as news
import requests
import wolframalpha   # a website that we use the API to get all kinda of different information from there, such as Math, personal health , people, money , hobbies and so on

try:
    app = wolframalpha.Client("JRURVW-JL5W237G5U")
except Exception:
    print("Some features are not working ")


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')       #getting details of current voice
engine.setProperty('voice', voices[0].id)  #changing index, changes voices. o for male
# engine.setProperty('voice', voices[1].id)   #changing index, changes voices. 1 for female


# alexa will talk to us
def speak(audio):
    engine.say(audio)
    engine.runAndWait() # whatever we pass soemthing it will say this to us



def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >=0 and hour <12:
        speak("good morning")
    elif hour >=12 and hour <= 18:
        speak("good afternoon")
    else:
        speak("good evening")
    speak("I am your personal assistant. Please tell me how may i help you")


def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("listening......")
        r.energy_threshold = 100000
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognising......")
        query = r.recognize_google(audio, language='en-US')
        print(f"User said: '{query}\n")
    except Exception as e:
        print("say that again please ")
        speak("say that again please.....")
        return "None"
    return query


#send an email
def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('karim991996@gmail.com','Kas@991996')
    server.sendmail('email id',to,content)
    server.close()



def note(text):
    date = datetime.datetime.now()
    file_name = str(date).replace(":", "-" ) + "-note.txt"
    with open(file_name,"w") as f:
        f.write(text)


if __name__ == "__main__":
    wishMe()
    while True:
        query = takecommand().lower()

        if 'wikipedia' in query:
            speak("searching wikipedia")
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences = 2)
            speak("according to wikipedia")
            print(results)
            speak(results)

        elif 'open youtube' in query:
            speak("opening youtube")
            webbrowser.open("youtube.com")
        elif 'open facebook' in query:
            speak("opening facebook")
            webbrowser.open("facebook.com")
        elif 'open google' in query:
            speak("opening google")
            webbrowser.open("google.com")
        elif 'play the weekend' in query:
            speak("playing the weekend for you")
            webbrowser.open("https://www.youtube.com/watch?v=34Na4j8AVgA&list=RD34Na4j8AVgA&start_radio=1")

        elif 'play music' in query:
            speak("playing music for you ")
            music_dir = 'C:/Users/karim.salim/Desktop/music'
            songs = os.listdir(music_dir)
            print(songs)
            # songs will start from zero
            os.startfile(os.path.join(music_dir,songs[0]))

        elif "youtube" in query:
            # this will put all words in lower letters and split the word and put it in index ex['y','o','u','t','u,'b','e']
            ind = query.lower().split().index("youtube")
            #will start at one at go the end of the word within the list
            search = query.split()[ind + 1:]
            webbrowser.open(
                "http://www.youtube.com/results?search_query=" +
                "+".join(search)
            )
            speak("opening" + str(search) + " on youtube ")
        elif "search" in query:
            ind = query.lower().split().index("search")
            search = query.split()[ind + 1:]
            webbrowser.open(
                "http://www.google.com/search?q=" +
                "+".join(search)
            )
            speak("opening" + str(search) + " on the web ")

        elif 'send email' in query:
            try:
                speak("what should i say?")
                content = takecommand()
                to = "karim991996@gmail.com" # to the person the email will be sent too
                sendEmail(to,content)
                speak("email has been sent")
            except Exception as e:
                print(e)
                speak("there was an error with something, please check again the information ")



        elif "open notion" in query:
            speak("give me a second karim, i will open notion for you")
            codePath = "C:/Users/karim.salim/AppData/Local/Programs/Notion/Notion.exe"
            os.startfile(codePath)
            print("enjoy")
            speak("enjoy karim")
        elif "open chrome" in query:
            speak("give me a second karim, i will open google chrome for you")
            codePath = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"
            os.startfile(codePath)
            print("enjoy")
            speak("enjoy karim")

            # normal questions
        elif 'how are you' in query:
            speak("i am fine. Thank you")
            speak("how are you karim ?")

        elif "good" in query:
            speak("its nice to hear that")


        elif "who are you" in query:
            speak("I am your personal assistant and they call me Alexa")


        elif "you can leave now" in query:
            print("bye karim ")
            speak("i will leave now, see you later")
            exit()



        elif "remember this" in query:
            speak("what should i write karim ?")
            note = takecommand()
            file = open('data.txt','w')
            speak("karim, should i include date and time as well? ")
            snfm = takecommand()
            if 'yes' in snfm or 'sure' in snfm:
                strTime = datetime.datetime.now().strftime("% H:% M:%S")
                file.write(strTime)
                file.write(" :- ")
                file.write(note)
            else:
                file.write(note)
        elif "show me my notes" in query:
            speak("showing your notes")
            file = open("data.txt","r")
            print(file.read())
            speak(file.read(6))




        elif "what is" in query:
            try:
                res = app.query(query)
                print(next(res.results).text)
                speak(next(res.results).text)
            except:
                print("internet connection was bad")
                speak("internet connection was bad")


        elif "where is" in query:
            try:
                res = app.query(query)
                print(next(res.results).text)
                speak(next(res.results).text)
            except:
                print("Internet connection was bad")
                speak("Internet connection was bad ")



        elif "compare" in query:
            try:
                res = app.query(query)
                print(next(res.results).text)
                speak(next(res.results).text)
            except:
                print("Internet connection was bad ")
                speak("Internet connection was bad ")


# what time and date
        elif "time" in query:
            try:
                res = app.query(query)
                print(next(res.results).text)
                speak(next(res.results).text)
            except:
                print("internet connection was bad")
                speak("internet connection was bad")

                #date, ex find the current date and time , get inforamtio baout time zone, current time in specfied city
        elif "date" in query:
            try:
                res = app.query(query)
                print(next(res.results).text)
                speak(next(res.results).text)
            except:
                print("Internet connection was bad ")
                speak("Internet connection was bad ")

        elif "tell me" in query:
            try:
                res = app.query(query)
                print(next(res.results).text)
                speak(next(res.results).text)
            except:
                print("Internet connection was bad")
                speak("Internet connection was bad")



        elif "who is" in query:
            try:
                res = app.query(query)
                print(next(res.results).text)
                speak(next(res.results).text)
            except:
                print("internet connection was bad ")
                speak("internet connection was bad")
            # else:
            #     try:
            #         res = app.query(query)
            #         print(next(res.results).text)
            #         speak(next(res.results).text)
            #     except:
            #         print("internet connection was bad ")



        elif 'calculate' in query:
            try:
                res = app.query(query)
                print(next(res.results).text)
                speak(next(res.results).text)
            except:
                print("internet connection was bad ")
                speak("internet connection was bad")




        elif 'tempreature' in query:
            try:
                res = app.query(query)
                print(next(res.results).text)
                speak(next(res.results).text)
            except:
                print("internet connection was bad ")
                speak("internet connection was bad")























