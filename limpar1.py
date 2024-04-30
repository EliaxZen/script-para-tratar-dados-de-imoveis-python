import os
import re

import numpy as np
import pandas as pd

from distrito_federal_setor import setores

caminho_arquivo = r"D:\Estágio - TRIM\arquivos sujos\Goias\2024-2-13-9-11-35-411235389769300-35.042 Imóveis à venda em GO -Part 3.xlsx"

nome_arquivo, extensao_arquivo = os.path.splitext(os.path.basename(caminho_arquivo))

df = pd.read_excel(caminho_arquivo)

#df["Área"] = pd.to_numeric(df["Área"].str.replace(" m²", ""), errors="coerce")


if "Preço" in df.columns and df["Preço"].dtype == object:
    df = df[~(df["Preço"].str.lower() == "sob consulta")]


df["Preço"] = pd.to_numeric(
    df["Preço"].apply(lambda x: "".join(filter(str.isdigit, str(x)))), errors="coerce"
)


def extrair_max_quartos(texto):
    if isinstance(texto, str):
        quartos_matches = re.findall(
            r"(\d+)\s*quarto|(\d+)\s*quartos", texto, flags=re.IGNORECASE
        )
        if quartos_matches:

            quartos_int = [int(quarto) for quarto in sum(quartos_matches, ()) if quarto]
            if quartos_int:
                return max(quartos_int)
    return np.nan


def extrair_max_suites(texto):
    if isinstance(texto, str):
        suites_matches = re.findall(
            r"(\d+)\s*suíte|(\d+)\s*suítes", texto, flags=re.IGNORECASE
        )
        if suites_matches:
            suites_int = [int(suite) for suite in sum(suites_matches, ()) if suite]
            if suites_int:
                return max(suites_int)
    return np.nan


def extrair_max_banheiros(texto):
    if isinstance(texto, str):
        banheiros_matches = re.findall(
            r"(\d+)\s*banheiro|(\d+)\s*banheiros", texto, flags=re.IGNORECASE
        )
        if banheiros_matches:

            banheiros_int = [
                int(banheiro) for banheiro in sum(banheiros_matches, ()) if banheiro
            ]
            if banheiros_int:
                return max(banheiros_int)  # Retornar o máximo
    return np.nan  # Retorna NaN se não houver correspondências


# Função para extrair e contar o número máximo de vagas de estacionamento
def extrair_max_vagas(texto):
    if isinstance(texto, str):  # Verifica se o valor é uma string
        vagas_matches = re.findall(
            r"(\d+)\s*vaga|(\d+)\s*vagas", texto, flags=re.IGNORECASE
        )
        if vagas_matches:
            # Filtrar valores não vazios e converter para inteiro
            vagas_int = [int(vaga) for vaga in sum(vagas_matches, ()) if vaga]
            if vagas_int:  # Verificar se há valores não vazios
                return max(vagas_int)  # Retornar o máximo
    return np.nan  # Retorna NaN se não houver correspondências


# Função para extrair e contar o número máximo de plantas
def extrair_max_plantas(texto):
    if isinstance(texto, str):  # Verifica se o valor é uma string
        plantas_matches = re.findall(
            r"(\d+)\s*planta|(\d+)\s*plantas", texto, flags=re.IGNORECASE
        )
        if plantas_matches:
            # Filtrar valores não vazios e converter para inteiro
            plantas_int = [int(planta) for planta in sum(plantas_matches, ()) if planta]
            if plantas_int:  # Verificar se há valores não vazios
                return max(plantas_int)  # Retornar o máximo
    return np.nan  # Retorna NaN se não houver correspondências


# # Extrair e contabilizar o número máximo de quartos
# df["Quartos"] = df["new-details-ul"].apply(extrair_max_quartos)
# df["Quartos"] = df["Quartos"].fillna(df["new-details-ul1"].apply(extrair_max_quartos))
# df["Quartos"] = df["Quartos"].fillna(df["new-details-ul2"].apply(extrair_max_quartos))
# df["Quartos"] = df["Quartos"].fillna(df["new-details-ul3"].apply(extrair_max_quartos))
# df["Quartos"] = df["Quartos"].fillna(df["new-details-ul4"].apply(extrair_max_quartos))
# df["Quartos"] = df["Quartos"].astype(float)
df["Quartos"] = df["Quartos"].fillna(0)

# # Extrair e contabilizar o número máximo de suítes
# df["Suítes"] = df["new-details-ul"].apply(extrair_max_suites)
# df["Suítes"] = df["Suítes"].fillna(df["new-details-ul1"].apply(extrair_max_suites))
# df["Suítes"] = df["Suítes"].fillna(df["new-details-ul2"].apply(extrair_max_suites))
# df["Suítes"] = df["Suítes"].fillna(df["new-details-ul3"].apply(extrair_max_suites))
# df["Suítes"] = df["Suítes"].fillna(df["new-details-ul4"].apply(extrair_max_suites))
# df["Suítes"] = df["Suítes"].astype(float)
df["Suítes"] = df["Suítes"].fillna(0)

