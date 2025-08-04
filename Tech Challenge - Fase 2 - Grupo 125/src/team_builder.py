import pandas as pd
def validar_time(time):
    """
    Verifica se o time tem pelo menos 1 goleiro e 10 jogadores de linha.
    Usa a coluna 'Posição Principal' (Preffered_Position no CSV).
    """
    position_mapping = {
        'GK': 'Goalkeeper',
        # Defensores
        'CB': 'DEF', 'LCB': 'DEF', 'RCB': 'DEF', 'LB': 'DEF', 'RB': 'DEF',
        'LWB': 'DEF', 'RWB': 'DEF',
        # Meias
        'CM': 'MEI', 'RCM': 'MEI', 'LCM': 'MEI', 'CAM': 'MEI', 'RAM': 'MEI', 'LAM': 'MEI',
        'LM': 'MEI', 'RM': 'MEI', 'CDM': 'MEI', 'RDM': 'MEI', 'LDM': 'MEI',
        # Atacantes
        'ST': 'ATA', 'CF': 'ATA', 'LS': 'ATA', 'RS': 'ATA',
        'LW': 'ATA', 'RW': 'ATA', 'LF': 'ATA', 'RF': 'ATA'
    }

    position_counts = {'Goalkeeper': 0, 'DEF': 0, 'MEI': 0, 'ATA': 0}

    for jogador in time.values():
        # Usa 'Posição Principal' (coluna 15) que veio do 'Preffered_Position'
        posicao = str(jogador.get('Posição Principal', '')).strip()
        
        # Divide posições compostas (ex: "CB/LB" -> ["CB", "LB"])
        posicoes = [p.strip() for p in posicao.split('/')] if '/' in posicao else [posicao]

        for p in posicoes:
            if p in position_mapping:
                general_position = position_mapping[p]
                position_counts[general_position] += 1
                break  # Adiciona apenas uma vez

    # Requisitos mínimos
    return position_counts['Goalkeeper'] >= 1 and sum(position_counts.values()) >= 11


def calcular_fitness(time, formation_target=None):
    """
    Calcula o fitness com base no rating total e penalidades por desvio da formação.
    """
    if not validar_time(time):
        return 0

    position_mapping = {
        'GK': 'Goalkeeper',
        'CB': 'DEF', 'LCB': 'DEF', 'RCB': 'DEF', 'LB': 'DEF', 'RB': 'DEF',
        'LWB': 'DEF', 'RWB': 'DEF',
        'CM': 'MEI', 'RCM': 'MEI', 'LCM': 'MEI', 'CAM': 'MEI', 'RAM': 'MEI', 'LAM': 'MEI',
        'LM': 'MEI', 'RM': 'MEI', 'CDM': 'MEI', 'RDM': 'MEI', 'LDM': 'MEI',
        'ST': 'ATA', 'CF': 'ATA', 'LS': 'ATA', 'RS': 'ATA',
        'LW': 'ATA', 'RW': 'ATA', 'LF': 'ATA', 'RF': 'ATA'
    }

    position_counts = {'Goalkeeper': 0, 'DEF': 0, 'MEI': 0, 'ATA': 0}
    total_rating = 0.0

    for jogador in time.values():
        rating = jogador.get('Rating', 0)
        if pd.notna(rating):
            total_rating += float(rating)

        posicao = str(jogador.get('Posição Principal', '')).strip()
        posicoes = [p.strip() for p in posicao.split('/')] if '/' in posicao else [posicao]

        for p in posicoes:
            if p in position_mapping:
                general_position = position_mapping[p]
                position_counts[general_position] += 1
                break

    # Formação alvo (padrão: 4-3-3)
    if formation_target is None:
        formation_target = {'Goalkeeper': 1, 'DEF': 4, 'MEI': 3, 'ATA': 3}

    # Penalidade por desvio da formação
    penalty = 0
    for pos, target in formation_target.items():
        actual = position_counts.get(pos, 0)
        penalty += abs(actual - target) * 50

    # Penalidade se não tiver 11 jogadores
    if len(time) != 11:
        penalty += abs(len(time) - 11) * 100

    return max(0, total_rating - penalty)