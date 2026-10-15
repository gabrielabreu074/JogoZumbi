import pygame

class Item:
    def __init__(self, tela, mapa, nome, x, y):
        self.nome = nome
        self.retangulo = pygame.Rect(x, y, 20, 20)
        self.tela = tela
        self.coletado = False

    def desenhar(self):
        pygame.draw.rect(self.tela, (139, 69, 19), self.retangulo)