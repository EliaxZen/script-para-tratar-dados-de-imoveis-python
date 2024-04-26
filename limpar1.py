import os
import pandas as pd
from distrito_federal_setor import setores

# Caminho para o arquivo Excel
caminho_arquivo = r"D:\Estágio - TRIM\arquivos sujos\Imoveis a Venda_DF_Nov22.xlsx"

# Extrair o nome do arquivo sem a extensão
nome_arquivo, extensao_arquivo = os.path.splitext(os.path.basename(caminho_arquivo))

# Carregando o arquivo Excel em um DataFrame
df = pd.read_excel(caminho_arquivo)

# Verificar e remover imóveis duplicados com base no conteúdo do link
df.drop_duplicates(subset=["Link"], inplace=True)

# Verificar se há imóveis com "Preço" igual a zero ou nulo
preco_zero_null = df["Preço"].isnull() | (df["Preço"] == 0)

# Remover imóveis com "Preço" igual a zero ou nulo
df = df[~preco_zero_null]

# Verificar se há imóveis com "Área" igual a zero ou nula
area_zero_null = df["Área"].isnull() | (df["Área"] == 0)

# Remover imóveis com "Área" igual a zero ou nula
df = df[~area_zero_null]

# Remover imóveis com "Preço" igual a "Sob Consulta"
df = df[~(df["Preço"].str.lower() == "sob consulta")]

# Remover caracteres não numéricos da coluna "Preço" e converter para numérico
df["Preço"] = pd.to_numeric(
    df["Preço"].apply(lambda x: "".join(filter(str.isdigit, str(x)))), errors="coerce"
)


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
