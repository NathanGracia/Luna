from urllib.request import urlopen
from googletrans import Translator
from random import choice, randrange
from termcolor import colored
import speech_recognition as sr
import pyttsx3
import subprocess
import wolframalpha
import webbrowser
import wikipedia



engine = pyttsx3.init()
voices = engine.getProperty('voices')

# Penser à metttre en minuscule !! Plusieurs noms pour la phoenetique
names = ["luna", "louna"]

fermer = ["arrête-toi", "tais-toi", "stop", "ce sera tout"]
ouvrir = ["ouvre", "ouvrir", "lances", "lance"]
status = ["ça va", "vas bien"]
actus = ["actus", "actualités"]
musique = ["musique"]
cherche = ["cherche sur youtube", "cherche sur google", "cherche sur wikipédia", "cherche",
           "est-ce que tu peux me dire", "c'est quoi"]
calculs = ["calcule la somme de", "calcule la différence de", " calcule le produit de", "calcule le quotient de",
           "calcule"]

articles = ["de", "le", "la", "l'", "les", "du", "de la", "de l'", "des"]


def assistant_voix(sortie, status="info"):

    if sortie != None:
        voix = pyttsx3.init()
        print()
        if status == "info":
            color = "blue"
        elif status == "succes":
            color = "green"
        elif status == "warning":
            color = "orange"
        elif status == "user":
            color = "purple"

        print(colored("Luna : " + sortie, color))
        voix.say(sortie)
        voix.runAndWait()


def internet():
    try:
        urlopen('https://www.google.com', timeout=1)
        return True
    except:
        print("Déconnecté")
        return False


def reconnaissance():
    r = sr.Recognizer()
    r.energy_threshold = 4000
    pas_compris = "Désolé, je n'ai pas compris ."
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        r.pause_threshold = 0.7
        print('....')
        audio = r.listen(source)
        if internet():
            try:
                vocal = r.recognize_google(audio, language='fr-FR')
                print(colored(vocal, "magenta"))
                return vocal
            except sr.UnknownValueError:
                print(colored(pas_compris, "yellow"))
        else:
            try:
                vocal = r.recognize_sphinx(audio, language='fr-fr')
                print(colored(vocal, "magenta"))
                return vocal
            except sr.UnknownValueError:
                print(colored(pas_compris, "yellow"))


def application(entree):
    if entree != None:
        dico_apps = {
            "note": ["notepad", "note pad"],
            "sublime": ["sublime", "sublime texte"],
            "obs": ["obs", "obs capture", "capture l'ecran"],
            "edge": ["microsoft edge", "edge"]
        }
        fini = False
        while not fini:
            for x in dico_apps["note"]:
                if x in entree.lower():
                    assistant_voix("Ouverture de Notepad .", "succes")
                    subprocess.Popen('C:\\Windows\\System32\\notepad.exe')
                    fini = True
            for x in dico_apps["sublime"]:
                if x in entree.lower():
                    assistant_voix("Ouverture de Sublime Text .", "succes")
                    subprocess.Popen('C:\\Program Files\\Sublime Text 3\\sublime_text.exe')
                    fini = True
            for x in dico_apps["obs"]:
                if x in entree.lower():
                    assistant_voix("Ouverture de Obs .", "succes")
                    subprocess.Popen('C:\\Program Files\\obs-studio\bin\\64bit\\obs64')
                    fini = True
            for x in dico_apps["edge"]:
                if x in entree.lower():
                    assistant_voix("Ouverture de Edge .", "succes")
                    subprocess.Popen('C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe')
                    fini = True
            fini = True


def calcul(entree):
    if entree != None:
        traducteur = Translator()
        traduction = traducteur.translate(text=entree, dest="en").text
        app_id = "L5H3JP-ERXK3EVKGW"
        client = wolframalpha.Client(app_id)
        res = client.query(traduction)
        try:
            reponse = next(res.results).text
            traduction_reponse = traducteur.translate(text=reponse, dest="fr").text
            assistant_voix("le résultat est %d" % (traduction_reponse))
        except:
            assistant_voix("Il y'a eu une erreur, désolé", "warning")


def ask_status():
    all_status = ['Je vais bien merci', "Franchement c'est ok là", "Y'a eu des mieux"]
    rand = randrange(0, 2)
    assistant_voix(all_status[rand], "succes")


