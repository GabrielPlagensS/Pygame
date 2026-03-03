import csv
import sys
import os

def load_words(filename="words.csv"):
    words = []

    # Pega o caminho da pasta atual do arquivo
    base_path = os.path.dirname(__file__)
    file_path = os.path.join(base_path, filename)

    try:
        with open(file_path, newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                pt = row["pt-br"]
                en = row["en"]

                len_pt = int(row["len-pt-br"])
                len_en = int(row["len-en"])

                if len(pt) != len_pt or len(en) != len_en:
                    continue

                words.append({
                    "pt": pt,
                    "en": en,
                    "len_pt": len_pt,
                    "len_en": len_en
                })

    except FileNotFoundError:
        print("Arquivo words.csv não encontrado no diretório do projeto.")
        sys.exit()

    return words