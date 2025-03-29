"""
Modulo per il filtraggio e l'analisi dei commit di un repository.

Funzioni:
- filter_and_save_results(input_file_path, output_file_path): Filtra e salva i commit relativi alla sicurezza.
- get_author_occurrences(): Restituisce la lista degli autori ordinata per numero di commit.
- get_major_contributors(): Genera un grafico dei principali contributori e lo restituisce come risposta HTML.
- generate_top10_contributors_html(authors): Genera una tabella HTML con i 10 migliori contributori.
"""

import base64
import csv
import io

import matplotlib.pyplot as plt
import pandas as pd
from starlette.responses import HTMLResponse

def filter_and_save_results(input_file_path, output_file_path):
    """Filtra e salva i commit contenenti riferimenti a correzioni di sicurezza.

    Args:
        input_file_path (str): Percorso del file CSV di input.
        output_file_path (str): Percorso del file CSV di output.
    """
    try:
        data_frame = pd.read_csv(input_file_path)
        filtered_df = data_frame[
            (data_frame["message"].str.contains(r"\bfix\b", case=False, regex=True))
            & (data_frame["message"].str.contains(r"\b(security|vulnerability|vulnerabilities)\b", case=False, regex=True))
        ]
        filtered_df.to_csv(output_file_path, index=False)
        print("Results successfully saved in:", output_file_path)
    except pd.errors.EmptyDataError:
        print("Il file di input è vuoto.")
    except FileNotFoundError:
        print(f"Il file {input_file_path} non è stato trovato.")
    except Exception as e:
        print(f"An error occurred during filtering and saving: {e}")

def get_author_occurrences():
    """Restituisce un elenco di autori con il numero di commit effettuati.

    Returns:
        list: Elenco di tuple (autore, numero di commit) ordinate per numero di commit.
    """
    try:
        with open("results.csv", newline="", encoding="utf-8") as csv_file:
            reader = csv.DictReader(csv_file)
            authors = {}
            for row in reader:
                author = row["author"]
                if author not in authors:
                    authors[author] = 0
                authors[author] += 1
            return sorted(authors.items(), key=lambda x: -x[1])
    except FileNotFoundError:
        print("Il file 'results.csv' non è stato trovato.")
        return []
    except Exception as e:
        print(f"An error occurred while processing the file: {e}")
        return []

def get_major_contributors():
    """Genera un grafico dei principali contributori e lo restituisce in formato HTML.

    Returns:
        HTMLResponse: Pagina HTML contenente il grafico dei contributori principali.
    """
    fig, ax = plt.subplots()
    result = get_author_occurrences()
    if result:  # Verifica che ci siano autori
        authors, occurrences = zip(*result)
        ax.bar(authors, occurrences)
        ax.set_xticklabels(authors, rotation=90, fontsize=8, fontname="Arial")
        ax.set_xlabel("Authors", fontsize=10, fontname="Arial")
        ax.set_ylabel("Occurrences", fontsize=10, fontname="Arial")
        yticks = list(range(0, max(occurrences) + 1, 1))
        ax.set_yticks(yticks)
        fig.tight_layout()
        fig.subplots_adjust(hspace=0.4, wspace=0.4)
        buf = io.BytesIO()
        fig.savefig(buf, format="png")
        buf.seek(0)
        image_b64 = base64.b64encode(buf.getvalue()).decode("utf-8")
        html_content = f"""
           <html>
              <h1 style="text-align:center;">Major contributors developer</h1>
               <body>
                   <center><img src="data:image/png;base64,{image_b64}" width="800"></center>
               </body>
           </html>
           """
        plt.close(fig)
        return HTMLResponse(content=html_content, headers={"Content-Disposition": "inline"})
    else:
        return HTMLResponse(content="<h1>No authors found</h1>", headers={"Content-Disposition": "inline"})

def generate_top10_contributors_html(authors):
    """Genera una tabella HTML con i primi 10 contributori.

    Args:
        authors (list): Elenco di tuple (autore, numero di commit).

    Returns:
        str: Tabella HTML con la classifica dei primi 10 contributori.
    """
    html_list = """
    <style>
        .top-contributors {
            list-style-type: none;
            padding: 0;
            margin: 0;
            border: 1px solid #ccc;
            border-radius: 5px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }

        .top-contributors-title {
            background-color: #f2f2f2;
            padding: 10px;
            border-bottom: 1px solid #ccc;
            border-radius: 5px 5px 0 0;
            font-family: Arial, sans-serif;
        }

        .top-contributors-title h2 {
            margin: 0;
            font-size: 18px;
            color: #333;
        }

        .top-contributors li {
            padding: 10px;
            border-bottom: 1px solid #ccc;
            font-family: Arial, sans-serif;
        }

        .top-contributors li:last-child {
            border-bottom: none;
        }

        .top-contributors li span {
            font-weight: bold;
            margin-right: 10px;
        }
    </style>
    <div class="top-contributors">
        <div class="top-contributors-title">
            <h2>Top 10 Contributors</h2>
        </div>
        <ol>
    """
    for author, occurrences in authors[:10]:
        html_list += f"<li><span>{author}:</span> {occurrences}</li>"
    html_list += "</ol></div>"
    return html_list