def sur_le_net(entree):
    if entree != None:
        for x in range(len(actus)):
            if actus[x] in entree.lower().split():
                indx = entree.lower().split().index(actus[x])
                voir_les_actus(entree, indx)

        if "youtube" in entree.lower():
            indx = entree.lower().split().index("youtube")
            recherche = entree.lower().split()[indx + 1:]
            if len(recherche) != 0:
                assistant_voix("Je cherche sur youtube", "succes")
                webbrowser.open("http://www.youtube.com/results?search_query=" + "+".join(recherche), new=2)
        elif "wikipédia" in entree.lower():
            wikipedia.set_lang("fr")
            try:
                recherche = entree.lower().replace("Je regarde sur wikipedia", "")
                if len(recherche) != 0:
                    resultat = wikipedia.summary(recherche, sentences=1)

                    assistant_voix(resultat)
            except:
                assistant_voix("Désolé, aucune page trouvée .", "succes")
        else:
            if "google" in entree.lower():
                indx = entree.lower().split().index("google")
                recherche = entree.lower().split()[indx + 1:]
                if len(recherche) != 0:
                    assistant_voix("Je te trouve ça", "succes")
                    webbrowser.open("https://www.google.com/search?q=" + "+".join(recherche), new=2)
            elif "cherche" in entree.lower() or "recherche" in entree.lower():
                indx = entree.lower().split().index("cherche")
                recherche = entree.lower().split()[indx + 1:]
                if len(recherche) != 0:
                    assistant_voix("Je regarde sur google", "succes")
                    webbrowser.open("https://www.google.com/search?q=" + "+".join(recherche), new=2)
            else:
                indx = 0

                for x in range(len(names)):
                    if names[x] in entree.lower().split():
                        indx = entree.lower().split().index(names[x])

                recherche = entree.lower().split()[indx + 1:]
                if len(recherche) != 0:
                    assistant_voix("Je te trouve ça", "succes")
                    webbrowser.open("http://www.google.com/search?q=" + "+".join(recherche), new=2)


def voir_les_actus(entree, indx):
    print("index : ")
    print(indx)
    print("string : ")
    print(entree.lower().split())
    print("mot choisis : ")
    print(entree.lower().split()[indx + 1:])
    recherche = delete_articles_contractés(entree.lower().split()[indx + 1:])
    if len(recherche) != 0:
        assistant_voix("Je t'envoie les dernieres actus", "succes")
        webbrowser.open("https://news.google.com/search?q=" + "+".join(recherche) + "&hl=fr&gl=FR&ceid=FR%3Afr", new=2)


def start_music():
    assistant_voix("C'est partit pour un petit peu de musique", "succes")
    # ici on douille yt en commenççant la playlist par un son de 0 seconeds, le prochain sera random
    webbrowser.open("https://www.youtube.com/watch?v=Mvvsa5HAJiI&list=RDMM&start_radio=1", new=2)


def main():
    assistant_voix("Salut DeusKiwi . On dirai que tu as besoin de moi")

    actif = True

    while actif:
        triggered = False
        done = False
        if (entree := reconnaissance()) is not None:

            usefull_words = delete_useless_words(entree)

            # checker si la phrase contient un trigger
            for x in range(len(names)):
                if names[x] in usefull_words.lower():
                    #print("Je me suis reconnu")
                    triggered = True

            for x in range(len(fermer)):
                if fermer[x] in usefull_words.lower() and triggered == True:
                    assistant_voix("A la prochaine DeusKiwi.")
                    actif = False
                    done = True

            for x in range(len(ouvrir)):
                if ouvrir[x] in usefull_words.lower() and triggered == True:
                    application(usefull_words)
                    done = True
                    break

            for x in range(len(cherche)):
                if cherche[x] in usefull_words.lower() and triggered == True:
                    sur_le_net(usefull_words)
                    done = True
                    break
            for x in range(len(musique)):
                if musique[x] in usefull_words.lower() and triggered == True:
                    start_music()
                    done = True
                    break
            for x in range(len(actus)):
                if actus[x] in usefull_words.lower() and triggered == True:
                    indx = entree.lower().split().index(actus[x])
                    voir_les_actus(usefull_words, indx)
                    done = True
                    break
            for x in range(len(calculs)):
                if calculs[x] in usefull_words.lower() and triggered == True:
                    calcul(usefull_words)
                    done = True
                    break

            for x in range(len(status)):

                if status[x] in usefull_words.lower() and triggered == True:
                    ask_status()
                    done = True
                    break

            if done == False and triggered == True:
                sur_le_net(usefull_words)


def delete_useless_words(string):
    useless_words = ["s'il te plaît", "merci", "c'est quoi", 'tu peux me donner', 'montre-moi', 'est-ce que']
    for word in useless_words:
        string = string.replace(word, "")
    return string


def delete_articles_contractés(string):
    print(string)
    if string[0] in articles:
        string[0] = ""
        return string


if __name__ == '__main__':
    main()
