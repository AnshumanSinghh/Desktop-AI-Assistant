import datetime
import os
import pyttsx3
import re 
import speech_recognition as sr
import urllib.request
import wikipedia
import webbrowser


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
print(voices[0].id)
engine.setProperty('voice', voices[0].id)

# path of applications
vs_code_path = "E:\\Microsoft VS Code\\Code.exe"
pycharm_path = "E:\\PyCharm Community Edition 2020.3\\bin\\pycharm64.exe"
edge_path = "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe"
chrome_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
dragon_center_path = "C:\\Program Files (x86)\\MSI\Dragon Center\\Dragon Center.exe"

# register for a particular Browser
webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))

# queries to cancel the current execution
cancel_execution = re.compile(r"^(.*)exit(.*)$|^(.*)not anymore(.*)$|^(.*)leave it(.*)$|^(.*)leave(.*)$")

# making speak function to speak out the given string.
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

# to wish or greet me accordong to time
def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning!")

    elif hour >= 12 and hour < 18:
        speak("Good Afternoon!")
    
    else:
         speak("Good Evening!")
    
    speak("Hello Sir!, I am MORPHINE, your personal Virtual AI Assistant. Please tell me how may I help you?")

# function to take voice as input and convert into string.
def takeCommand():
    #It takes microphone input from the user and returns string output.
    r = sr.Recognizer()
    with sr.Microphone() as source:
        # v = sr.Microphone.list_microphone_names()
        # print(v)
        print("listening...")
        r.pause_threshold = 1
        r.energy_threshold = 300
        audio = r.listen(source)
    
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User says: {query}")
    
    except sr.UnknownValueError as e:
        print(e)
        speak("Say that again please...")
        return 'None'

    except sr.RequestError as e:
        print(e)
        speak("I'm feeling Network issue...It will be grateful if you 'HELP ME OUT!'.")
        speak("And please re-run this program once you SETUP THE NETWORK CONNECTION.")
    return query


# function to extract files even from the deep folders. Just give initial path for that folder.
movie_dir = 'D:\\Movies'
new = []
def file_extractor(movie_dir):
    mv_li = os.listdir(movie_dir)
    mk_li = [x for x in mv_li if os.path.isdir(f"{movie_dir}\\{x}")]

    for x in mk_li:
        if os.path.isdir(f"{movie_dir}\\{x}"):
            path = f"{movie_dir}\\{x}\\"
            v = os.listdir(path)
            for i in v:
                new.append(f"{path}\\{i}")
            file_extractor(f"{movie_dir}\\{x}\\")
        else:
            pass
    return  [*mv_li, *new]


def youtube_videos(): 
    speak('Which video Sir!?')
    query = takeCommand().lower()

    if cancel_execution.findall(query):
        speak('Ohkay!, let me know if you need any help...')
        return 'yes'

    elif query != 'none':
        query_to_search = re.sub(" ", "+", query)
        print(query)
        html = urllib.request.urlopen(f"https://www.youtube.com/results?search_query={query_to_search}")

        video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
        res = video_ids[0]
        webbrowser.get('chrome').open_new_tab(f"https://www.youtube.com/watch?v={res}")
        speak(f'Playing {query} on YouTube.')
        return 'yes'

    else:
        youtube_videos()

    
if __name__ == '__main__':
    wishMe()
    while True:
        query = takeCommand().lower()

        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            speak(results)

        elif 'play movie' in query:

            def play_movie():
                speak("Which movie sir?")
                mv_name = takeCommand().lower()

                if cancel_execution.findall(mv_name):
                    speak('Ohkay!, let me know if you need any help...')
                    return 'yes'
                    
                elif mv_name != 'none':
                    movies = file_extractor("D:\\Movies")
                    for mv in movies:
                        if re.search(mv_name, mv.lower()):        
                            try:
                                if os.path.isdir(f'D:\\Movies\\{mv}'):
                                    os.startfile(f'D:\\Movies\\{mv}')
                                    speak(f"Here's the folder having {mv_name} movies...") 
                                    return 'yes'

                                elif os.path.isdir(mv):
                                    os.startfile(mv)
                                    speak(f"Here's the folder having {mv_name} movies...") 
                                    return 'yes'

                                else:
                                    os.startfile(mv)
                                    speak(f"Playing {mv_name} movie...") 
                                    return 'yes'

                            # If the movie already present in D:\Movies (movies folder or movie_dir here)
                            # then the list returned by file_extractor() don't contains directories to their names
                            # that's why we have to give its directory by joining its path and movie name---> {movie_dir}\\{mv}
                            except:
                                os.startfile(f'{movie_dir}\\{mv}')
                                speak(f"Playing {mv_name} movie...")
                                return 'yes'

                    # return mv_name, mv # returning 2 values bcz ---> mv_name to check voice is recognized or not and mv 
                                    # if voice is recognized properly and to get the current movie name

                else:
                    voice_for_mv_name = play_movie()
                    return voice_for_mv_name
                
            voice_for_mv_name = play_movie() # voice_for_mv_name = voice for movie name(mv_name)

            if voice_for_mv_name != 'yes': # if recognized but no such movie exist in this machine
                print(voice_for_mv_name)
                speak("Sorry Sir!, this movie doesn't exist on your machine.")
                speak("Say, play movie again. If you want to play a movie.")
                    

        elif 'the time' in query or 'time now' in query:
            strfTime = datetime.datetime.now().strftime("%H:%M:%S")
            print(strfTime)
            speak(f"The time is {strfTime}")
        
        elif 'today is' in query or 'the date' in query or "today's date" in query:
            date = datetime.datetime.now().strftime("%A %B %d %Y")
            print(date)
            speak(f"Today is {date}")
        
        elif 'open' in query and 'app' in query:
            try:
                a, *query, b = query.split()
                app_name = " ".join(query)
                var_path = {'vs code':vs_code_path, 'pycharm':pycharm_path, 'chrome':chrome_path, 'ms browser':edge_path, 'dragon centre':dragon_center_path}
                print(app_name)
                os.startfile(var_path[app_name])
                speak(f"Opening {app_name}")

            except Exception as e:
                print(f"Exception for open app is: {e}")
                speak(f"Couldn't find {query}, Please, set the path first, ignore if it's set already!")

        elif 'email to anshuman' in query:
            try:
                speak("what should i say?")
                content = takeCommand()
            except Exception as e:
                print(e)

        elif 'open' in query:
            try:
                query = query.replace('open ', '')
                var = {
                        'nse': 'www.nseindia.com', 
                        'youtube': 'youtube.com', 
                        'google': 'google.com'
                        }
                webbrowser.get('chrome').open_new_tab(var[query])
                speak(f"Openinng... {query}")

            except Exception as e:
                print(f"Exception for open is: {e}")
                speak("Couldn't find that")

        elif 'web search' in query:
            speak('What would I search for?')
            query = takeCommand().lower()

            if query == 'none':
                speak('Sorry, Would you like to try one more time?')
                query = takeCommand().lower()
                if 'yes' in query:
                    query = takeCommand().lower()
                else:
                    speak("Sorry! say 'SEARCH' again or I'm waiting for your next command.")
               
            else:
                webbrowser.get('chrome').open_new_tab(f'https://www.google.com/search?q={query}')
                speak(f'Here are the searched result for {query}')
        
        elif 'search video' in query or 'play video' in query:
            youtube_videos()

            