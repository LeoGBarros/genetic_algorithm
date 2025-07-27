import pygame
import random
# Importações atualizadas - removemos 'executar_algoritmo_genetico' daqui
# pois vamos definir localmente com a modificação do callback
from src.data_loader import carregar_dados
from src.genetic_algorithm import agrupar_por_posicao, gerar_individuo_formacao, crossover, mutacao_formacao, FORMACOES # Adicionado FORMACOES
from src.team_builder import calcular_fitness
from src.visualization import inicializar_fonte, desenhar_campo, desenhar_jogadores, criar_botoes, desenhar_botoes

def executar_algoritmo_genetico(posicoes, formacao, jogadores, geracoes=50, tamanho_pop=30, callback=None):
    """
    Executa o algoritmo genético.
    Agora aceita um callback para atualizar a visualização em tempo real.
    O callback recebe (melhor_individuo_da_geracao, numero_da_geracao, fitness_do_melhor).
    """
    populacao = [gerar_individuo_formacao(posicoes, formacao) for _ in range(tamanho_pop)]
    populacao = [ind for ind in populacao if ind]

    if not populacao:
        print("❌ Nenhum time válido gerado.")
        if callback:
            callback(None, 0, 0) # Notificar falha
        return None

    melhor = max(populacao, key=calcular_fitness)
    melhor_fitness = calcular_fitness(melhor)
    geracao_atual = 0

    # Chama o callback com o primeiro melhor time encontrado
    if callback:
        callback(melhor, geracao_atual, melhor_fitness)

    for geracao in range(geracoes):
        populacao = sorted(populacao, key=calcular_fitness, reverse=True)
        nova_pop = [populacao[0]] # Elitismo

        while len(nova_pop) < tamanho_pop:
            pai1 = random.choice(populacao[:10]) # Seleção por torneio simplificada
            pai2 = random.choice(populacao[:10])
            filho = crossover(pai1, pai2)
            filho = mutacao_formacao(filho, posicoes, formacao, taxa=0.2)
            if filho:
                nova_pop.append(filho)

        populacao = nova_pop
        melhor_atual = populacao[0]
        melhor_atual_fitness = calcular_fitness(melhor_atual)

        # Verifica se encontrou um novo melhor
        if melhor_atual_fitness > melhor_fitness:
            melhor = {k: v for k, v in melhor_atual.items()} # Cópia profunda
            melhor_fitness = melhor_atual_fitness
            # Chama o callback com o novo melhor
            if callback:
                callback(melhor, geracao + 1, melhor_fitness)
        else:
            # Mesmo que não melhore, atualiza a visualização a cada 5 gerações para mostrar progresso
            # Isso evita travar a tela por muito tempo
            if (geracao + 1) % 5 == 0 and callback:
                 callback(melhor, geracao + 1, melhor_fitness)

        # Atualiza sempre o número da geração para o callback final
        geracao_atual = geracao + 1

    # Garante que o estado final seja enviado ao callback
    if callback:
        callback(melhor, geracao_atual, melhor_fitness)

    return melhor

