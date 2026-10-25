# nud-lab

O caderno de laboratório da whatevertr: os logs, as ideias e o que eu vou aprendendo construindo com IA.

No ar em **https://whatevertr.github.io/nud-lab** (GitHub Pages, a partir da `main`).

> 🚧 **Em andamento** (*work in progress*): o blog está sendo construído em público e muda o tempo todo.

- **Diário de Bordo:** os posts dos meus tumblrs (o whatever-log e o NUD), reunidos aqui na ordem das datas. Os tumblrs ficam no ar, parados; os posts novos nascem aqui.
- **Noa:** os ensaios estão sendo refeitos.
- **NUD.FM:** os discos.

## Como mexer
O site inteiro sai de uma página-modelo só, o `_modelo.html`. Cada capítulo vira uma pasta própria (`/diario/`, `/noa/`, `/nudfm/`, `/sobre/`), pro Google enxergar cada um, e o menu troca o conteúdo sem recarregar. Pra mudar qualquer coisa: edite o `_modelo.html` e rode `python _ferramentas/gerar_paginas.py`. Nunca edite os `index.html` gerados à mão. (Arquivos e pastas que começam com `_` não são publicados pelo GitHub Pages.)
