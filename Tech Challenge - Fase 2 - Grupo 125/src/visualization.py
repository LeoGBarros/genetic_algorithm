import pygame

def inicializar_fonte():
    global FONTE
    FONTE = pygame.font.SysFont('Arial', 24)

def desenhar_campo(screen):
    screen.fill((0, 100, 0))
    pygame.draw.rect(screen, (255, 255, 255), (50, 100, 700, 400), 3)
    pygame.draw.line(screen, (255, 255, 255), (400, 100), (400, 500), 3)
    pygame.draw.circle(screen, (255, 255, 255), (400, 300), 80, 3)

    # Área esquerda
    pygame.draw.rect(screen, (255, 255, 255), (50, 200, 120, 200), 3)
    pygame.draw.rect(screen, (255, 255, 255), (50, 250, 50, 100), 3)
    pygame.draw.circle(screen, (255, 255, 255), (120, 300), 10)

    # Área direita
    pygame.draw.rect(screen, (255, 255, 255), (630, 200, 120, 200), 3)
    pygame.draw.rect(screen, (255, 255, 255), (700, 250, 50, 100), 3)
    pygame.draw.circle(screen, (255, 255, 255), (730, 300), 10)

def desenhar_jogadores(screen, time, formacao):
    posicoes_map = {
        "4-4-2": {
            'GK': (100, 300),
            'D1': (200, 150), 'D2': (200, 250), 'D3': (200, 350), 'D4': (200, 450),
            'M1': (350, 150), 'M2': (350, 250), 'M3': (350, 350), 'M4': (350, 450),
            'A1': (550, 250), 'A2': (550, 350)
        },
        "4-3-3": {
            'GK': (100, 300),
            'D1': (200, 150), 'D2': (200, 250), 'D3': (200, 350), 'D4': (200, 450),
            'M1': (300, 200), 'M2': (300, 300), 'M3': (300, 400),
            'A1': (500, 180), 'A2': (500, 300), 'A3': (500, 420)
        },
        "3-5-2": {
            'GK': (100, 300),
            'D1': (200, 200), 'D2': (200, 300), 'D3': (200, 400),
            'M1': (300, 150), 'M2': (300, 230), 'M3': (300, 310), 'M4': (300, 390), 'M5': (300, 470),
            'A1': (500, 250), 'A2': (500, 350)
        },
        "5-3-2": {
            'GK': (100, 300),
            'D1': (200, 150), 'D2': (200, 230), 'D3': (200, 300), 'D4': (200, 370), 'D5': (200, 450),
            'M1': (350, 200), 'M2': (350, 300), 'M3': (350, 400),
            'A1': (550, 250), 'A2': (550, 350)
        }
    }

    pos_tela = posicoes_map.get(formacao, posicoes_map["4-4-2"])

    font_nome = pygame.font.SysFont('Arial', 18, bold=True)
    font_rating = pygame.font.SysFont('Arial', 24, bold=True)

    for pos, jogador in time.items():
        if pos in pos_tela:
            x, y = pos_tela[pos]
            rating = jogador['Rating']
            cor = (0, 255, 0) if rating > 75 else (255, 255, 0) if rating > 70 else (255, 0, 0)
            pygame.draw.circle(screen, cor, (x, y), 28)
            pygame.draw.circle(screen, (255, 255, 255), (x, y), 28, 2)

            nome = jogador['Nome'].split()[0][:8]
            texto_nome = font_nome.render(nome, True, (0, 0, 0))
            screen.blit(texto_nome, (x - 35, y - 50))

            texto_rating = font_rating.render(str(int(rating)), True, (0, 0, 100))
            screen.blit(texto_rating, (x - 12, y - 12))

def desenhar_botoes(screen, botoes):
    mouse_pos = pygame.mouse.get_pos()
    for botao in botoes:
        cor = (100, 149, 237) if botao['rect'].collidepoint(mouse_pos) else (70, 130, 180)
        pygame.draw.rect(screen, cor, botao['rect'], border_radius=8)
        texto_surf = FONTE.render(botao['texto'], True, (255, 255, 255))
        screen.blit(texto_surf, (botao['rect'].x + 15, botao['rect'].y + 10))

def criar_botoes():
    return [
        {'texto': '4-4-2', 'rect': pygame.Rect(50, 20, 100, 40), 'valor': '4-4-2'},
        {'texto': '4-3-3', 'rect': pygame.Rect(160, 20, 100, 40), 'valor': '4-3-3'},
        {'texto': '3-5-2', 'rect': pygame.Rect(270, 20, 100, 40), 'valor': '3-5-2'},
        {'texto': '5-3-2', 'rect': pygame.Rect(380, 20, 100, 40), 'valor': '5-3-2'},
        {'texto': 'GERAR TIME', 'rect': pygame.Rect(600, 20, 140, 40), 'valor': 'gerar'}
    ]