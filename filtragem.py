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
    nome_parlamentar = parlamentar.find(".//NomeParlamentar")
    nome_completo = parlamentar.find(".//NomeCompletoParlamentar")
    sexo = parlamentar.find(".//SexoParlamentar")
    partido = parlamentar.find(".//SiglaPartidoParlamentar")
    uf = parlamentar.find(".//UfParlamentar")

    if nome_parlamentar is not None and nome_parlamentar.text:
        nome_parlamentar = nome_parlamentar.text.strip()
        senadores_info[nome_parlamentar] = {
            "Sexo": sexo.text.strip() if sexo is not None else "não definido",
            "Partido": partido.text.strip() if partido is not None else "não declarado",
            "UF": uf.text.strip() if uf is not None else "não declarado"
        }

    if nome_completo is not None and nome_completo.text:
        nome_completo = nome_completo.text.strip()
        senadores_info[nome_completo] = {
            "Sexo": sexo.text.strip() if sexo is not None else "não definido",
            "Partido": partido.text.strip() if partido is not None else "não declarado",
            "UF": uf.text.strip() if uf is not None else "não declarado"
        }

# 2. Ler o CSV
df = pd.read_csv(csv_file, encoding="utf-8", sep=";", dtype=str)
df.columns = df.columns.str.strip()

df.rename(columns={
    "Tipo de Servi�o": "Tipo de Serviço",
    "Multa/Remarca��o": "Multa/Remarcação",
    "GRU / Diferen�a Tarif�ria": "GRU / Diferença Tarifária",
    "Tx.de Embarque": "Taxa de Embarque",
    "***Desconto Contratual 0,04%": "Desconto Contratual 0,04%",
    "Data do Cancelamento/ Remarca��o": "Data do Cancelamento/Remarcação",
    "GRU / UPGRADE de  \n0    Classe": "GRU / Upgrade de Classe",
    "Valor do Ree...": "Valor do Reembolso",
    "Custo Efetivo SF": "Custo Efetivo Senado Federal"
}, inplace=True)

# 3. Excluir linhas onde 'Tipo de serviço' é 'Seguro Viagem'
df = df[df["Tipo de Serviço"] != "Seguro Viagem"]

# 4. Corrigir Valores

# df["Tarifa"] = df["Tarifa"].fillna("").astype(str).str.strip() + df["Unnamed: 9"].fillna("").astype(str).str.strip()
# df.drop(columns=["Unnamed: 9"], inplace=True)


# df["Taxa de Embarque"] = df["Taxa de Embarque"].fillna("").astype(str).str.strip() + df["Unnamed: 11"].fillna("").astype(str).str.strip()
# df.drop(columns=["Unnamed: 11"], inplace=True)


# df["Multa/Remarcação"] = df["Multa/Remarcação"].fillna("").astype(str).str.strip() + df["Unnamed: 13"].fillna("").astype(str).str.strip()
# df.drop(columns=["Unnamed: 13"], inplace=True)


# df["Total"] = df["Total"].fillna("").astype(str).str.strip() + df["Unnamed: 15"].fillna("").astype(str).str.strip()
# df.drop(columns=["Unnamed: 15"], inplace=True)


# df["Desconto Contratual 0,04%"] = df["Desconto Contratual 0,04%"].fillna("").astype(str).str.strip() + df["Unnamed: 19"].fillna("").astype(str).str.strip()
# df.drop(columns=["Unnamed: 19", "Unnamed: 17"], inplace=True)


# df["Total com Desconto"] = df["Total com Desconto"].fillna("").astype(str).str.strip() + df["Unnamed: 21"].fillna("").astype(str).str.strip()
# df.drop(columns=["Unnamed: 21", "Unnamed: 24"], inplace=True)


# df["GRU / Diferença Tarifária"] = df["GRU / Diferença Tarifária"].fillna("").astype(str).str.strip() + df["Unnamed: 26"].fillna("").astype(str).str.strip()
# df.drop(columns=["Unnamed: 26"], inplace=True)


# df["Valor do Reembolso"] = df["Valor do Reembolso"].fillna("").astype(str).str.strip() + df["Unnamed: 28"].fillna("").astype(str).str.strip()
# df.drop(columns=["Unnamed: 28"], inplace=True)


# df["Custo Efetivo Senado Federal"] = df["Custo Efetivo Senado Federal"].fillna("").astype(str).str.strip() + df["Unnamed: 30"].fillna("").astype(str).str.strip()
# df.drop(columns=["Unnamed: 30", "Unnamed: 31"], inplace=True)

# df["Data de volta"] = df["Unnamed: 7"].fillna("").astype(str).str.strip()
# df.drop(columns=["Unnamed: 7"], inplace=True)

# 5. Filtrar o DataFrame para manter apenas os senadores (considerando NomeParlamentar e NomeCompletoParlamentar)
coluna_nome = "Passageiro"
df_filtrado = df[df[coluna_nome].isin(senadores_info.keys())].copy()

# 6. Adicionar informações adicionais (Sexo, Partido, UF)
df_filtrado["Sexo"] = df_filtrado[coluna_nome].map(lambda nome: senadores_info[nome]["Sexo"])
df_filtrado["Partido"] = df_filtrado[coluna_nome].map(lambda nome: senadores_info[nome]["Partido"])
df_filtrado["UF"] = df_filtrado[coluna_nome].map(lambda nome: senadores_info[nome]["UF"])

# 7. Salvar o CSV filtrado
df_filtrado.to_csv(csv_output, index=False, encoding="utf-8")
print(f"Arquivo filtrado salvo em: {csv_output}")
