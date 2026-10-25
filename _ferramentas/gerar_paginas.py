"""gerar_paginas.py · gera as páginas do nud-lab a partir de uma página-modelo só (`_modelo.html`)
e dos posts da pasta `_posts/` (um arquivo por post).

Cada capítulo vira uma pasta com o seu index.html (/diario/, /noa/, /nudfm/, /sobre/), pro Google
enxergar cada um. Por fora o site continua igual: o menu troca o conteúdo sem recarregar, só que o
endereço é de verdade (sem #). Os links antigos com # são levados pro endereço novo.

Rodar (da raiz do repositório):  python _ferramentas/gerar_paginas.py
Muda o site? Mude o `_modelo.html` e rode de novo. Post novo? Crie um arquivo em `_posts/` e rode de novo.
Nunca edite os index.html gerados à mão. Só usa Python puro (nada pra instalar).

O formato de um post (`_posts/AAAA-MM-DD-titulo.md`):
    ---
    tipo: WHATEVER-LOG          (ou THINKER, ou TEXTO)
    titulo: whatever-log 26/10/2026
    data: 2026-10-26            (ou com a hora, pra ordenar posts do mesmo dia: 2026-10-26 21:30)
    tags: wtr devlog
    origem:                     (opcional: o link do post original, se veio de outro lugar)
    ---
    o texto do post. parágrafo separado por linha em branco.
    **negrito**, *itálico*, [link](https://...), ![descrição da imagem](assets/posts/arquivo.webp)
    - item de lista

v0.2.0 · 25/10/2026 · tars (Claude), o thinker do NUD · guardião, com a autora.
"""
import glob, html, os, re

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


def inline(s):
    """O markdown de dentro da linha: imagem, link, negrito, itálico (o texto já vem escapado)."""
    s = re.sub(r"!\[([^\]]*)\]\(([^)\s]+)\)", r'<img src="\2" alt="\1" loading="lazy">', s)
    s = re.sub(r"\[([^\]]+)\]\((https?://[^)\s]+)\)", r'<a href="\2" target="_blank" rel="noopener noreferrer">\1</a>', s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"(?<![*\w])\*(?!\s)(.+?)(?<!\s)\*(?![*\w])", r"<i>\1</i>", s)
    return s


def markdown(texto):
    """Markdown simples: parágrafos, listas com '- ', e o que o inline() entende. HTML puro passa direto."""
    if texto.lstrip().startswith("<"):
        return texto.strip()
    saida = []
    for bloco in re.split(r"\n\s*\n", texto.strip()):
        linhas = [l.rstrip() for l in bloco.splitlines() if l.strip()]
        if linhas and all(l.lstrip().startswith("- ") for l in linhas):
            saida.append("<ul>" + "".join(f"<li>{inline(html.escape(l.lstrip()[2:]))}</li>" for l in linhas) + "</ul>")
        else:
            saida.append("<p>" + "<br>".join(inline(html.escape(l)) for l in linhas) + "</p>")
    return "".join(saida)


def ler_post(caminho):
    t = open(caminho, encoding="utf-8").read()
    m = re.match(r"---\n(.*?)\n---\n(.*)", t, re.S)
    if not m:
        raise SystemExit(f"RECUSADO: {os.path.basename(caminho)} não começa com o cabeçalho entre ---")
    cab = dict(l.split(":", 1) for l in m.group(1).splitlines() if ":" in l)
    cab = {k.strip(): v.strip() for k, v in cab.items()}
    for campo in ("tipo", "titulo", "data"):
        if not cab.get(campo):
            raise SystemExit(f"RECUSADO: {os.path.basename(caminho)} sem '{campo}' no cabeçalho")
    return cab, m.group(2)


def cartao(cab, corpo):
    d = cab["data"][:10]   # a hora (se tiver) só serve pra ordenar
    data_br = f"{d[8:10]}/{d[5:7]}/{d[0:4]}"
    corpo_html = markdown(corpo)
    if 'src="assets/' in corpo_html:
        corpo_html = corpo_html.replace('src="assets/', 'src="__RAIZ__assets/')
    corpo_html = re.sub(r'<img src="__RAIZ__assets/([^"]+)" alt="([^"]*)"(?! loading)', r'<img src="__RAIZ__assets/\1" alt="\2" loading="lazy"', corpo_html)
    tags = " ".join("#" + html.escape(x) for x in cab.get("tags", "").split()[:4])
    origem = cab.get("origem", "")
    pe_link = ""
    if origem:
        onde = "tumblr do NUD" if "nerdunitdescription" in origem else ("tumblr whatevertr" if "tumblr" in origem else "post original")
        pe_link = f'<a href="{html.escape(origem)}" target="_blank" rel="noopener noreferrer">ver no {onde} ↗</a>'
    return (f'<article class="cartao"><div class="etq"><span>//{html.escape(cab["tipo"])}_</span><time datetime="{d}">{data_br}</time></div>'
            f'<h3>{html.escape(cab["titulo"])}</h3><div class="post">{corpo_html}</div>'
            f'<div class="pe"><span class="tags">{tags}</span>{pe_link}</div></article>')


posts = [ler_post(p) for p in glob.glob(os.path.join(RAIZ_REPO, "_posts", "*.md"))]
posts.sort(key=lambda x: x[0]["data"], reverse=True)
diario = "\n".join(cartao(c, b) for c, b in posts)

modelo = open(os.path.join(RAIZ_REPO, "_modelo.html"), encoding="utf-8").read()
if "__DIARIO__" not in modelo:
    raise SystemExit("RECUSADO: o _modelo.html não tem o marcador __DIARIO__")
modelo = modelo.replace("__DIARIO__", diario)
urls = []
for pasta, inicial, titulo in PAGINAS:
    raiz = "../" if pasta else ""
    url = SITE + (pasta + "/" if pasta else "")
    pagina = (modelo.replace("__RAIZ__", raiz).replace("__INICIAL__", inicial)
                    .replace("__URL__", url).replace("__TITULO__", titulo))
    destino = os.path.join(RAIZ_REPO, pasta, "index.html") if pasta else os.path.join(RAIZ_REPO, "index.html")
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    with open(destino, "w", encoding="utf-8", newline="\n") as f:
        f.write(pagina)
    urls.append(url)
with open(os.path.join(RAIZ_REPO, "sitemap.xml"), "w", encoding="utf-8", newline="\n") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
    for u in urls:
        f.write(f"  <url><loc>{u}</loc></url>\n")
    f.write("</urlset>\n")
print(f"{len(posts)} posts · {len(urls)} páginas geradas · sitemap ok")