def main():
    # Carregar dados
    try:
        jogadores = carregar_dados("data/FullData.csv")
        if not jogadores:
            print("❌ Nenhum jogador carregado.")
            return
        print(f"✅ {len(jogadores)} jogadores carregados.")
    except Exception as e:
        print(f"❌ Erro ao carregar dados: {e}")
        return

    # Agrupar por posição
    posicoes = agrupar_por_posicao(jogadores)

    # Depuração: Mostrar jogadores por posição
    print("\n🔍 Jogadores por posição:")
    for pos, lista in posicoes.items():
        print(f"  {pos}: {len(lista)} jogadores")

    # Teste de geração (opcional, pode ser removido)
    teste = gerar_individuo_formacao(posicoes, "4-4-2")
    if teste:
        print(f"✅ Teste: Time gerado! Goleiro: {teste['GK']['Nome']}")
    else:
        print("❌ Teste: Falha ao gerar time. Verifique os dados.")
        # Não retorna mais aqui, o teste é apenas informativo

    # Configurações
    formacao_selecionada = "4-4-2"
    time_gerado = None
    geracao_atual = 0
    fitness_gerado = 0.0
    total_geracoes = 50 # Padrão
    esta_executando = False # Flag para controlar o estado da execução

    # Pygame
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Time Ideal - Algoritmo Genético")
    clock = pygame.time.Clock()
    inicializar_fonte()
    botoes = criar_botoes()

    # Fonte para informações
    fonte_info = pygame.font.SysFont(None, 28)

    rodando = True
    while rodando:
        # --- Tratamento de Eventos ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando = False

            if event.type == pygame.MOUSEBUTTONDOWN and not esta_executando:
                for botao in botoes:
                    if botao['rect'].collidepoint(event.pos):
                        if botao['valor'] == 'gerar':
                            print(f"🔄 Iniciando geração do time na formação {formacao_selecionada}...")
                            esta_executando = True
                            geracao_atual = 0
                            time_gerado = None # Reseta para mostrar início
                            fitness_gerado = 0.0

                            # --- Função Callback ---
                            def callback(melhor_time, gen, fit):
                                nonlocal time_gerado, geracao_atual, fitness_gerado
                                time_gerado = melhor_time
                                geracao_atual = gen
                                fitness_gerado = fit
                                # Redesenha a tela com o novo time
                                screen.fill((0, 0, 0))
                                desenhar_campo(screen)
                                desenhar_botoes(screen, botoes)
                                if time_gerado:
                                    desenhar_jogadores(screen, time_gerado, formacao_selecionada)
                                # Exibir informações de progresso
                                texto_formacao = fonte_info.render(f"Formação: {formacao_selecionada}", True, (255, 255, 255))
                                screen.blit(texto_formacao, (20, 520))
                                texto_geracao = fonte_info.render(f"Geração: {geracao_atual}/{total_geracoes}", True, (255, 255, 255))
                                screen.blit(texto_geracao, (20, 550))
                                texto_fitness = fonte_info.render(f"Fitness: {fitness_gerado:.1f}", True, (255, 255, 255))
                                screen.blit(texto_fitness, (20, 580))
                                texto_status = fonte_info.render("Executando...", True, (255, 215, 0)) # Amarelo
                                screen.blit(texto_status, (650, 580))
                                pygame.display.flip()
                                # Pequeno atraso para permitir a visualização (opcional)
                                # pygame.time.delay(50) # Pode deixar a execução mais lenta

                            # --- Chama o Algoritmo ---
                            # O algoritmo será executado, mas o callback atualizará a tela
                            # durante o processo. O `main` loop do pygame continua rodando.
                            def executar_e_finalizar():
                                nonlocal esta_executando
                                # Chama o algoritmo genético com o callback
                                resultado = executar_algoritmo_genetico(
                                    posicoes, formacao_selecionada, jogadores,
                                    geracoes=total_geracoes, tamanho_pop=30,
                                    callback=callback
                                )
                                # Após terminar, atualiza o estado final
                                if resultado:
                                    print(f"✅ Algoritmo concluído! Melhor Fitness: {calcular_fitness(resultado):.1f}")
                                else:
                                    print("❌ Algoritmo não encontrou um time válido.")
                                esta_executando = False # Libera os botões

                            # Chama a função que executa o algoritmo e depois finaliza
                            executar_e_finalizar()


                        else: # Seleção de formação
                            # Só permite mudar formação se não estiver executando
                            if not esta_executando:
                                formacao_selecionada = botao['valor']
                                print(f"✅ Formação selecionada: {formacao_selecionada}")
                                # Se a formação mudar, o time atual pode não ser válido
                                # Você pode optar por limpar `time_gerado` aqui também
                                # time_gerado = None


        # --- Desenho na Tela (se não estiver no meio de uma execução via callback) ---
        # O callback já redesenha a tela, então este bloco só é relevante
        # para estados estáticos (idle, após conclusão)
        if not esta_executando:
            screen.fill((0, 0, 0))
            desenhar_campo(screen)
            desenhar_botoes(screen, botoes)

            if time_gerado:
                desenhar_jogadores(screen, time_gerado, formacao_selecionada)

            # Exibir informações finais
            texto_formacao = fonte_info.render(f"Formação: {formacao_selecionada}", True, (255, 255, 255))
            screen.blit(texto_formacao, (20, 520))
            texto_geracao = fonte_info.render(f"Geração: {geracao_atual}/{total_geracoes}", True, (255, 255, 255))
            screen.blit(texto_geracao, (20, 550))
            texto_fitness = fonte_info.render(f"Fitness: {fitness_gerado:.1f}", True, (255, 255, 255))
            screen.blit(texto_fitness, (20, 580))

            # Status
            status_texto = "Pronto" if not esta_executando else "Executando..."
            cor_status = (0, 255, 0) if not esta_executando else (255, 215, 0) # Verde ou Amarelo
            texto_status = fonte_info.render(status_texto, True, cor_status)
            screen.blit(texto_status, (650, 580))

            pygame.display.flip()

        # Limita a taxa de quadros
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()