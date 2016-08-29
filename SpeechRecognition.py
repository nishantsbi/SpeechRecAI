def Dictionary(x):
    # Searches dictionary for specified words
    print("func")
    global googleUsed
    grammar = None
    wordList = []
    count = 0
    word = x.split()
    if word[-1] in dictionaryList:
        word = word[-2]
    else:
        word = word[-1]
    noOfDefs = len(dictionary.meaning(word))
    if noOfDefs > 1:
        noOfDefs = noOfDefs/2
    reply = None
    try:

        for i in dictionaryList:
            wordExist = x.count(i)
            if wordExist > 0:
                if count <= 3:
                    reply = dictionary.meaning(word)
                    reply = reply.values()
                    for i in range(0, noOfDefs):
                        wordList.append(reply[0][i])
                    reply = "The word "+word+" means "+str(wordList)
                    break
                elif count <=6:
                    reply = dictionary.synonym(word)
                    for i in reply:
                        wordList.append(str(i))
                    wordList = str(wordList)
                    if len(wordList) > 1:
                        grammar = "are"
                        syno = "synonyms"
                    else:
                        grammar = "is"
                        syno = "synonym"
                    reply = "The "+syno+" for "+word+" "+grammar+wordList
                    break
                else:
                    reply = dictionary.atonym(word)
                    for i in reply:
                       wordList.append(str(i))
                    wordList = str(wordList)
                    if len(wordList) > 1:
                        grammar = "are"
                        syno = "antonyms"
                    else:
                        grammar = "is"
                        syno = "antonym"
                    reply = "The "+syno+" for "+word+" "+grammar+wordList
                    break
            count += 1
    except Exception:
        googleUsed = True
        GoogleIt(x)
    return reply

def howToReply():
    # If it doesn't know how to reply, it asks you how to reply
    global wait
    global questions
    global answers
    global asked
    wait = False
    system('say How would I reply to this?')
    print("Speak")
    with sr.Microphone() as source:                
        audio = r.listen(source)
    try:
        HumanAnswer = r.recognize_google(audio)
        with open("questions.txt", 'a') as questions, open("answers.txt", 'a') as answers:
            questions.write(str(asked)+"\n")
            answers.write(str(HumanAnswer)+"\n")
        questions.close()
        answers.close()
        beginAI()
    except Exception:
        global asked
        asked = 0
        system('say Sorry, I did not understand that')
        howToReply()

def GoogleIt(x):
    # Googles the phrase x
    webbrowser.get('safari').open_new_tab("https://www.google.co.uk/#q="+x)
    
def beginAI():
    # Main AI. A.K.A server
    global questions
    global answers
    global dictionaryUsed
    global questionFound
    global noOfQuestions
    global noOfAnswers
    global asked
    global wait
    global dictionaryList
    global exitWords
    global googleUsed
    questions = open("questions.txt", 'r')
    answers = open("answers.txt", 'r')
    dictionaryUsed = False
    googleUsed = False
    googleSearch = True
    questionFound = False
    noOfQuestions = 0
    noOfAnswers = 0
    wait = False
    count = 0
    if asked == None:
        system('say -v Tom Hello, how can I help?')
        print("Files opened")
    if asked != None and asked != 0 and wait == False:
        system('say Okay, anything else?')
    print("Speak")
    with sr.Microphone() as source:
        audio = r.listen(source)
    try:
        asked = r.recognize_google(audio)
        print(asked)
        
        if asked in exitWords:
            system('say Okay')
            sys.exit()
        for i in dictionaryList:
            if asked.count(i) > 0:
                dictionaryUsed = True
                reply = Dictionary(asked)
                if googleUsed == True:
                    system('say Here is what I found for '+asked)
                else:
                    system('say '+reply)
                break
        for i in asked.split():
            if i in refersToYou:
                googleSearch = False
                break
        if dictionaryUsed != True and googleSearch == True:
            for i in googleKeys:
                asked = asked.lower()
                if asked.count(i) > 0:
                    googleUsed = True
                    term = asked.split()
                    for i in googleKeys:
                        try:
                            count += 1
                            if count < len(googleKeys):
                                ind = term.index(i)
                                ind += 1
                                if term[ind] == "for":
                                    ind += 1
                                term = " ".join(term[ind:])
                            else:
                                term = " ".join(term[2:])
                            reply = GoogleIt(term)
                            system('say Here is what I found for '+term)
                            break
                        except Exception:
                            print("Google term searching")
        for i in questions:
            noOfQuestions += 1
            i = i.strip()
            if str(asked.lower()) == str(i):
                questionFound = True
                print("Found")
                break
        if questionFound == True:
            print(noOfQuestions)
            for y in answers:
                noOfAnswers += 1
                if noOfAnswers == noOfQuestions:
                    system('say '+str(y))
                    wait = True
                    break
        if questionFound == False and dictionaryUsed == False and googleUsed == False:
            howToReply()

    except Exception:
        asked = 0
        system('say Sorry, I did not understand that')
    beginAI()


import speech_recognition as sr
from os import system
import sys
from PyDictionary import PyDictionary
import sqlite3
import webbrowser
conn = sqlite3.connect('conversations.db')
cur=conn.cursor()
try:
    cur.execute('''CREATE TABLE Convo(
        question VARCHAR(100),
        answer1 VARCHAR(100)
        )''')
except sqlite3.Error as e:
    print("An error occurred: " + e.args[0])

dictionary = PyDictionary()
r = sr.Recognizer()
r.energy_threshold = 3000
r.dynamic_energy_threshold = True
r.dynamic_energy_adjustment_damping = 0.15
r.pause_threshold = 1.5
r.dynamic_energy_adjustment_ratio = 1.5
cont = True
asked = None
wait = False
googleUsed = None
noOfQuestions = 0
noOfAnswers = 0
questionFound = False
dictionaryUsed = False
dictionaryList = ["define", "meaning", "mean", "synonym", "synonyms", "Another word for", "antonym", "antonyms", "opposite of"]
exitWords = ["quit", "exit", "stop", "no", "sortie", "shutdown", "sleep", "nope"]
googleKeys = ["webpage", "google", "website", "search", "what is"]
refersToYou = ["your", "you"]
beginAI()
