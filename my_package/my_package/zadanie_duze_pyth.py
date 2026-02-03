import argparse
import csv
import json
import re
import time
from pathlib import Path

import matplotlib.pyplot as plt
import pandas
import requests
from bs4 import BeautifulSoup
from wordfreq import zipf_frequency, top_n_list


def ruby_to_text(ruby):
    parts = []
    for node in ruby.contents:
        if isinstance(node, str):
            parts.append(node.strip())
        elif node.name == "rt":
            parts.append(node.text.strip())
    return "".join(parts)

class Summary:
    @staticmethod
    def summary(summary: str, moja: str):
        response = requests.post(moja + summary)
        if response.status_code == 200: 
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
    def table(n: int, strona: str, jestrue: bool, moja: str):
        s = strona.replace(" ", "_")
        response = requests.post(moja + strona)
        if response.status_code == 200: 
            soup = BeautifulSoup(response.text, 'html.parser')
            text_paragraphs = soup.find('div', class_='mw-body-content')
            tablica = text_paragraphs.find_all('table')[n - 1]
            tr = tablica.find_all('tr')
            with open(strona + '.csv', 'w', newline='') as plik:
                pisarz = csv.writer(plik)
                czy = False
                czynorm = False
                for wiersz in tr:
                    if czy: 
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
                        else:
                            w = wiersz.find_all('td')
                            m = wiersz.find('a')
                            h = []
                            h.append(m.text)
                            for wi in w: h.append(wi.text)
                            pisarz.writerow(h)
                    else: 
                        czy = True
        else:
            print("Strona nie istnieje")


class CountWords:
    @staticmethod
    def count_words(strona: str, moja: str):
        dictionary, ile = Count.count(moja + strona, {})
        with open(strona + '.json', 'w', encoding="utf-8") as plik:
            json.dump(dictionary, plik, ensure_ascii=False, indent=2)

class Count:
    @staticmethod
    def count(strona: str, dicti):
        response = requests.post(strona)
        if response.status_code == 200: 
            soup = BeautifulSoup(response.text, 'html.parser')
            text_paragraphs = soup.find('div', class_='mw-body-content').text
            ile = 0
            ktore = ""
            words = re.findall(r"\b\w+\b", text_paragraphs)
            for i, word in enumerate(words):
                dicti[word] = dicti.get(word, 0) + 1
                if ile < dicti[word]: 
                    if zipf_frequency(word, "en") > 0:
                        ile = dicti[word]
                        ktore = word
            return dicti, ktore
        else:
            print("Strona nie istnieje")
            return dicti, ""

class Znajdzstrony:
    @staticmethod
    def znajdzstrony(strona: str):
        response = requests.post(strona)
        if response.status_code == 200: 
            soup = BeautifulSoup(response.text, 'html.parser')
            soup2 = soup.find('div', class_='mw-body-content')
            stro = soup2.find_all('a', href=True)
            return stro
        else: 
            return []

class Dodolu:
    @staticmethod
    def dodolu(strona: str, moja: str, n: int, t: int, wszystko, historia):
        print(strona)
        wszystko, cokolwiek = Count.count(strona, wszystko)
        if n != 0:
            strony = Znajdzstrony.znajdzstrony(strona)
            for html in strony:
                if html.get('href') not in historia:
                    if "wiki" not in html.get('href'):
                        if requests.post(moja + html.get('href')).status_code != 404:
                            historia.add(strona)
                            time.sleep(t)
                            wszystko = Dodolu.dodolu(moja + html.get('href'), moja, n-1, t, wszystko, historia)
                        else: print(html.get('href') + " strona poza wiki")
        return wszystko



