import pygame


class Arma:
    def __init__(self, nome, caminho_imagem, x, y, capacidade=12, municao=6, reserva=36):
        self.nome = nome
        self.capacidade = capacidade
        self.municao = min(municao, capacidade)
        self.reserva = reserva

        imagem = pygame.image.load(caminho_imagem).convert_alpha()
        self.imagem_chao = pygame.transform.smoothscale(imagem, (46, 32))
        self.icone = pygame.transform.smoothscale(imagem, (36, 25))
        self.retangulo = self.imagem_chao.get_rect(center=(x, y))

    def esta_perto(self, personagem):
        posicao_arma = pygame.Vector2(self.retangulo.center)
        posicao_personagem = pygame.Vector2(personagem.retangulo.center)
        return posicao_arma.distance_to(posicao_personagem) <= 75

    def desenhar_chao(self, tela, camera):
        x = self.retangulo.x - camera.camera_x
        y = self.retangulo.y - camera.camera_y
        tela.blit(self.imagem_chao, (x, y))

    def recarregar(self):
        faltando = self.capacidade - self.municao
        quantidade = min(faltando, self.reserva)

        if quantidade <= 0:
            return False

        self.municao += quantidade
        self.reserva -= quantidade
        return True
