import pygame
import random
from graphics import Superficie
from settings import *
from sys import exit
from player import Player
from level import Mapa
from enemy import Enemy
from debug import debug
from collectibles import *
from hud import HUD
from tela_morte import Tela_morte
from Botao import *

# Inicializando o PyGame
pygame.init()
# Definindo o titulo e o icon para a janela onde o jogo será executado
pygame.display.set_caption("Dungeon Sword")
icone = pygame.image.load("projeto\sprites_folder\sprite_06.png")
pygame.display.set_icon(icone)

#carregando imagens dos botoes
start_img = pygame.image.load('projeto/assets/start_btn.png').convert_alpha()
exit_img = pygame.image.load('projeto/assets/exit_btn.png').convert_alpha()
restart_img = pygame.image.load('projeto/assets/restart_btn.png').convert_alpha()
#instanciando os botoes, atribuindo a eles a classe Button de Botao
start_botao = Button((LARGURA_TELA/2 ) , 9* ALTURA_TELA /10 - (restart_img.get_height()/2), start_img, 0.75)#args: pos x, pos y , img, escala
exit_botao = Button((LARGURA_TELA/2 - exit_img.get_width()) , 9* ALTURA_TELA /10 - (restart_img.get_height()/2), exit_img, 0.75) 
restart_botao = Button(LARGURA_TELA/2,  9* ALTURA_TELA /10 - (restart_img.get_height()/2) ,restart_img, 0.3)

class Game:
    def __init__(self):
        # Criando um objeto de relógio que ajudara a controlar o tempo percorrido no jogo
        self.relogio = pygame.time.Clock()
    def running(self):
        jogo_pausado = True
        # Decidindo uma fonte para a UI, e criando a instancia de mapa, inimigo e jogador
        fonte = pygame.font.Font('projeto/assets/fonts\Pixeltype.ttf', 50)
        mapa = Mapa()
        mapa.proxima_fase()
        jogador = Player()
        porta = Portal()
        hud = HUD()
        # Rodando o loop do jogo
        while True: 
                # Isso vai 'limpar' a tela de fundo, para que as imagens que aparecem na tela não fiquem permanentemente nela 
                TELA.fill('Black')
                # Cria o mapa do jogo
                mapa.desenhar_mapa()
                # Vai checar quais eventos estão ocorrendo por dentro
                if jogo_pausado:
                    #ir para menu
                    TELA.blit(Superficie.im_jogo, (LARGURA_TELA/2 - Superficie.im_jogo.get_width()/2, ALTURA_TELA/2 - Superficie.im_jogo.get_height()/2))
                    if start_botao.draw(TELA):# se o botao foi pressionado executa ação
                        jogo_pausado = False
                    if exit_botao.draw(TELA):
                        break
                else: 
                    
                    # Isso vai atualizar o jogador e o inimigo, vendo se o jogador fez algum input, se o jogador ou o inimigo sofreu dano, e movimentando ambos, e após isso tudo, coloca suas superficies na tela
                    for inimigo in Enemy.lista_inimigos_presentes:
                        inimigo.atualizar(jogador, mapa)
                    if len(Enemy.lista_inimigos_presentes) == 0:
                        TELA.blit(porta.imagem, porta.hitbox)
                        if porta.hitbox.colliderect(jogador.hitbox):
                            mapa.proxima_fase()
                    jogador.atualizar(mapa)
                    #A hud no momento esta só como uma imagem para conter o contador de vida e de quantos abates foram feitos"
                    hud.exibir_hud(jogador, Enemy)
                    #Se o jogador morrer ele vai mostrar a tela de morte
                    if jogador.morreu:
                        Tela_morte().exibir_tela_morte(hud)
                        if restart_botao.draw(TELA):
                            jogador = mapa.reiniciar_jogo(jogador)
                        if exit_botao.draw(TELA):
                            break 
                    # Debug
                    # Atualizando o que aparece na tela a cada "Tick" (Tick é uma única atualização que ocorre na simulação do jogo)
                    # Limitando o número máximo de 'ticks'/'frames' por segundo a 60 para evitar que ocorra atualizações excessivas
                    self.relogio.tick(FPS)
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_m:
                            jogo_pausado = True
                            
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
                for coletavel in Coletaveis.lista_coletaveis:
                    TELA.blit(coletavel.imagem, coletavel.hitbox) #insere coletáveis
                    coletavel.coletar(jogador)

               
                pygame.display.update()
# Certificando que o jogo só será rodado nesse arquivo, e não caso ele seja importado ou algo do tipo
if __name__ == '__main__':    
    Game().running()