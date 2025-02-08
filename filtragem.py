import pandas as pd
import xml.etree.ElementTree as ET

# Caminhos dos arquivos
xml_file = "./Bases originais/senadores.xml"
csv_file = "./Bases originais/2022.csv"
csv_output = "./Bases filtradas/2022_filtrado.csv"

# 1. Ler o XML e extrair os nomes dos senadores
tree = ET.parse(xml_file)
root = tree.getroot()

senadores = set()
for parlamentar in root.findall(".//Parlamentar"):
    nome = parlamentar.find(".//NomeParlamentar")
    if nome is not None:
        senadores.add(nome.text.strip())

# 2. Ler o CSV e identificar a coluna de nomes
df = pd.read_csv(csv_file, encoding="utf-8", sep=";")

coluna_nomes = "Passageiro"

# 3. Filtrar o DataFrame para manter apenas os senadores
df_filtrado = df[df[coluna_nomes].isin(senadores)]

# 4. Salvar o CSV filtrado
df_filtrado.to_csv(csv_output, index=False, encoding="utf-8")

print(f"Arquivo filtrado salvo em: {csv_output}")