class Workfreq:
    @staticmethod
    def workfreq(mode: str, chart: str, strona: str, count: int):
        freq, word2 = Count.count(strona, {})
        words = {}
        table = []
        if word2 != "":
            for word1 in freq:
                freq[word1] = freq.get(word1)/freq.get(word2)
        if mode == 'article':
            words = freq.keys()
            for word in words:
                count -= 1
                fre = zipf_frequency(word, "en")
                if zipf_frequency(word, "en") > 0:
                    if zipf_frequency(word2, "en") > 0:
                        fre = fre/zipf_frequency(word2, "en")
                table.append({
                    "word": word,
                    "wiki_freq": freq.get(word),
                    "en_freq": fre 
                })
                if count == 0: break
        elif mode == 'language': 
            words = top_n_list("en", 10)
            for word in words:
                count -= 1
                fre = zipf_frequency(word, "en")
                if zipf_frequency(word, "en") > 0:
                    if zipf_frequency(word2, "en") > 0:
                        fre = fre/zipf_frequency(word2, "en")
                table.append({
                    "word": word,
                    "en_freq": fre,
                    "wiki_freq": freq.get(word) 
                })
                if count == 0: break
        df = pandas.DataFrame(table)
        print(df.head())
        if chart is not None:
            plt.title("Frequency of some word on Wiki")
            ax = df.set_index("word")[["en_freq", "wiki_freq"]].plot.bar(color=["steelblue", "orange"], figsize=(12, 6))
            ax.set_ylabel("Frequency")
            ax.set_xlabel("Word")
            ax.legend(
                labels=["English wordfreq", "Wiki frequency"]
            )
            plt.savefig(chart, dpi=300)

class Strona:
    def __init__(self, strona: str):
        self.stronamoja = strona
    def parser(self):
        parser = argparse.ArgumentParser(
            add_help=False
        )
        parser.add_argument('--summary', type=str)
        parser.add_argument('--table', type=str, help='Zapisz pliki')
        parser.add_argument('--number', type=int, help='Wyświetl pomoc')
        parser.add_argument('--count-words', type=str, help='Wyświetl pomoc', dest="count_words")
        parser.add_argument('--first-row-is-header', action = 'store_true', help='Wyświetl pomoc', dest="first_row_is_header")
        parser.add_argument('--analyze-relative-word-frequency', action = 'store_true', help='Wyświetl pomoc', dest="analyze_relative_word_frequency")
        parser.add_argument('--mode', type = str, help='Wyświetl pomoc')
        parser.add_argument('--count', type = int, help='Wyświetl pomoc')
        parser.add_argument('--chart', type = str, help='Wyświetl pomoc')
        parser.add_argument('--auto-count-words', help='Wyświetl pomoc', dest="auto_count_words")
        parser.add_argument('--depth', type = int, help='Wyświetl pomoc')
        parser.add_argument('--wait', type=int, help='Wyświetl pomoc')
        return parser
    
    def master(self, args):
        if args.summary is not None:
            s = args.summary.replace(" ", "_")
            Summary.summary(s, self.stronamoja + '/')
        if args.table is not None:
            if args.number is not None:
                Table.table(args.number, args.table, args.first_row_is_header, self.stronamoja + '/')
        if args.count_words is not None:
            s2 = args.count_words.replace(" ", "_")
            CountWords.count_words(s2, self.stronamoja + '/')
        if args.auto_count_words:
            if args.depth is not None:
                if args.wait is not None: 
                    s = args.auto_count_words.replace(" ", "_")
                    historia = set()
                    historia.add(self.stronamoja + '/' + s)
                    wszystko = Dodolu.dodolu(self.stronamoja + '/' + s, self.stronamoja, args.depth, args.wait, {}, historia)
                    with open(s + '.json', 'w', encoding="utf-8") as plik:
                        json.dump(wszystko, plik, ensure_ascii=False, indent=2)
        if args.analyze_relative_word_frequency is not None:
            if args.mode is not None: 
                if args.count is not None:
                    Workfreq.workfreq(args.mode, args.chart, self.stronamoja, args.count)

s = Strona("https://bulbapedia.bulbagarden.net/wiki")
parser = s.parser()
args = parser.parse_args()
s.master(args)


