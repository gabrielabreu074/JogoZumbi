import pygame

class Projetil:
    def __init__(self, tela, x, y, width, height, velocidade, dirx, diry):
        self.tela = tela
        self.retangulo = pygame.Rect(x, y, width, height)
        self.velocidade = velocidade
        self.dirx = dirx
        self.diry = diry
        self.x = x
        self.y = y

    def atualizar(self):
        dirx = self.velocidade * self.dirx
        diry = self.velocidade * self.diry
        self.x += dirx
        self.y += diry
        self.retangulo.x = self.x
        self.retangulo.y = self.y
    def desenhar(self, camera):
        posicao_x = self.retangulo.x - camera.camera_x
        posicao_y = self.retangulo.y - camera.camera_y
        retangulo_tela = pygame.Rect(posicao_x, posicao_y, self.retangulo.width, self.retangulo.height)
        pygame.draw.rect(self.tela, (255,255,0), retangulo_tela )