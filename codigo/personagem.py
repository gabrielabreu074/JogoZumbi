import pygame
from codigo.inventario import Inventario
import os


class Personagem:

    def __init__(self, tela, mapa):
        self.tela = tela
        self.mapa = mapa
        self.direcao = "direita"
        self.vivo = True
        self.item_equipado = None
        self.area_ataque = None
        self.ultimo_ataque = 0
        self.atacando = False
        self.vida_maxima = 100
        self.vida = self.vida_maxima
        self.velocidade = 3
        self.inventario = Inventario()
        self.arma = None
        self.tamanho_imagem = (38, 74)
        self.spritesheet_pistola = pygame.image.load('imagens/personagem/zoio arma1.png').convert_alpha()

        self.pistola_parado_baixo = self.spritesheet_pistola.subsurface((350, 10, 200, 355))
        self.pistola_parado_direita = self.spritesheet_pistola.subsurface((760,10,200,355))
        self.pistola_parado_esquerda = self.spritesheet_pistola.subsurface((970,10,200,355))
        self.pistola_parado_cima = self.spritesheet_pistola.subsurface((570,10,200,355))

        self.pistola_andando_direita_1 = self.spritesheet_pistola.subsurface((730, 370, 195, 270))
        self.pistola_andando_direita_2 = self.spritesheet_pistola.subsurface((1090, 370, 167, 270))

        self.pistola_andando_esquerda_1 = pygame.image.load('imagens/personagem/pistola_andando_esquerda_1_38x74.png').convert_alpha()
        self.pistola_andando_esquerda_2 = pygame.image.load('imagens/personagem/pistola_andando_esquerda_2_38x74.png').convert_alpha()

        self.pistola_andando_cima_1 = pygame.image.load('imagens/personagem/pistola_andando_cima_1_38x74_ajustada.png').convert_alpha()
        self.pistola_andando_cima_2 = pygame.image.load('imagens/personagem/pistola_andando_cima_2_38x74_ajustada.png').convert_alpha()

        self.pistola_andando_baixo_1 = pygame.image.load('imagens/personagem/frame2_38x74.png').convert_alpha()
        self.pistola_andando_baixo_2 = pygame.image.load('imagens/personagem/frame4_38x74.png').convert_alpha()

        self.pistola_parado_baixo_redimensionado = pygame.transform.scale(self.pistola_parado_baixo, self.tamanho_imagem)
        self.pistola_parado_direita_redimensionado = pygame.transform.scale(self.pistola_parado_direita, self.tamanho_imagem)
        self.pistola_parado_esquerda_redimensionado = pygame.transform.scale(self.pistola_parado_esquerda, self.tamanho_imagem)
        self.pistola_parado_cima_redimensionado = pygame.transform.scale(self.pistola_parado_cima , self.tamanho_imagem)
        self.retangulo = pygame.Rect(45, 45, 30, 30)

        self.pistola_andando_direita_1_redimensionado = pygame.transform.scale(self.pistola_andando_direita_1 , self.tamanho_imagem)
        self.pistola_andando_direita_2_redimensionado = pygame.transform.scale(self.pistola_andando_direita_2, self.tamanho_imagem)

        self.indice_imagem = 0
        self.tempo_anterior = pygame.time.get_ticks()
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

        self.angulos_animacao = [0, 1, 1, 1, 0, -1, -1, -1]
        self.alturas_animacao = [0, 1, 2, 1, 0, 1, 2, 1]
        self.lados_animacao = [0, 1, 1, 0, 0, -1, -1, 0]

        self.frames_pistola_andando_direita = [self.pistola_andando_direita_1_redimensionado, self.pistola_andando_direita_2_redimensionado]
        self.frames_pistola_andando_esquerda = [self.pistola_andando_esquerda_1, self.pistola_andando_esquerda_2]
        self.frames_pistola_andando_cima = [self.pistola_andando_cima_1, self.pistola_andando_cima_2]
        self.frames_pistola_andando_baixo = [self.pistola_andando_baixo_1, self.pistola_andando_baixo_2]

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
            velocidade_diagonal = ((self.velocidade ** 2) / 2) ** 0.5
            fator = velocidade_diagonal / self.velocidade

            movimento_x = movimento_x * fator
            movimento_y = movimento_y * fator

        posicao_anterior = self.retangulo.topleft
        novo_retangulo = self.retangulo.copy()
        novo_retangulo.x += movimento_x

        if self.mapa.pode_andar(novo_retangulo):
            self.retangulo.x = novo_retangulo.x

        novo_retangulo = self.retangulo.copy()
        novo_retangulo.y += movimento_y

        if self.mapa.pode_andar(novo_retangulo):
            self.retangulo.y = novo_retangulo.y

        self.esta_andando = (self.retangulo.topleft != posicao_anterior)

        tempo_atual = pygame.time.get_ticks()


        if self.esta_andando:
            if tempo_atual - self.ultimo_frame >= self.velocidade_animacao:
                self.indice_animacao = (self.indice_animacao + 1) % len(self.angulos_animacao)
                self.ultimo_frame = tempo_atual
        else:
            self.indice_animacao = 0
            self.ultimo_frame = tempo_atual

        if pygame.mouse.get_pressed()[0] and self.item_equipado == "taco":
            self.atacando = True
            self.area_ataque = self.retangulo.copy()
            self.area_ataque = self.area_ataque.inflate(40, 40)

        else:
            self.atacando = False
            self.area_ataque= None


    def desenhar(self):

        if self.esta_andando:
            imagem = self.frames_andando[self.direcao][self.indice_animacao]
        else:
            imagem = self.imagens_parado[self.direcao]

        if self.item_equipado == "Pistola" and self.direcao == "baixo":
            imagem = self.pistola_parado_baixo_redimensionado
            if self.esta_andando and self.item_equipado == "Pistola" and self.direcao == "baixo":
                imagem = self.frames_pistola_andando_baixo[self.indice_animacao % 2]

        elif self.item_equipado == "Pistola" and self.direcao == "direita":
            imagem = self.pistola_parado_direita_redimensionado
            if self.esta_andando and self.item_equipado == "Pistola" and self.direcao == "direita":
                imagem = self.frames_pistola_andando_direita[self.indice_animacao % 2]

        elif self.item_equipado == "Pistola" and self.direcao == "esquerda":
            imagem = self.pistola_parado_esquerda_redimensionado
            if self.esta_andando and self.item_equipado == "Pistola" and self.direcao == "esquerda":
                imagem = self.frames_pistola_andando_esquerda[self.indice_animacao % 2]

        elif self.item_equipado == "Pistola" and self.direcao == "cima":
            imagem = self.pistola_parado_cima_redimensionado
            if self.esta_andando and self.item_equipado == "Pistola" and self.direcao == "cima":
                imagem = self.frames_pistola_andando_cima[self.indice_animacao % 2]




        posicao_x = (
            self.retangulo.centerx
            - imagem.get_width() // 2
            - self.mapa.camera.camera_x
        )

        posicao_y = (
                self.retangulo.bottom
                - imagem.get_height()
                - self.mapa.camera.camera_y
        )

        if self.esta_andando:
            posicao_y -= self.alturas_animacao[self.indice_animacao]
            posicao_x += self.lados_animacao[self.indice_animacao]

        self.tela.blit(imagem, (posicao_x, posicao_y))

        retangulo_tela = self.retangulo.copy()

        retangulo_tela.x -= self.mapa.camera.camera_x
        retangulo_tela.y -= self.mapa.camera.camera_y