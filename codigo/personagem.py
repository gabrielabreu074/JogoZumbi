import os
import pygame
from codigo.inventario import Inventario


def carregar_imagem(caminho):
    """Carrega uma imagem. Se o arquivo ainda não existir, retorna None
    (assim o jogo não quebra enquanto você não colocou todas as imagens)."""
    if os.path.exists(caminho):
        return pygame.image.load(caminho).convert_alpha()
    return None


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

        self.retangulo = pygame.Rect(45, 45, 45, 75)

        # ------------------------------------------------------------
        # IMAGENS PARADO (1 imagem para cada direção)
        # Troque os nomes dos arquivos pelos seus.
        # ------------------------------------------------------------
        self.imagens_parado = {
            "esquerda": carregar_imagem("imagens/personagem/zoio parado puto-2.png"),
            "frente": carregar_imagem("imagens/personagem/zoio parado puto-1.png"),
            "costas": carregar_imagem("imagens/personagem/zoio parado puto-4.png"),
            "direita": carregar_imagem("imagens/personagem/zoio parado puto-3.png"),
        }

        # ------------------------------------------------------------
        # IMAGENS DE MOVIMENTO (4 partes, 1 imagem para cada direção)
        # Troque os nomes dos arquivos pelos seus.
        # ------------------------------------------------------------
        self.imagens_movimento = {
            "esquerda": carregar_imagem("imagens/personagem/zoio andando puto-3.png"),
            "frente": carregar_imagem("imagens/personagem/zoio andando puto-1.png"),
            "costas": carregar_imagem("imagens/personagem/zoio andando puto-2.png"),
            "direita": carregar_imagem("imagens/personagem/zoio andando puto-4.png"),
        }

        self.esta_andando = False

        # ------------------------------------------------------------
        # ANIMAÇÃO DE ANDAR
        # Enquanto anda, alterna entre a imagem "parado" e "andando".
        # intervalo_animacao = tempo (em milissegundos) entre cada troca.
        # Diminua para trocar mais rápido, aumente para trocar mais devagar.
        # ------------------------------------------------------------
        self.intervalo_animacao = 150
        self.ultimo_troca_animacao = pygame.time.get_ticks()
        self.mostrar_imagem_andando = False

        # avisa no terminal qual imagem não foi encontrada
        for nome, img in {
            **{"parado-" + d: i for d, i in self.imagens_parado.items()},
            **{"andando-" + d: i for d, i in self.imagens_movimento.items()},
        }.items():
            if img is None:
                print("IMAGEM NÃO ENCONTRADA:", nome)

        self.tempo_anterior = pygame.time.get_ticks()

        self.tamanho_imagem = (45, 75)

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

        # direção (vertical primeiro; horizontal tem prioridade se pressionado)
        if teclas[pygame.K_w]:
            self.direcao = "costas"

        if teclas[pygame.K_s]:
            self.direcao = "frente"

        if teclas[pygame.K_a]:
            self.direcao = "esquerda"

        if teclas[pygame.K_d]:
            self.direcao = "direita"

        esta_andando = movimento_x != 0 or movimento_y != 0
        self.esta_andando = esta_andando

        # --------------------------------------------------------
        # Controle da animação: troca entre parado e andando
        # --------------------------------------------------------
        agora = pygame.time.get_ticks()

        if esta_andando:
            if agora - self.ultimo_troca_animacao >= self.intervalo_animacao:
                self.mostrar_imagem_andando = not self.mostrar_imagem_andando
                self.ultimo_troca_animacao = agora
        else:
            # ao parar, volta para a imagem parado e reinicia a animação
            self.mostrar_imagem_andando = False
            self.ultimo_troca_animacao = agora

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

        if not esta_andando:

            if pygame.mouse.get_pressed()[0]:
                self.atacando = True
                self.area_ataque = self.retangulo.copy()
                self.area_ataque = self.area_ataque.inflate(40, 40)

            else:
                self.atacando = False
                self.area_ataque = None

    def escolher_imagem(self):
        """Decide qual imagem desenhar.
        Parado: sempre a imagem parado.
        Andando: alterna entre a imagem andando e a parado."""

        if self.esta_andando and self.mostrar_imagem_andando:
            imagem = self.imagens_movimento[self.direcao]

            if imagem is not None:
                return imagem

        # parado (ou na metade "parado" da animação, ou sem imagem de movimento)
        return self.imagens_parado[self.direcao]

    def desenhar(self):

        imagem_original = self.escolher_imagem()

        if imagem_original is not None:

            imagem = pygame.transform.scale(
                imagem_original,
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

            self.tela.blit(
                imagem,
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