import xml.etree.ElementTree as ET
import unicodedata

def remover_acentos(texto):
    return ''.join(c for c in unicodedata.normalize('NFKD', texto) if not unicodedata.combining(c))

def processar_xml(arquivo_entrada, arquivo_saida):
    tree = ET.parse(arquivo_entrada)
    root = tree.getroot()
    
    nomes_unicos = set()
    parlamentares = root.find(".//Parlamentares")
    
    if parlamentares is not None:
        for parlamentar in list(parlamentares):
            nome_elemento = parlamentar.find(".//NomeParlamentar")
            if nome_elemento is not None:
                nome_sem_acentos = remover_acentos(nome_elemento.text)
                
                if nome_sem_acentos in nomes_unicos:
                    parlamentares.remove(parlamentar)
                else:
                    nomes_unicos.add(nome_sem_acentos)
                    nome_elemento.text = nome_sem_acentos
    
    tree.write(arquivo_saida, encoding="utf-8", xml_declaration=True)
    print(f"Arquivo processado e salvo como {arquivo_saida}")

# Exemplo de uso
processar_xml("Bases_originais/senadores.xml", "Bases_originais/senadores2.xml")
