import pygame
import random
from graphics import Superficie
from graphics import fonte_hud
from settings import *
from sys import exit
from player import Player
from level import Mapa
from enemy import Enemy
from debug import debug
from collectibles import Coletaveis
from hud import HUD
from tela_morte import Tela_morte
# Inicializando o PyGame
pygame.init()
# Definindo o titulo e o icon para a janela onde o jogo será executado
pygame.display.set_caption("Jogo maneirasso")
icone = pygame.image.load("projeto/assets\icone-placeholder.png")
pygame.display.set_icon(icone)


class Game:
    def __init__(self):
        # Criando um objeto de relógio que ajudara a controlar o tempo percorrido no jogo
        self.relogio = pygame.time.Clock()
    def running(self):
        # Decidindo uma fonte para a UI, e criando a instancia de mapa, inimigo e jogador
        fonte = pygame.font.Font('projeto/assets/fonts\Pixeltype.ttf', 50)
        mapa = Mapa()
        numero_inimigos = random.randint(3, 7)
        for _ in range(numero_inimigos):
            inimigo = Enemy(mapa)
            Enemy.lista_inimigos_presentes.append(inimigo)
        jogador = Player()
        # Rodando o loop do jogo
        while True: 
                # Isso vai 'limpar' a tela de fundo, para que as imagens que aparecem na tela não fiquem permanentemente nela 
                TELA.fill('Black')
                # Cria o mapa do jogo
                mapa.desenhar_mapa()
                # Vai checar quais eventos estão ocorrendo por dentro
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    # Ver função ataque do Player
                    elif event.type == EVENTO_INTERVALO_ATAQUE:
                        jogador.pode_atacar = True
                        pygame.time.set_timer(EVENTO_INTERVALO_ATAQUE, 0)
                    # Ver função causou_dano do Enemy
                    elif event.type == EVENTO_INTERVALO_DANO:
                        jogador.sofreu_dano = False
                        pygame.time.set_timer(EVENTO_INTERVALO_DANO, 0)
                # Inserindo uma superficie em cima do display. A os valores representam as cordenadas da superficie sobre o display. O ponto de origem é sempre no canto superior esquerdo
                TELA.blit(Coletaveis.sword, (900,100)) #insere coletável da espada
                TELA.blit(Coletaveis.shield,(200,500)) #insere coletável do escudo
                # Isso vai atualizar o jogador e o inimigo, vendo se o jogador fez algum input, se o jogador ou o inimigo sofreu dano, e movimentando ambos, e após isso tudo, coloca suas superficies na tela
                for inimigo in Enemy.lista_inimigos_presentes:
                    inimigo.atualizar(jogador, mapa)
                jogador.atualizar(mapa)
                if len(Enemy.lista_inimigos_presentes) == 0:
                    numero_inimigos = random.randint(3, 7)
                    for _ in range(numero_inimigos):
                        inimigo = Enemy(mapa)
                        Enemy.lista_inimigos_presentes.append(inimigo)
                #A hud no momento esta só como uma imagem para conter o contador de vida e de quantos abates foram feitos"
                sup_vida= fonte_hud.render(f'{jogador.vida}', False, "Yellow")
                sup_pontuacao = fonte.render(f'{jogador.pontuacao}', False, 'White')
                TELA.blit(sup_pontuacao, (205,100))
                TELA.blit(HUD.hud, (2,2))
                TELA.blit(sup_vida, (225,43))

                #Se o jogador morrer ele vai mostrar a tela de morte
                if jogador.vida == 0:
                    TELA.blit(Tela_morte.tela_morte, (1,1))
                    TELA.blit(sup_pontuacao, (600,400))
            
                # Debug
                #debug(jogador.olhando_direcao, 'Direção:')         
                debug((inimigo.sofreu_dano), 'Pode sofrer dano:')
                #debug((jogador.vida), 'Vida jogador:', 60)
                # Atualizando o que aparece na tela a cada "Tick" (Tick é uma única atualização que ocorre na simulação do jogo)
                pygame.display.update()
                # Limitando o número máximo de 'ticks'/'frames' por segundo a 60 para evitar que ocorra atualizações excessivas
                self.relogio.tick(FPS)
# Certificando que o jogo só será rodado nesse arquivo, e não caso ele seja importado ou algo do tipo
if __name__ == '__main__':    
    Game().running()