import pandas as pd
import xml.etree.ElementTree as ET

# Caminhos dos arquivos
xml_file = "./Bases_originais/senadores.xml"
csv_file = "./Bases_originais/2022.csv"
csv_output = "./Bases_filtradas/2022_filtrado.csv"

# 1. Ler o XML e extrair os nomes dos senadores
tree = ET.parse(xml_file)
root = tree.getroot()

senadores_info = {}
for parlamentar in root.findall(".//Parlamentar"):
    nome = parlamentar.find(".//NomeParlamentar")
    sexo = parlamentar.find(".//SexoParlamentar")
    partido = parlamentar.find(".//SiglaPartidoParlamentar")
    uf = parlamentar.find(".//UfParlamentar")
    if nome is not None:
        senadores_info[nome.text.strip()] = {
            "Sexo": sexo.text.strip() if sexo is not None else "não definido",
            "Partido": partido.text.strip() if partido is not None else "não declarado",
            "UF": uf.text.strip() if uf is not None else "não declarado"
        }

# 2. Ler o CSV e identificar a coluna de nomes
df = pd.read_csv(csv_file, encoding="utf-8", sep=";")
coluna_nome = "Passageiro"
# 3. Filtrar o DataFrame para manter apenas os senadores
df_filtrado = df[df[coluna_nome].isin(senadores_info.keys())].copy()
df_filtrado["Sexo"] = df_filtrado[coluna_nome].map(lambda nome: senadores_info[nome]["Sexo"])
df_filtrado["Partido"] = df_filtrado[coluna_nome].map(lambda nome: senadores_info[nome]["Partido"])
df_filtrado["UF"]= df_filtrado[coluna_nome].map(lambda nome: senadores_info[nome]["UF"])
df_filtrado.to_csv(csv_output, index=False, encoding="utf-8")

print(f"Arquivo filtrado salvo em: {csv_output}")
