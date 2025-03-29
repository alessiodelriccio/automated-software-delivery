"""
Modulo per il recupero e la formattazione dei risultati in formato HTML.

Funzioni:
- get_results(file_path, chunk_size): Legge un file CSV e restituisce una tabella HTML paginata.
"""

import os
import pandas as pd

TABLE_STYLE = """
<style>
    table {
        border-collapse: collapse;
        width: 100%;
        background-color: #ffffff;
        border: 2px solid #dddddd;
    }

    thead {
        background-color: #f2f2f2;
        text-align: center;
    }

    th, td {
        border: 2px solid #dddddd;
        padding: 10px;
        text-align: center;
    }

    th {
        background-color: #4caf50;
        color: white;
    }

    tr:nth-child(even) {
        background-color: #f2f2f2;
    }

    tr:nth-child(odd) {
        background-color: #ffffff;
    }

    hr {
        margin: 1em 0;
        opacity: 0.6;
    }

    .centered-cell {
        text-align: center;
    }
</style>
"""

def get_results(file_path, chunk_size):
    """Legge un file CSV e restituisce una tabella HTML paginata.

    Args:
        file_path (str): Percorso del file CSV.
        chunk_size (int): Numero di righe per ogni blocco di lettura.

    Returns:
        str: Tabella HTML contenente i dati del file CSV.
    """
    if os.path.exists(file_path):
        try:
            chunks = pd.read_csv(file_path, chunksize=chunk_size)
            tabulated_chunks = []
            first_chunk = True
            for chunk in chunks:
                html_chunk = chunk.to_html(escape=True)
                html_chunk = html_chunk.replace("\n", "")

                if first_chunk:
                    html_chunk = f"""
                        <html>
                        <head>
                        {TABLE_STYLE}
                        </head>
                        <body>
                        <table>
                        {html_chunk}
                        </table>
                        </body>
                        </html>
                    """
                    first_chunk = False
                tabulated_chunks.append(html_chunk)
            return "".join(tabulated_chunks)
        except Exception as e:
            return f"An error occurred while reading the file: {e}"
    else:
        return "File not found"