# # Extrair e contabilizar o número máximo de banheiros
# df["Banheiros"] = df["new-details-ul"].apply(extrair_max_banheiros)
# df["Banheiros"] = df["Banheiros"].fillna(
#     df["new-details-ul1"].apply(extrair_max_banheiros)
# )
# df["Banheiros"] = df["Banheiros"].fillna(
#     df["new-details-ul2"].apply(extrair_max_banheiros)
# )
# df["Banheiros"] = df["Banheiros"].fillna(
#     df["new-details-ul3"].apply(extrair_max_banheiros)
# )
# df["Banheiros"] = df["Banheiros"].fillna(
#     df["new-details-ul4"].apply(extrair_max_banheiros)
# )
# df["Banheiros"] = df["Banheiros"].astype(float)
#df["Banheiros"] = df["Banheiros"].fillna(0)

# # Extrair e contabilizar o número máximo de vagas de estacionamento
# df["Vagas"] = df["new-details-ul"].apply(extrair_max_vagas)
# df["Vagas"] = df["Vagas"].fillna(df["new-details-ul1"].apply(extrair_max_vagas))
# df["Vagas"] = df["Vagas"].fillna(df["new-details-ul2"].apply(extrair_max_vagas))
# df["Vagas"] = df["Vagas"].fillna(df["new-details-ul3"].apply(extrair_max_vagas))
# df["Vagas"] = df["Vagas"].fillna(df["new-details-ul4"].apply(extrair_max_vagas))
# df["Vagas"] = df["Vagas"].astype(float)
df["Vagas"] = df["Vagas"].fillna(0)

# # Extrair e contabilizar o número máximo de plantas
# df["Plantas"] = df["new-details-ul"].apply(extrair_max_plantas)
# df["Plantas"] = df["Plantas"].fillna(df["new-details-ul1"].apply(extrair_max_plantas))
# df["Plantas"] = df["Plantas"].fillna(df["new-details-ul2"].apply(extrair_max_plantas))
# df["Plantas"] = df["Plantas"].fillna(df["new-details-ul3"].apply(extrair_max_plantas))
# df["Plantas"] = df["Plantas"].fillna(df["new-details-ul4"].apply(extrair_max_plantas))
# df["Plantas"] = df["Plantas"].astype(float)
#df["Plantas"] = df["Plantas"].fillna(0)


# Função para extrair o setor da string de título
def extrair_setor(titulo):
    if isinstance(titulo, str):  # Verifica se o valor é uma string
        palavras = titulo.split()
        palavras_upper = [palavra.upper() for palavra in palavras]
        for palavra in palavras_upper:
            if palavra in setores:
                return palavra
    return "OUTRO"  # Retorna "OUTRO" se o valor não for uma string


df["Setor"] = df["Título"].apply(extrair_setor)


# Convertendo as colunas "Área" e "Preço" para numéricos
df["Área"] = pd.to_numeric(df["Área"], errors="coerce")

# Remover linhas onde "Área" é NaN após a conversão
df = df.dropna(subset=["Área"])

# Verificar se há valores vazios nas colunas "Preço" e "Área" e excluir as linhas correspondentes
df = df.dropna(subset=["Preço", "Área"])

# Verificar se há imóveis com "Preço" igual a zero ou nulo
preco_zero_null = df["Preço"].isnull() | (df["Preço"] == 0)

# Remover imóveis com "Preço" igual a zero ou nulo
df = df[~preco_zero_null]

# Verificar se há imóveis com "Área" igual a zero ou nula
area_zero_null = df["Área"].isnull() | (df["Área"] == 0)

# Remover imóveis com "Área" igual a zero ou nula
df = df[~area_zero_null]


# Função para extrair o tipo do imóvel do link
def extrair_tipo(link):
    if "apartamento" in link:
        return "Apartamento"
    elif "casa" in link:
        return "Casa"
    elif "casa-condominio" in link:
        return "Casa Condomínio"
    elif "galpo" in link:
        return "Galpão"
    elif "garagem" in link:
        return "Garagem"
    elif "hotel-flat" in link:
        return "Flat"
    elif "flat" in link:
        return "Flat"
    elif "kitnet" in link:
        return "Kitnet"
    elif "loja" in link:
        return "Loja"
    elif "loteamento" in link:
        return "Loteamento"
    elif "lote-terreno" in link:
        return "Lote Terreno"
    elif "ponto-comercial" in link:
        return "Ponto Comercial"
    elif "prdio" in link or "predio" in link:
        return "Prédio"
    elif "sala" in link:
        return "Sala"
    elif "rural" in link:
        return "Zona Rural"
    elif "lancamento" in link:
        return "Lançamento"
    else:
        return "OUTROS"


# Adicionar uma coluna 'Tipo do Imóvel' ao DataFrame e preenchê-la com os tipos extraídos dos links
df["Tipo"] = df["Link"].apply(extrair_tipo)

# Criando uma nova coluna 'M2' que é o resultado da divisão da coluna 'Preço' pela coluna 'Área'
df["M2"] = df["Preço"] / df["Área"]

# Salvar o DataFrame modificado no caminho desejado
caminho_arquivo_modificado = os.path.join(
    r"D:\Estágio - TRIM\arquivos limpos", f"{nome_arquivo}_limpo{extensao_arquivo}"
)
df.to_excel(caminho_arquivo_modificado, index=False)

print("\nArquivo salvo com sucesso em:", caminho_arquivo_modificado)

# Exibindo as primeiras linhas do DataFrame com as novas colunas de amenidades
print(df.head())
