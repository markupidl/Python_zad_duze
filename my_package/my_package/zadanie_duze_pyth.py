from bs4 import BeautifulSoup
from pathlib import Path
import argparse
#from wordfreq import word_frequency
import matplotlib.pyplot as plt

from wordfreq import zipf_frequency, top_n_list
import requests
import csv
import re
import time
import json
import pandas
# niech tworzy wlasne otoczenie z inport wlasnymi typami

# teraz zrob testy i sprawdz, że to działa :
# a potem robimy pozostałe

# wf, kup bluzę, to, zad z sql


# to dokończyć, akademik zapłacic i poprosić o wjazd, plan zajęć, lektoraty i wf


def ruby_to_text(ruby):
    parts = []
    for node in ruby.contents:
        if isinstance(node, str):
            parts.append(node.strip())
        elif node.name == "rt":
            parts.append(node.text.strip())
        # rp ignorujemy
    return "".join(parts)

class Summary:
    @staticmethod
    def summary(summary): # moze jest ok?
        response = requests.post('https://bulbapedia.bulbagarden.net/wiki/' + summary) # jesli istnieje
        if response.status_code != 404: 
            soup = BeautifulSoup(response.text, 'html.parser')
            text_paragraphs = soup.find('div', class_='mw-body-content')
            first_paragraph = text_paragraphs.find('p')
            for ruby in  first_paragraph.find_all("ruby"):
                ruby.replace_with(ruby_to_text(ruby))
            print(first_paragraph.text)
        else:
            print("Strona nie istnieje")

class Table:
    @staticmethod
    def table(n, strona, jestrue): # jest true zmienia troszke, pierwszy tr jest inny
        s = strona.replace(" ", "_")
        response = requests.post('https://bulbapedia.bulbagarden.net/wiki/' + strona) # zrob naglowek boczny
        if response.status_code != 404: 
            soup = BeautifulSoup(response.text, 'html.parser')
            #text_paragraphs = soup.find_all('div', class_='mw-body-content')
            #first_paragraph = text_paragraphs.find('p').text
            text_paragraphs = soup.find('div', class_='mw-body-content')
            tablica = text_paragraphs.find_all('table')[n-1] # czy istnieje taka tablica???
            tr = tablica.find_all('tr')
            with open(strona + '.csv', 'w', newline='') as plik:
                pisarz = csv.writer(plik)
                czy = False
                czynorm = False
                for wiersz in tr:
                    if czy: 

                        #i = 0
                        #for wi in w:
                        #    h[i] = wi.text
                        #    i += 1
                        if jestrue:
                            if czynorm: 
                                w = wiersz.find_all('td')
                                m = wiersz.find('a')
                                h = []
                                h.append(m.text)
                                for wi in w: h.append(wi.text)
                                pisarz.writerow(h)
                            else: 
                                czynorm = True
                                h = []
                                w = wiersz.find_all('a')
                                h.append("")
                                for wi in w: h.append(wi.text)
                                pisarz.writerow(h)
                                # zapisz jako nagłówek
                        else:
                            w = wiersz.find_all('td')
                            m = wiersz.find('a')
                            h = []
                            h.append(m.text)
                            for wi in w: h.append(wi.text)
                            pisarz.writerow(h)
                    else: czy = True
                    #print(first_paragraph)
        else:
            print("Strona nie istnieje")


class Scrapper:
    def __init__(url, dodurl, czyuzyclocalhtml):
        self.url = url + "/" + dodurl.replace(" ", "_")

class count_words:
    @staticmethod
    def count_words(strona, moja):
        dictionary, ile = count.count(moja + strona, {})
        with open(strona + '.json', 'w', encoding="utf-8") as plik:
            json.dump(dictionary, plik, ensure_ascii=False, indent=2)
        #plik.json()

class count:
    @staticmethod
    def count(strona, dicti):
        response = requests.post(strona) # jesli istnieje dlaczego payload nie dziala przyrequests??
        if response.status_code != 404: 
            print("jest")
            soup = BeautifulSoup(response.text, 'html.parser')
            text_paragraphs = soup.find('div', class_='mw-body-content').text
            #juz mamy tekst caly yay, teraz trza go przeanalizowac!
            #dicti = {}
            ile = 0
            words = re.findall(r"\b\w+\b", text_paragraphs)
            for i, word in enumerate(words):
                dicti[word] = dicti.get(word, 0) + 1
                if ile < dicti[word]: ile = dicti[word]
                #if word in dicti:
                #    dicti[word][0] += 1 #tak????
                #    if dicti[word][0] > ile: ile = dicti[word][0]
               # else:
               #     dicti.append(word)
               #     dicti[word][0] = 0

            return dicti, ile
            #text_paragraphs = soup.find('div', class_='mw-body-content')
            #first_paragraph = text_paragraphs.find('p').text
            #print(first_paragraph)
        else:
            print("Strona nie istnieje")
            return dicti, 0

class znajdzstrony:
    @staticmethod
    def znajdzstrony(strona): # a skąd ma brać te strony, hmm?
        response = requests.post(strona)
        if response.status_code != 404: 
            soup = BeautifulSoup(response.text, 'html.parser')
            soup2 = soup.find('div', class_='mw-body-content')
            stro = soup2.find_all('a', href=True)
            return stro
        else: return []

class dodolu:
    @staticmethod # znajdz tylko te strony ktore sa okej, nie próbuj wszystkich
    def dodolu(strona, moja, n, t, wszystko):
        wszystko, cokolwiek = count.count(strona, wszystko)
        if n != 0:
            strony = znajdzstrony.znajdzstrony(strona)
            for html in strony:
                #print("ha")
                #

                #if requests.post(moja + html.get('href')).status_code != 404:
                    #time.sleep(t)
                wszystko = dodolu.dodolu(moja + html.get('href'), moja, n-1, t, wszystko)
        return wszystko


