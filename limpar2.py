import os
import pandas as pd
from distrito_federal_setor import setores

# Caminho para o arquivo Excel
caminho_arquivo = r"D:\Estágio - TRIM\arquivos sujos\Salas Comerciais à venda em BSB_VivaReal_Ago2022.xlsx"

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


# Criar uma lista com todas as amenidades
amenidades = [
    "Desnível para frente (rua)",
    "Desnível para trás (fundo)",
    "Espaço gourmet",
    "Plano",
    "Elevador",
    "Playground",
    "Ar-condicionado",
    "Rede de água e esgoto",
    "Câmera de segurança",
    "Pomar",
    "Salão de festas",
    "Academia",
    "Casa sede",
    "Arenoso",
    "Argiloso",
    "Árvore Frutífera",
    "Bicicletário",
    "Churrasqueira",
    "Condomínio Fechado",
    "Conexão à internet",
    "Energia elétrica",
    "Espaço Verde / Parque",
    "Frente para o leste",
    "Frente para o norte",
    "Frente para o sul",
    "Frente para o oeste",
    "Jardim",
    "Piscina",
    "Portaria 24h",
    "TV a cabo",
    "Rua asfaltada",
    "Portão eletrônico",
    "Poço artesiano",
    "Estacionamento",
    "Cozinha",
    "Acesso para deficientes",
    "Banheiro de serviço",
    "Interfone",
    "Armário embutido",
    "Garagem",
    "Condomínio fechado",
    "Vista para lago",
    "Conexão à internet",
    "Lavanderia",
    "Armário no banheiro",
    "Ambientes integrados",
    "Circuito de segurança",
    "Escritório",
]

# Criar colunas para cada amenidade e inicializá-las com 0
for amenidade in amenidades:
    df[amenidade] = 0

# Preencher as novas colunas com 1 onde a informação correspondente existir nas colunas originais
for coluna in df.columns:
    if coluna.startswith("Atributo 1"):
        for amenidade in amenidades:
            df[amenidade] = df[amenidade] | df[coluna].astype(str).str.contains(
                amenidade, case=False, regex=False
            )

# Substituir "True" por 1 e "False" por 0 nas novas colunas de amenidades
for amenidade in amenidades:
    df[amenidade] = df[amenidade].replace({True: 1, False: 0})

# Remover as colunas originais de amenities
colunas_para_remover = [
    "Atributo 1",
    "Atributo 2",
    "Atributo 3",
    # "property-card__amenities",
    # "property-card__amenities1",
    # "property-card__amenities2",
    # "property-card__amenities3",
    # "property-card__amenities4",
]
df.drop(columns=colunas_para_remover, inplace=True)

# Salvar o DataFrame modificado no caminho desejado
caminho_arquivo_modificado = os.path.join(
    r"D:\Estágio - TRIM\arquivos limpos", f"{nome_arquivo}_limpo{extensao_arquivo}"
)
df.to_excel(caminho_arquivo_modificado, index=False)

print("Arquivo salvo com sucesso em:", caminho_arquivo_modificado)

# Exibindo as primeiras linhas do DataFrame com as novas colunas de amenidades
print(df.head())
