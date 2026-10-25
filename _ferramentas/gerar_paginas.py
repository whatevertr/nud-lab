"""gerar_paginas.py · gera as páginas do nud-lab a partir de uma página-modelo só (`_modelo.html`).

Cada capítulo vira uma pasta com o seu index.html (/diario/, /noa/, /nudfm/, /sobre/), pro Google
enxergar cada um. Por fora o site continua igual: o menu troca o conteúdo sem recarregar, só que o
endereço é de verdade (sem #). Os links antigos com # são levados pro endereço novo.

Rodar (da raiz do repositório):  python _ferramentas/gerar_paginas.py
Muda o site? Mude o `_modelo.html` e rode de novo. Nunca edite os index.html gerados à mão.
v0.1.0 · 25/10/2026 · tars (Claude), o thinker do NUD · guardião, com a autora.
"""
import os

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ_REPO = os.path.dirname(AQUI)
SITE = "https://whatevertr.github.io/nud-lab/"
BASE_TITULO = "nud-lab · o caderno de laboratório da whatevertr"
PAGINAS = [  # (pasta, capítulo que abre, título)
    ("", "", BASE_TITULO),
    ("diario", "diario", "Diário de Bordo · nud-lab"),
    ("noa", "noa", "Noa · nud-lab"),
    ("nudfm", "nudfm", "NUD.FM · nud-lab"),
    ("sobre", "sobre", "Sobre · nud-lab"),
]

modelo = open(os.path.join(RAIZ_REPO, "_modelo.html"), encoding="utf-8").read()
urls = []
for pasta, inicial, titulo in PAGINAS:
    raiz = "../" if pasta else ""
    url = SITE + (pasta + "/" if pasta else "")
    html = (modelo.replace("__RAIZ__", raiz).replace("__INICIAL__", inicial)
                  .replace("__URL__", url).replace("__TITULO__", titulo))
    destino = os.path.join(RAIZ_REPO, pasta, "index.html") if pasta else os.path.join(RAIZ_REPO, "index.html")
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    with open(destino, "w", encoding="utf-8", newline="\n") as f:
        f.write(html)
    urls.append(url)
    print("gerada:", os.path.relpath(destino, RAIZ_REPO))

with open(os.path.join(RAIZ_REPO, "sitemap.xml"), "w", encoding="utf-8", newline="\n") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
    for u in urls:
        f.write(f"  <url><loc>{u}</loc></url>\n")
    f.write("</urlset>\n")
print("sitemap:", len(urls), "endereços")
