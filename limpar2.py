import os
import pandas as pd
from distrito_federal_setor import setores

# Caminho para o arquivo Excel
caminho_arquivo = (
    r"D:\Estágio - TRIM\arquivos sujos\Apartamentos a venda_Viva Real_2q_11_09.xlsx"
)

# Extrair o nome do arquivo sem a extensão
nome_arquivo, extensao_arquivo = os.path.splitext(os.path.basename(caminho_arquivo))

# Carregando o arquivo Excel em um DataFrame
df = pd.read_excel(caminho_arquivo)

# Verificar se há imóveis com "Preço" igual a zero ou nulo
preco_zero_null = df["Preço"].isnull() | (df["Preço"] == 0)

# Remover imóveis com "Preço" igual a zero ou nulo
df = df[~preco_zero_null]

# Verificar se há imóveis com "Área" igual a zero ou nula
area_zero_null = df["Área"].isnull() | (df["Área"] == 0)

# Remover imóveis com "Área" igual a zero ou nula
df = df[~area_zero_null]

# Verificar se há imóveis com "Preço" igual a "Sob Consulta"
if (
    "Preço" in df.columns and df["Preço"].dtype == object
):  # Verifica se a coluna existe e é do tipo objeto (string)
    df = df[
        ~(df["Preço"].str.lower() == "sob consulta")
    ]  # Remove linhas com "Sob Consulta" na coluna "Preço"

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
    "Academia",
    "Churrasqueira",
    "Cinema",
    "Espaço gourmet",
    "Espaço verde / Parque",
    "Gramado",
    "Jardim",
    "Piscina",
    "Playground",
    "Quadra de squash",
    "Quadra de tênis",
    "Quadra poliesportiva",
    "Quintal",
    "Salão de festas",
    "Salão de jogos",
    "Aceita animais",
    "Aquecimento",
    "Ar-condicionado",
    "Conexão à internet",
    "Depósito",
    "Elevador",
    "Garagem",
    "Lavanderia",
    "Mobiliado",
    "Recepção",
    "Sauna",
    "Spa",
    "TV a cabo",
    "Circuito de segurança",
    "Condomínio fechado",
    "Interfone",
    "Segurança 24h",
    "Sistema de alarme",
    "Vigia",
    "Área de serviço",
    "Cozinha",
    "Escritório",
    "Varanda",
    "Varanda gourmet",
    "Desnível para frente (rua)",
    "Desnível para trás (fundo)",
    "Rede de água e esgoto",
    "Câmera de segurança",
    "Pomar",
    "Casa sede",
    "Arenoso",
    "Argiloso",
    "Árvore Frutífera",
    "Bicicletário",
    "Frente para o leste",
    "Frente para o norte",
    "Frente para o sul",
    "Frente para o oeste",
    "Portaria 24h",
    "Rua asfaltada",
    "Portão eletrônico",
    "Poço artesiano",
    "Estacionamento",
    "Acesso para deficientes",
    "Banheiro de serviço",
    "Armário embutido",
    "Vista para lago",
    "Ambientes integrados",
]

# Criar colunas para cada amenidade e inicializá-las com 0
for amenidade in amenidades:
    df[amenidade] = 0

# Preencher as novas colunas com 1 onde a informação correspondente existir nas colunas originais
for coluna in df.columns:
    if coluna.startswith("A"):
        for amenidade in amenidades:
            df[amenidade] = df[amenidade] | df[coluna].astype(str).str.contains(
                amenidade, case=False, regex=False
            )

# Substituir "True" por 1 e "False" por 0 nas novas colunas de amenidades
for amenidade in amenidades:
    df[amenidade] = df[amenidade].replace({True: 1, False: 0})

# Remover as colunas originais de amenities
colunas_para_remover = [
    "A",
    "B",
    "C",
    "D",
    "E",
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
