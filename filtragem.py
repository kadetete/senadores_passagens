import pandas as pd
import xml.etree.ElementTree as ET

# Caminhos dos arquivos
xml_file = "./Bases_originais/senadores.xml"
csv_file = "./Bases_originais/2021.csv"
csv_output = "./Bases_filtradas/2021_filtrado.csv"

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

# 2. Ler o CSV
df = pd.read_csv(csv_file, encoding="utf-8", sep=";", dtype=str)
df.columns = df.columns.str.strip() 

# 3. Excluir linhas onde 'Tipo de serviço' é 'Seguro Viagem'
df = df[df["Tipo de Servi�o"] != "Seguro Viagem"]

#4. Corrigir Valores

# if not df["Unnamed: 9"].isnull():
#     df["Tarifa"] = df["Tarifa"].fillna("").astype(str).str.strip() + df["Unnamed: 9"].fillna("").astype(str).str.strip()
#     df.drop(columns=["Unnamed: 9"], inplace=True)

# if not df["Unnamed: 11"].isnull():
#     df["Tx.de Embarque"] = df["Tx.de Embarque"].fillna("").astype(str).str.strip() + df["Unnamed: 11"].fillna("").astype(str).str.strip()
#     df.drop(columns=["Unnamed: 11"], inplace=True)

# if not df["Unnamed: 13"].isnull():
#     df["Multa/Remarca��o"] = df["Multa/Remarca��o"].fillna("").astype(str).str.strip() + df["Unnamed: 13"].fillna("").astype(str).str.strip()
#     df.drop(columns=["Unnamed: 13"], inplace=True)

# if not df["Unnamed: 15"].isnull():
#     df["Total"] = df["Total"].fillna("").astype(str).str.strip() + df["Unnamed: 15"].fillna("").astype(str).str.strip()
#     df.drop(columns=["Unnamed: 15"], inplace=True)

# if not df["Unnamed: 19"].isnull():
#     df["***Desconto Contratual 0,04%"] = df["***Desconto Contratual 0,04%"].fillna("").astype(str).str.strip() + df["Unnamed: 19"].fillna("").astype(str).str.strip()
#     df.drop(columns=["Unnamed: 19", "Unnamed: 17"], inplace=True)

# if not df["Unnamed: 21"].isnull():
#     df["Total com Desconto"] = df["Total com Desconto"].fillna("").astype(str).str.strip() + df["Unnamed: 21"].fillna("").astype(str).str.strip()
#     df.drop(columns=["Unnamed: 21", "Unnamed: 24"], inplace=True)

# if not df["Unnamed: 26"].isnull():
#     df["GRU / Diferen�a Tarif�ria"] = df["GRU / Diferen�a Tarif�ria"].fillna("").astype(str).str.strip() + df["Unnamed: 26"].fillna("").astype(str).str.strip()
#     df.drop(columns=["Unnamed: 26"], inplace=True)

# if not df["Unnamed: 28"].isnull():
#     df["Valor do Reembolso"] = df["Valor do Reembolso"].fillna("").astype(str).str.strip() + df["Unnamed: 28"].fillna("").astype(str).str.strip()
#     df.drop(columns=["Unnamed: 28"], inplace=True)

# if not df["Unnamed: 30"].isnull():
#     df["Custo Efetivo SF"] = df["Custo Efetivo SF"].fillna("").astype(str).str.strip() + df["Unnamed: 30"].fillna("").astype(str).str.strip()
#     df.drop(columns=["Unnamed: 30", "Unnamed: 31"], inplace=True)


# 5. Filtrar o DataFrame para manter apenas os senadores
coluna_nome = "Passageiro"
df_filtrado = df[df[coluna_nome].isin(senadores_info.keys())].copy()
df_filtrado["Sexo"] = df_filtrado[coluna_nome].map(lambda nome: senadores_info[nome]["Sexo"])
df_filtrado["Partido"] = df_filtrado[coluna_nome].map(lambda nome: senadores_info[nome]["Partido"])
df_filtrado["UF"] = df_filtrado[coluna_nome].map(lambda nome: senadores_info[nome]["UF"])

# 6. Salvar o CSV filtrado
df_filtrado.to_csv(csv_output, index=False, encoding="utf-8")
print(f"Arquivo filtrado salvo em: {csv_output}")