class workfreq:
    @staticmethod
    def workfreq(mode, chart, strona):
        #znajdz wszystkie slowa i ich czestotliwosci
        freq, ile = count.count(strona, {})
        words = {}
        table = []
        print(ile)
        if ile != 0:
            for word in freq:
                freq[word] = freq.get(word)/ile
        #if ile != 0:
        #    for pas, word in freq:
        #        freq[word][0] = freq[word][0]/ile
        if mode == 'article':
            words = freq.keys()
            #blob = freq
            for word in words:
                table.append({
                    "word": word,
                    "wiki_freq": freq.get(word),
                    "en_freq": zipf_frequency(word, "en")  # None if missing
                })
        elif mode == 'language': 
            words = top_n_list("en", 10)
            for word in words:
                table.append({
                    "word": word,
                    "en_freq": zipf_frequency(word, "en"),
                    "wiki_freq": freq.get(word)  # None if missing
                })
        df = pandas.DataFrame(table)
        print(df.head)
        #df.to_csv("word_frequencies.csv", index=False)
        if chart is not None:
            plt.title("Frequency of some word on Wiki")
            ax = df.set_index("word")[["en_freq", "wiki_freq"]].plot.bar(color=["steelblue", "orange"], figsize=(12, 6))
            ax.set_ylabel("Frequency")
            ax.set_xlabel("Word")
            ax.legend(
                #title="Frequency source",
                labels=["English wordfreq", "Wiki frequency"]
            )
            plt.savefig("word_frequencies.jpg", dpi=300)
        #df_24g = df[df["Czas uśredniania"] == '24g'].copy() 
        #df_24g.boxplot(column="Średnia", by="Rok")
        #plt.title("Rozkład PM2.5 dla województw")
        #plt.xlabel("Rok")
        #plt.ylabel("Średnia")
        #plt.grid(True)
        #plt.show()

        #df_24g = df[df["Czas uśredniania"] == '24g'].copy() 

        #df_24g["ponad"] = (df_24g["Średnia"] >= 25).astype(int)

        #pivot1 = pd.pivot_table(
        #    df_24g,
        #    index="Województwo",
        #    columns="Rok",
        #    values=["Średnia", "ponad"],
        #    aggfunc={"Średnia": 'value', 'ponad': 'value'}
        #)



        # zrób 

    # analizuj ile jest slow

class Strona():
    #str stronamoja
    def __init__(self, strona):
        self.stronamoja = strona
    def parser(self):
        parser = argparse.ArgumentParser(
            add_help=False
        )

        # 3 flagi: -o, -z, -h
        parser.add_argument('--summary', type=str)
        parser.add_argument('--table', type=str, help='Zapisz pliki')
        parser.add_argument('--number', type=int, help='Wyświetl pomoc')
        parser.add_argument('--count-words', type=str, help='Wyświetl pomoc', dest="count_words")
        parser.add_argument('--first-row-is-header', action = 'store_true', help='Wyświetl pomoc', dest="first_row_is_header")
        parser.add_argument('--analyze-relative-word-frequency', type=str, help='Wyświetl pomoc', dest="analyze_relative_word_frequency")
        parser.add_argument('--mode', type = str, help='Wyświetl pomoc')
        parser.add_argument('--count', help='Wyświetl pomoc')
        parser.add_argument('--chart', action = 'store_true', help='Wyświetl pomoc', dest='prawda')
        parser.add_argument('--auto-count-words', help='Wyświetl pomoc', dest="auto_count_words")
        parser.add_argument('--depth', type = int, help='Wyświetl pomoc')
        parser.add_argument('--wait', type=int, help='Wyświetl pomoc')
        #args = parser.parse_args()
        return parser
    
    def master(self, args):
        #args = parser.parse_args()
       # if args.store_true:
        if args.summary is not None:
            #summary()
            s = args.summary.replace(" ", "_")
            Summary.summary(s)
            #print("Tryb odczytu")

        elif args.table is not None:
            if args.number is not None:
                table.table(args.number, args.table, args.first_row_is_header)
            #print("Tryb zapisu")
        elif args.count_words is not None:
            s2 = args.count_words.replace(" ", "_")
            count_words.count_words(s2, self.stronamoja + '/')
        elif args.auto_count_words:
            if args.depth is not None:
                if args.wait is not None: 
                    s = args.auto_count_words.replace(" ", "_")
                    dodolu.dodolu(self.stronamoja + '/' + s, self.stronamoja, args.depth, args.wait, {})
        elif args.analyze_relative_word_frequency is not None:
            if args.mode is not None: 
                workfreq.workfreq(args.mode, args.prawda, self.stronamoja)
            # slowo.zmien(" ", "_"), idź do str, (sprawdź czy istnieje)
            #if not args.odczyt and not args.zapis and not args.help:
            #    args.zapis = True
            #    print("Nie podano flagi - ustawiam domyślnie tryb ZAPISU (-z)")

            # Tryb interaktywny
            #print("Podaj dane ([miesiace], [dni], [pory])")
            #data = input()

            ##lista_danych = zmiana_danych(data)
            ##miesiace = lista_danych[1]
            ##dni_input = lista_danych[2]
            ##pora_input = lista_danych[3]
            ##if args.odczyt:
            ##    odczyt_plikow(miesiace, dni_input, pora_input)
            ##elif args.zapis:
            ##    zapisanie_plikow(miesiace, dni_input, pora_input)
        else:
            print("Program nic nie robi.") 

    


#s = Strona("https://bulbapedia.bulbagarden.net/wiki")
#parser = s.parser()
#args = parser.parse_args()
#s.master(args)


