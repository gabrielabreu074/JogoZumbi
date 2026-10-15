
import pygame


class HUD:

    def __init__(self, largura, altura):
        self.largura = largura
        self.altura = altura

        self.total_slots = 9
        self.tamanho_slot = 52
        self.espaco_slot = 5
        self.slot_selecionado = 0

        self.largura_hud = (
            self.total_slots * self.tamanho_slot
            + (self.total_slots - 1) * self.espaco_slot
        )

        self.x_hud = (largura - self.largura_hud) // 2
        self.y_hud = altura - 75

        self.fonte = pygame.font.SysFont("comicsans", 20)
        self.fonte_vida = pygame.font.SysFont("comicsans", 20)

    def atualizar(self, eventos):
        for evento in eventos:
            if evento.type == pygame.KEYDOWN:
                if pygame.K_1 <= evento.key <= pygame.K_9:
                    self.slot_selecionado = evento.key - pygame.K_1

    def desenhar(self, tela, vida, vida_maxima):

        for i in range(self.total_slots):
            x = self.x_hud + i * (
                self.tamanho_slot + self.espaco_slot
            )

            slot = pygame.Rect(
                x,
                self.y_hud,
                self.tamanho_slot,
                self.tamanho_slot
            )

            pygame.draw.rect(
                tela,
                (25, 25, 25),
                slot,
                border_radius=5
            )

            if i == self.slot_selecionado:
                cor = (255, 220, 80)
                espessura = 4
            else:
                cor = (130, 130, 130)
                espessura = 2

            pygame.draw.rect(
                tela,
                cor,
                slot,
                espessura,
                border_radius=5
            )

            numero = self.fonte.render(
                str(i + 1),
                True,
                (220, 220, 220)
            )

            tela.blit(numero, (x + 4, self.y_hud + 2))

        x_vida = self.x_hud
        y_vida = self.y_hud - 28

        texto_vida = self.fonte_vida.render(
            "VIDA",
            True,
            (255, 255, 255)
        )

        tela.blit(texto_vida, (x_vida, y_vida))

        if vida_maxima > 0:
            proporcao = max(0, min(vida / vida_maxima, 1))
        else:
            proporcao = 0

        largura_barra = 180
        altura_barra = 16

        barra_fundo = pygame.Rect(
            x_vida + 75,
            y_vida + 5,
            largura_barra,
            altura_barra
        )

        pygame.draw.rect(
            tela,
            (70, 30, 30),
            barra_fundo,
            border_radius=4
        )

        largura_preenchida = int(largura_barra * proporcao)

        if largura_preenchida > 0:
            barra_vida = pygame.Rect(
                barra_fundo.x,
                barra_fundo.y,
                largura_preenchida,
                altura_barra
            )

            pygame.draw.rect(
                tela,
                (220, 35, 35),
                barra_vida,
                border_radius=4
            )

        texto_valor = self.fonte_vida.render(
            f"{max(0, vida)}/{vida_maxima}",
            True,
            (255, 255, 255)
        )

        tela.blit(
            texto_valor,
            (barra_fundo.right + 10, y_vida)
        )