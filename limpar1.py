import os
import pandas as pd
from distrito_federal_setor import setores

# Caminho para o arquivo Excel
caminho_arquivo = (
    r"D:\Estágio - TRIM\arquivos sujos\Imóveis comerciais_Bsb_ago22_Parte1.xlsx"
)

# Extrair o nome do arquivo sem a extensão
nome_arquivo, extensao_arquivo = os.path.splitext(os.path.basename(caminho_arquivo))

# Carregando o arquivo Excel em um DataFrame
df = pd.read_excel(caminho_arquivo)

# Verificar e remover imóveis duplicados com base no conteúdo do link
duplicados = df[df.duplicated(subset=["Link"])]

# Se houver imóveis duplicados, remova-os
if not duplicados.empty:
    print("Imóveis duplicados encontrados. Removendo...")
    df.drop_duplicates(subset=["Link"], inplace=True)
    print("Imóveis duplicados removidos com sucesso.")

# Verificar se há imóveis com "Área" igual a zero
area_zero = df[df["Área"] == 0 | (df["Área"].isnull())]

# Se houver imóveis com "Área" igual a zero, exclua-os
if not area_zero.empty:
    print("Imóveis com 'Área' igual a zero encontrados. Removendo...")
    df.drop(area_zero.index, inplace=True)
    print("Imóveis com 'Área' igual a zero removidos com sucesso.")

# Verificar se há imóveis com "Preço" igual a zero
preco_zero = df[df["Preço"] == 0 | (df["Preço"].isnull())]

# Se houver imóveis com "Preço" igual a zero, exclua-os
if not preco_zero.empty:
    print("Imóveis com 'Preço' igual a zero encontrados. Removendo...")
    df.drop(preco_zero.index, inplace=True)
    print("Imóveis com 'Preço' igual a zero removidos com sucesso.")


# Função para extrair o setor da string de título
def extrair_setor(titulo):
    if isinstance(titulo, str):  # Verifica se o valor é uma string
        palavras = titulo.split()
        palavras_upper = [palavra.upper() for palavra in palavras]
        for palavra in palavras_upper:
            if palavra in setores:
                return palavra
    return "OUTRO"  # Retorna "OUTRO" se o valor não for uma string


df["Setor"] = df["Endereço"].apply(extrair_setor)

# Convertendo as colunas "Preço" e "Área" para numéricos
df["Preço"] = pd.to_numeric(df["Preço"], errors="coerce")
df["Área"] = pd.to_numeric(df["Área"], errors="coerce")

# Remover linhas onde "Preço" ou "Área" é NaN após a conversão
df = df.dropna(subset=["Preço", "Área"])

# Criando uma nova coluna 'M2' que é o resultado da divisão da coluna 'Preço' pela coluna 'Área'
df["M2"] = df["Preço"] / df["Área"]

# Salvar o DataFrame modificado no caminho desejado
caminho_arquivo_modificado = os.path.join(
    r"D:\Estágio - TRIM\arquivos limpos", f"{nome_arquivo}_limpo{extensao_arquivo}"
)
df.to_excel(caminho_arquivo_modificado, index=False)

print("Arquivo salvo com sucesso em:", caminho_arquivo_modificado)

# Exibindo as primeiras linhas do DataFrame com as novas colunas de amenidades
print(df.head())
