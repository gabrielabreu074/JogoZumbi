import pygame
from codigo.inventario import Inventario

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

        self.retangulo = pygame.Rect(45, 45, 30, 30)

        self.imagens = [
            pygame.image.load(
                "imagens/personagem/sprite_0.png"
            ).convert_alpha(),

            pygame.image.load(
                "imagens/personagem/sprite_1.png"
            ).convert_alpha(),

            pygame.image.load(
                "imagens/personagem/sprite_2.png"
            ).convert_alpha(),

            pygame.image.load(
                "imagens/personagem/sprite_3.png"
            ).convert_alpha()
        ]

        self.indice_imagem = 0

        self.tempo_anterior = pygame.time.get_ticks()

        self.tamanho_imagem = (60, 60)

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

        if teclas[pygame.K_a]:
            self.direcao = "esquerda"

        if teclas[pygame.K_d]:
            self.direcao = "direita"

        esta_andando = movimento_x != 0 or movimento_y != 0

        if movimento_x != 0 and movimento_y != 0:
            velocidade_diagonal = ((self.velocidade ** 2) / 2) ** 0.5
            fator = velocidade_diagonal / self.velocidade

            movimento_x = movimento_x * fator
            movimento_y = movimento_y * fator

        novo_retangulo = self.retangulo.copy()
        novo_retangulo.x += movimento_x

        if self.mapa.pode_andar(novo_retangulo):
            self.retangulo.x = novo_retangulo.x

        novo_retangulo = self.retangulo.copy()
        novo_retangulo.y += movimento_y

        if self.mapa.pode_andar(novo_retangulo):
            self.retangulo.y = novo_retangulo.y

        if esta_andando:

            tempo_atual = pygame.time.get_ticks()

            if tempo_atual - self.tempo_anterior >= 250:

                self.indice_imagem += 1

                if self.indice_imagem >= len(self.imagens):
                    self.indice_imagem = 0

                self.tempo_anterior = tempo_atual

        else:
            self.indice_imagem = 0
            self.tempo_anterior = pygame.time.get_ticks()

        if pygame.mouse.get_pressed()[0] and self.item_equipado == "taco":
            self.atacando = True
            self.area_ataque = self.retangulo.copy()
            self.area_ataque = self.area_ataque.inflate(40, 40)

        else:
            self.atacando = False
            self.area_ataque= None


    def desenhar(self):

        imagem = pygame.transform.scale(
            self.imagens[self.indice_imagem],
            self.tamanho_imagem
        )

        posicao_x = (
            self.retangulo.centerx
            - imagem.get_width() // 2
            - self.mapa.camera.camera_x
        )

        posicao_y = (
            self.retangulo.centery
            - imagem.get_height() // 2
            - self.mapa.camera.camera_y
        )

        teste = imagem

        if self.direcao == "direita":
            teste = pygame.transform.flip(imagem, True, False)

        self.tela.blit(
            teste,
            (posicao_x, posicao_y)
        )

        retangulo_tela = self.retangulo.copy()

        retangulo_tela.x -= self.mapa.camera.camera_x
        retangulo_tela.y -= self.mapa.camera.camera_y

        pygame.draw.rect(
            self.tela,
            (255, 0, 0),
            retangulo_tela,
            2
        )