# Importando a bib pygame
import pygame as pg

# Importando randrange da bib random
from random import randrange

# Define tamanhado da janela que vai rodar o jogo
JANELA = 700

# Inicialização da janela com a função set_mode, passando JANELA
tela = pg.display.set_mode([JANELA] * 2)

# Instância da classe clock. "Seta" o frame rate
relogio = pg.time.Clock()

# *************************************************************************
# O jogo será baseado em mosaico, portanto, as 3 variáveis abaixo configuram esse aspceto:

# 1º Define o tamanho de cada mosaico
TAMANHO_MOSAICO = 50

# 2º Tupla que define o alcance das coordenadas aleatórias referente a cada mosaico dentro da tela
ALCANCE = (TAMANHO_MOSAICO // 2, JANELA - TAMANHO_MOSAICO // 2, TAMANHO_MOSAICO)

# 3º Usando a tupla criada acima, pega as posiçãoes aletórias criadas - Função
pega_posicao_aleatoria = (lambda alcance: lambda: [randrange(*alcance), randrange(*alcance)])(ALCANCE)

# *************************************************************************
# Parâmetros da cobrinha

# Cabeça = Instânica da classe Rect (Objeto que armazena coordenadas para um retângulo/quadrado
cobrinha = pg.rect.Rect([0, 0, TAMANHO_MOSAICO - 2, TAMANHO_MOSAICO - 2])

# Define a posição da cobrinha aleatóriamente na tela
cobrinha.center = pega_posicao_aleatoria()

# Define o comprimento de cada segmento da cobrinha
comprimento = 1

# Armazena os segmentos da cobrinha. Cópias iguais
segmentos = [cobrinha.copy()]

# Direção da cobrinha
cobrinha_direcao = (0, 0)

# Controla a velocidade dos passos da cobrinha. tempo_passo é o delay, em milisegundos, entre cada passo
tempo, tempo_passo = 0, 110

# Dicionário que será usado para proibir que a cobrinha ande para trás e se mate
dirs = {pg.K_w: 1, pg.K_s: 1, pg.K_a: 1, pg.K_d: 1}
# *************************************************************************
# Parâmetros da comida da cobrinha

# A comida será uma cópia da cabeça da cobrinha
comida = cobrinha.copy()

# Seta a posição da comida aleatóriamente
comida.center = pega_posicao_aleatoria()

# Principal laço de repetição da aplicação
while True:
    # Para cada iteração...
    for event in pg.event.get():
        # Verifica se o usuário fechou a aplicação
        if event.type == pg.QUIT:
            # Fecha a aplicação se for true
            exit()
        # Realiza as verificações se as teclas para movimentar a cobrinha estção sendo pressionadas - Checagem de evento
        if event.type == pg.KEYDOWN:
            # Para cada movimento, foi dada o tamanho que o movimento pode dar, no caso igual o tamanho da cobrinha (Cabeça)
            if event.key == pg.K_w and dirs[pg.K_w]:
                cobrinha_direcao = (0, -TAMANHO_MOSAICO)
                dirs = {pg.K_w: 1, pg.K_s: 0, pg.K_a: 1, pg.K_d: 1}
            if event.key == pg.K_s and dirs[pg.K_s]:
                cobrinha_direcao = (0, TAMANHO_MOSAICO)
                dirs = {pg.K_w: 0, pg.K_s: 1, pg.K_a: 1, pg.K_d: 1}
            if event.key == pg.K_a and dirs[pg.K_a]:
                cobrinha_direcao = (-TAMANHO_MOSAICO, 0)
                dirs = {pg.K_w: 1, pg.K_s: 1, pg.K_a: 1, pg.K_d: 0}
            if event.key == pg.K_d and dirs[pg.K_d]:
                cobrinha_direcao = (TAMANHO_MOSAICO, 0)
                dirs = {pg.K_w: 1, pg.K_s: 1, pg.K_a: 0, pg.K_d: 1}
        # Inicializa a tela da aplicação se for falso

        # Primeiro inicializa uma tela preta
        tela.fill('black')

        # Desenha a cobrinha - Compreensão de lista
        [pg.draw.rect(tela, 'green', segmento) for segmento in segmentos]

        # Desenha a comida da cobrinha
        pg.draw.rect(tela, 'red', comida)

        # Checa as bordas da tela e se a cminha se comeu. Coordenadas da cabeça da cobrinha com as das bordas da janela
        suicidio = pg.Rect.collidelist(cobrinha, segmentos[:-1]) != -1
        if cobrinha.left < 0 or cobrinha.right > JANELA or cobrinha.top < 0 or cobrinha.bottom > JANELA or suicidio:
            cobrinha.center, comida.center = pega_posicao_aleatoria(), pega_posicao_aleatoria()
            comprimento, cobrinha_direcao = 1, (0, 0)
            segmentos = [cobrinha.copy()]

        # Checa as posições da cobrinha e da comida. Se forem as mesmas...
        if cobrinha.center == comida.center:
            # Mostra a comida em uma nova posição
            comida.center = pega_posicao_aleatoria()
            # Adicona mais um segmento a cobrinha
            comprimento += 1

        # Armazena o valor do intervalo, de todas as direções, entre cada passo dado na casa dos milisegundos
        tempo_agora = pg.time.get_ticks()
        # Assim que o valor do intervalo for maior que o valor do tempo_passo...
        if tempo_agora - tempo > tempo_passo:
            # A cobrinha vai dar o próximo passow
            tempo = tempo_agora
            # Movimenta a cobrinha
            cobrinha.move_ip(cobrinha_direcao)
            # Adiciona uma nova cabeça para cada passo dado a lista
            segmentos.append(cobrinha.copy())
            # Remove o passo dado da lista para poder dar mais um novo passo...
            segmentos = segmentos[-comprimento:]

        # Atualiza a tela inicializada
        pg.display.flip()
        # Seta a atualização de quadros para 60
        relogio.tick(60)
