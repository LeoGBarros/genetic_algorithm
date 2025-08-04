import pandas as pd
def carregar_dados(caminho):
    colunas = ['Nome', 'Rating', 'Posição Principal']

    df = pd.read_csv(caminho, header=None, names=colunas, low_memory=False, sep=';')

    #numérico e removendo linhas com valores inválidos
    df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce')
    df.dropna(subset=['Rating'], inplace=True)
    
    return df.to_dict('records')