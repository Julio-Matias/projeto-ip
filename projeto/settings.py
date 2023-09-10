import pygame
pygame.init()
# Dimensões do jogador
LARGURA_JOGADOR, ALTURA_JOGADOR = 100, 100
# Caracteristicas da tela
# O display (tela do jogo) é uma superficie onde tudo que está sendo mostrado ao jogador ficará
LARGURA_TELA, ALTURA_TELA = 1200, 700
TELA = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA)) 
FPS = 60
# Mapa do jogo
TAMANHO_TILE = 50
mapa = [
    "PPPPPPPPPPPPPPPPPPPPPPPP",
    "P000000000P000000000000P",
    "P000000000P000000000000P",
    "P0000000000000000000000P",
    "P0000000000000000000000P",
    "P0000000000000000000000P",
    "P0000000000000000000000P",
    "P0000000000000000000000P",
    "P0000000000000000000000P",
    "P0000000000000000000000P",
    "P0000000000000000000000P",
    "P0000000000000000000000P",
    "P000000000P000000000000P",
    "PPPPPPPPPPPPPPPPPPPPPPPP"
]
# Cores
class Cor:
    PRETO = (0, 0, 0)
    BRANCO = (255, 255, 255)
    VERMELHO = (255, 0, 0)
    def __init__(self) -> None:
        pass
    