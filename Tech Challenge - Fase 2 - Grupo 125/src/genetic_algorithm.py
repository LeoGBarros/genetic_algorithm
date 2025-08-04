import random
# Importamos calcular_fitness apenas se for necessário dentro deste arquivo
# Mas como está no team_builder, e o crossover/mutacao usam o time, pode não ser preciso aqui
# A validação pode ser feita em team_builder tambem
# from src.team_builder import calcular_fitness # Removido se não for usado aqui diretamente

# Formações suportadas
FORMACOES = {
    "4-4-2": {"GK": 1, "DEF": 4, "MEI": 4, "ATA": 2},
    "4-3-3": {"GK": 1, "DEF": 4, "MEI": 3, "ATA": 3},
    "3-5-2": {"GK": 1, "DEF": 3, "MEI": 5, "ATA": 2},
    "5-3-2": {"GK": 1, "DEF": 5, "MEI": 3, "ATA": 2}
}

def agrupar_por_posicao(jogadores):
    """
    Agrupa jogadores por posição útil usando 'Posição Principal'.
    Ex: 'CB/LB' -> pode ser CB ou LB.
    """
    grupos = {
        'GK': [],
        'CB': [], 'RB': [], 'LB': [],
        'CM': [], 'CAM': [], 'RM': [], 'LM': [],
        'ST': [], 'LW': [], 'RW': []
    }
    for jogador in jogadores:
        pos_principal = jogador.get('Posição Principal', '')
        if not pos_principal or pos_principal == '':
            continue
        # Divide posições compostas (ex: 'CB/LB' -> ['CB', 'LB'])
        posicoes = [p.strip() for p in pos_principal.split('/') if p.strip()]
        for pos in posicoes:
            if pos == 'GK':
                grupos['GK'].append(jogador)
            elif pos in ['CB', 'LCB', 'RCB']:
                grupos['CB'].append(jogador)
            elif pos in ['RB', 'RWB']:
                grupos['RB'].append(jogador)
            elif pos in ['LB', 'LWB']:
                grupos['LB'].append(jogador)
            elif pos in ['CM', 'CDM' ]:
                grupos['CM'].append(jogador)
            elif pos in ['CAM', 'RAM', 'LAM']:
                grupos['CAM'].append(jogador)
            elif pos in ['RM', 'RCM', 'RDM']:
                grupos['RM'].append(jogador)
            elif pos in ['LM', 'LCM', 'LDM']:
                grupos['LM'].append(jogador)
            elif pos in ['ST', 'CF']:
                grupos['ST'].append(jogador)
            elif pos in ['LW']:
                grupos['LW'].append(jogador)
            elif pos in ['RW']:
                grupos['RW'].append(jogador)
    return grupos

def gerar_individuo_formacao(posicoes, formacao):
    if formacao not in FORMACOES:
        return None
    config = FORMACOES[formacao]
    time = {}
    usado = set()
    # Goleiro
    if not posicoes.get('GK'):
        print("❌ Nenhum goleiro disponível.")
        return None
    gk = random.choice(posicoes['GK'])
    time['GK'] = gk
    usado.add(gk['Nome'])
    # Defensores
    defensores = []
    for p in ['CB', 'RB', 'LB']:
        if p in posicoes:
            defensores.extend([j for j in posicoes[p] if j['Nome'] not in usado])
    if len(defensores) < config['DEF']:
        print(f"❌ Precisa de {config['DEF']} defensores, mas só há {len(defensores)} disponíveis.")
        return None
    escolhidos = random.sample(defensores, config['DEF'])
    for i, j in enumerate(escolhidos):
        time[f'D{i+1}'] = j
        usado.add(j['Nome'])
    # Meias
    meias = []
    for p in ['CM', 'CAM', 'RM', 'LM']:
        if p in posicoes:
            meias.extend([j for j in posicoes[p] if j['Nome'] not in usado])
    if len(meias) < config['MEI']:
        print(f"❌ Precisa de {config['MEI']} meias, mas só há {len(meias)} disponíveis.")
        return None
    escolhidos = random.sample(meias, config['MEI'])
    for i, j in enumerate(escolhidos):
        time[f'M{i+1}'] = j
        usado.add(j['Nome'])
    # Atacantes
    atacantes = []
    for p in ['ST', 'LW', 'RW']:
        if p in posicoes:
            atacantes.extend([j for j in posicoes[p] if j['Nome'] not in usado])
    if len(atacantes) < config['ATA']:
        print(f"❌ Precisa de {config['ATA']} atacantes, mas só há {len(atacantes)} disponíveis.")
        return None
    escolhidos = random.sample(atacantes, config['ATA'])
    for i, j in enumerate(escolhidos):
        time[f'A{i+1}'] = j
    return time

def crossover(pai1, pai2):
    filho = {}
    for pos in pai1:
        if random.random() < 0.7: # Taxa de crossover pode ser um parâmetro
            filho[pos] = pai1[pos]
        else:
            filho[pos] = pai2[pos]
    return filho

def mutacao_formacao(individuo, posicoes, formacao, taxa=0.2):
    if random.random() < taxa:
        # Escolhe uma posição aleatória do time para mutar
        pos_alvo = random.choice(list(individuo.keys()))
        # Gera um novo indivíduo completo com a mesma formação
        novo = gerar_individuo_formacao(posicoes, formacao)
        # Se o novo indivíduo foi gerado com sucesso e tem a posição alvo,
        # substitui o jogador na posição alvo do indivíduo original
        if novo and pos_alvo in novo:
            individuo[pos_alvo] = novo[pos_alvo]
    return individuo