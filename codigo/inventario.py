import pygame


class Inventario:
    def __init__(self):
        self.itens = []

    def adicionar(self, item):
        self.itens.append(item)

    def remover(self, item):
        if item in self.itens:
            self.itens.remove(item)

    def desenhar(self, tela):
        fonte = pygame.font.Font(None, 35)

        pygame.draw.rect(tela, "gray", (200, 100, 880, 520))
        pygame.draw.rect(tela, "black", (220, 120, 840, 480))

        titulo = fonte.render("INVENTARIO", True, "White")
        tela.blit(titulo, (240, 140))

        for i, item in enumerate(self.itens):
            texto = fonte.render(
                f"{i + 1} - {item}", True, "White")

            tela.blit(texto, (250, 190 + i * 40))


