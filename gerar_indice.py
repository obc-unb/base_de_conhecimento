import subprocess, html, os
from urllib.parse import quote
from collections import defaultdict

dono, repo = os.environ["GITHUB_REPOSITORY"].split("/")
BASE = f"https://{dono.lower()}.github.io/{repo}"

raw = subprocess.check_output(
    ["git", "-c", "core.quotepath=false", "ls-files", "-z"])
arqs = [p for p in raw.decode("utf-8").split("\0")
        if p.lower().endswith((".pdf", ".html")) and p != "index.html"]

grupos = defaultdict(list)
for p in sorted(arqs):
    pasta, _, nome = p.rpartition("/")
    grupos[pasta or "(raiz)"].append((nome, p))

e = html.escape
blocos = []
for pasta in sorted(grupos):
    itens = "\n".join(
        f'    <li><a href="{BASE}/{quote(p)}">{e(n.rsplit(".", 1)[0])}</a></li>'
        for n, p in grupos[pasta])
    blocos.append(f"  <h2>{e(pasta)}</h2>\n  <ul>\n{itens}\n  </ul>")

pagina = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Base de Conhecimento</title>
</head>
<body>
  <h1>Base de Conhecimento</h1>
  <p>Índice dos documentos, organizados por pasta. Total: {len(arqs)} arquivos.</p>
{chr(10).join(blocos)}
</body>
</html>
"""
open("index.html", "w", encoding="utf-8").write(pagina)
