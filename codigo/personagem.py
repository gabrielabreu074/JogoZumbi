
import os
import pygame
from codigo.inventario import Inventario


class Personagem:
    def __init__(self, tela, mapa):
        self.tela = tela
        self.mapa = mapa
        self.direcao = "direita"
        self.vivo = True
        self.area_ataque = None
        self.ultimo_ataque = 0
        self.atacando = False
        self.vida_maxima = 100
        self.vida = self.vida_maxima
        self.velocidade = 3
        self.inventario = Inventario()
        self.arma = None

        self.retangulo = pygame.Rect(45, 45, 38, 74)
        self.tamanho_imagem = (38, 74)
        self.esta_andando = False

        self.velocidade_animacao = 85
        self.indice_animacao = 0
        self.ultimo_frame = pygame.time.get_ticks()

        pasta_sprites = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "imagens", "personagem"
        )

        sprites_parado = {
            "baixo": "zoio parado puto-1.png",
            "esquerda": "zoio parado puto-2.png",
            "direita": "zoio parado puto-3.png",
            "cima": "zoio parado puto-4.png",
        }

        sprites_andando = {
            "baixo": "zoio andando puto-1.png",
            "cima": "zoio andando puto-2.png",
            "esquerda": "zoio andando puto-3.png",
            "direita": "zoio andando puto-4.png",
        }

        self.imagens_parado = {
            direcao: self.carregar_sprite(pasta_sprites, nome)
            for direcao, nome in sprites_parado.items()
        }

        self.imagens_andando = {
            direcao: self.carregar_sprite(pasta_sprites, nome)
            for direcao, nome in sprites_andando.items()
        }

        self.angulos_animacao = [0, 2, 3, 2, 0, -2, -3, -2]
        self.alturas_animacao = [0, 1, 2, 1, 0, 1, 2, 1]
        self.lados_animacao = [0, 1, 1, 0, 0, -1, -1, 0]

        self.frames_andando = {
            direcao: [
                pygame.transform.rotate(imagem, angulo)
                for angulo in self.angulos_animacao
            ]
            for direcao, imagem in self.imagens_andando.items()
        }

    def carregar_sprite(self, pasta, nome):
        imagem = pygame.image.load(
            os.path.join(pasta, nome)
        ).convert_alpha()

        return pygame.transform.scale(
            imagem, self.tamanho_imagem
        )

    def atualizar(self):
        teclas = pygame.key.get_pressed()
        movimento_x = 0
        movimento_y = 0

        if teclas[pygame.K_a]:
            movimento_x -= self.velocidade
        if teclas[pygame.K_d]:
            movimento_x += self.velocidade
        if teclas[pygame.K_w]:
            movimento_y -= self.velocidade
        if teclas[pygame.K_s]:
            movimento_y += self.velocidade

        if movimento_x < 0:
            self.direcao = "esquerda"
        elif movimento_x > 0:
            self.direcao = "direita"
        elif movimento_y < 0:
            self.direcao = "cima"
        elif movimento_y > 0:
            self.direcao = "baixo"

        if movimento_x != 0 and movimento_y != 0:
            fator = 1 / (2 ** 0.5)
            movimento_x *= fator
            movimento_y *= fator

        posicao_anterior = self.retangulo.topleft

        novo_retangulo = self.retangulo.copy()
        novo_retangulo.x += movimento_x

        if self.mapa.pode_andar(novo_retangulo):
            self.retangulo.x = novo_retangulo.x

        novo_retangulo = self.retangulo.copy()
        novo_retangulo.y += movimento_y

        if self.mapa.pode_andar(novo_retangulo):
            self.retangulo.y = novo_retangulo.y

        self.esta_andando = (
            self.retangulo.topleft != posicao_anterior
        )

        agora = pygame.time.get_ticks()

        if self.esta_andando:
            if agora - self.ultimo_frame >= self.velocidade_animacao:
                self.indice_animacao = (
                    self.indice_animacao + 1
                ) % len(self.angulos_animacao)

                self.ultimo_frame = agora
        else:
            self.indice_animacao = 0
            self.ultimo_frame = agora

        if not self.esta_andando:
            if pygame.mouse.get_pressed()[0]:
                self.atacando = True
                self.area_ataque = self.retangulo.inflate(40, 40)
            else:
                self.atacando = False
                self.area_ataque = None

    def desenhar(self):
        deslocamento_x = 0
        deslocamento_y = 0

        if self.esta_andando:
            imagem = self.frames_andando[
                self.direcao
            ][self.indice_animacao]

            deslocamento_x = self.lados_animacao[
                self.indice_animacao
            ]

            deslocamento_y = self.alturas_animacao[
                self.indice_animacao
            ]
        else:
            imagem = self.imagens_parado[self.direcao]

        posicao_x = (
            self.retangulo.centerx
            - imagem.get_width() // 2
            - self.mapa.camera.camera_x
            + deslocamento_x
        )

        posicao_y = (
            self.retangulo.bottom
            - imagem.get_height()
            - self.mapa.camera.camera_y
            - deslocamento_y
        )

        self.tela.blit(imagem, (posicao_x, posicao_y))

        retangulo_tela = self.retangulo.copy()
        retangulo_tela.x -= self.mapa.camera.camera_x
        retangulo_tela.y -= self.mapa.camera.camera_y

        pygame.draw.rect(
            self.tela,
            (255, 0, 0),
            retangulo_tela,
            2
        )
