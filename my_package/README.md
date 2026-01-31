# Analiza wiki

## autor: Martyna Kupidłowska

## Opis
Projekt analizuje artykuły z Wiki Bulbapedii, liczy słowa, generuje tabele i porównuje częstotliwość użycia słów z top słowami w języku angielskim.  
Pozwala na:
- Pobranie streszczenia artykułu i zamianę tagów `<ruby>` na tekst.
- Zliczanie słów w artykułach i zapisywanie wyników w JSON.
- Tworzenie tabel CSV z wybranych sekcji artykułów.
- Analizę względnej częstotliwości słów i wizualizację wyników.

## Streszczenie artykułu
python main.py --summary "Pikachu"

## Tworzenie tabeli z artykułu
python main.py --table "Bulbasaur" --number 1 <--first-row-is-header>

## Zliczanie słów w artykule
python main.py --count-words "Pikachu"

## Automatyczne przeszukiwanie linków w dół
python main.py --auto-count-words "Pokemon" --depth 2 --wait 1

## Analiza względnej częstotliwości słów
python main.py --analyze-relative-word-frequency --mode article --count 2 <--chart "Plik.png">

## Testy pytest w katalogu tests
pytest



## Instalacja
1. Sklonuj repozytorium
2. Zainstaluj wymagania:
   ```bash
   pip install -e .

## Wymagania
- Python 3.13.5
- biblioteki:
  - `requests`
  - `beautifulsoup4`
  - `matplotlib`
  - `pandas`
  - `wordfreq`
  - `pytest` (do testów)

## Instalacja wymagań:
```bash
pip install -e .

