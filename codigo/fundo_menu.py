import math
import random
from pathlib import Path

import pygame


class FundoMenu:
    def __init__(self, largura, altura):
        self.largura = largura
        self.altura = altura
        self.tempo = 0

        caminho = (
                Path(__file__).resolve().parent.parent
                / "imagens"
                / "fundo"
                / "fundo_menu.png"
        )

        imagem = pygame.image.load(str(caminho)).convert()

        self.imagem = pygame.transform.smoothscale(
            imagem, (largura, altura)
        )

        self.camada_chuva = pygame.Surface(
            (largura, altura), pygame.SRCALPHA
        )

        self.gotas = []

        for _ in range(150):
            self.gotas.append({
                "x": random.uniform(0, largura),
                "y": random.uniform(0, altura),
                "velocidade": random.uniform(350, 650),
                "comprimento": random.randint(10, 23),
                "alpha": random.randint(35, 90)
            })

        self.nevoa = self.criar_nevoa()

        self.nuvens = [
            {
                "x": -largura * 0.3,
                "y": altura * 0.48,
                "velocidade": 12,
                "fase": 0
            },
            {
                "x": largura * 0.2,
                "y": altura * 0.60,
                "velocidade": 8,
                "fase": 2
            },
            {
                "x": largura * 0.7,
                "y": altura * 0.51,
                "velocidade": 15,
                "fase": 4
            }
        ]

        self.luz = self.criar_luz()

        self.posicao_luz = (
            round(largura * 0.831),
            round(altura * 0.365)
        )

    def criar_nevoa(self):
        superficie = pygame.Surface(
            (200, 60), pygame.SRCALPHA
        )

        for y in range(60):
            for x in range(200):
                distancia = (
                    ((x - 100) / 100) ** 2
                    + ((y - 30) / 30) ** 2
                )

                if distancia < 1:
                    alpha = int(
                        23 * (1 - distancia) ** 2
                    )

                    superficie.set_at(
                        (x, y),
                        (150, 170, 185, alpha)
                    )

        return pygame.transform.smoothscale(
            superficie,
            (
                int(self.largura * 0.8),
                int(self.altura * 0.23)
            )
        )

    def criar_luz(self):
        superficie = pygame.Surface(
            (100, 100), pygame.SRCALPHA
        )

        for y in range(100):
            for x in range(100):
                distancia = math.hypot(
                    x - 50, y - 50
                ) / 50

                if distancia < 1:
                    alpha = int(
                        60 * (1 - distancia) ** 2
                    )

                    superficie.set_at(
                        (x, y),
                        (255, 185, 90, alpha)
                    )

        tamanho = max(
            40, round(self.largura * 0.12)
        )

        return pygame.transform.smoothscale(
            superficie, (tamanho, tamanho)
        )

    def atualizar(self, dt):
        dt = min(dt, 0.05)
        self.tempo += dt

        for gota in self.gotas:
            gota["x"] -= gota["velocidade"] * 0.28 * dt
            gota["y"] += gota["velocidade"] * dt

            if (
                gota["y"] > self.altura + 30
                or gota["x"] < -30
            ):
                gota["x"] = random.uniform(
                    0, self.largura + self.altura * 0.28
                )
                gota["y"] = random.uniform(-100, -25)

        for nuvem in self.nuvens:
            nuvem["x"] += nuvem["velocidade"] * dt

            if nuvem["x"] > self.largura:
                nuvem["x"] = -self.nevoa.get_width()

    def desenhar(self, tela):
        tela.blit(self.imagem, (0, 0))

        intensidade = (
            175
            + 35 * math.sin(self.tempo * 2.1)
            + 15 * math.sin(self.tempo * 5.3)
        )

        self.luz.set_alpha(int(intensidade))

        tela.blit(
            self.luz,
            self.luz.get_rect(center=self.posicao_luz)
        )

        for nuvem in self.nuvens:
            deslocamento_y = math.sin(
                self.tempo * 0.4 + nuvem["fase"]
            ) * 9

            tela.blit(
                self.nevoa,
                (
                    round(nuvem["x"]),
                    round(nuvem["y"] + deslocamento_y)
                )
            )

        self.camada_chuva.fill((0, 0, 0, 0))

        for gota in self.gotas:
            x = round(gota["x"])
            y = round(gota["y"])
            comprimento = gota["comprimento"]

            pygame.draw.line(
                self.camada_chuva,
                (175, 195, 215, gota["alpha"]),
                (x, y),
                (
                    x - round(comprimento * 0.28),
                    y + comprimento
                ),
                1
            )

        tela.blit(self.camada_chuva, (0, 0))