import pygame
import math
import os
from collections import deque


PASTA_JOGO = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

PASTA_SPRITES = os.path.join(
    PASTA_JOGO, "imagems", "personagem"
)


def achar_imagem(nome_arquivo):
    caminho = os.path.join(PASTA_SPRITES, nome_arquivo)

    if os.path.isfile(caminho):
        return caminho

    for pasta, _, arquivos in os.walk(PASTA_JOGO):
        for arquivo in arquivos:
            if arquivo.lower() == nome_arquivo.lower():
                return os.path.join(pasta, arquivo)

    raise FileNotFoundError(
        f"Nao encontrei '{nome_arquivo}' em "
        f"'{PASTA_JOGO}' ou nas suas subpastas."
    )


def extrair_frame(folha, coluna, linha, colunas, linhas):
    esquerda = coluna * folha.get_width() // colunas
    direita = (coluna + 1) * folha.get_width() // colunas

    topo = linha * folha.get_height() // linhas
    base = (linha + 1) * folha.get_height() // linhas

    return folha.subsurface(
        pygame.Rect(
            esquerda,
            topo,
            direita - esquerda,
            base - topo
        )
    ).copy()


def preparar_frames(frames, tamanho):
    caixas = [
        frame.get_bounding_rect(min_alpha=1)
        for frame in frames
    ]

    largura_maxima = max(
        (caixa.width for caixa in caixas),
        default=0
    )

    altura_maxima = max(
        (caixa.height for caixa in caixas),
        default=0
    )

    if largura_maxima == 0 or altura_maxima == 0:
        raise ValueError(
            "Os recortes dos sprites estao vazios. "
            "Confira a organizacao da folha."
        )

    escala = min(
        tamanho[0] / largura_maxima,
        tamanho[1] / altura_maxima
    )

    resultado = []

    for frame, caixa in zip(frames, caixas):
        superficie = pygame.Surface(
            tamanho, pygame.SRCALPHA
        )

        if caixa.width > 0 and caixa.height > 0:
            recorte = frame.subsurface(caixa).copy()

            largura = max(
                1, round(caixa.width * escala)
            )

            altura = max(
                1, round(caixa.height * escala)
            )

            recorte = pygame.transform.scale(
                recorte, (largura, altura)
            )

            posicao = recorte.get_rect(
                midbottom=(
                    tamanho[0] // 2,
                    tamanho[1]
                )
            )

            superficie.blit(recorte, posicao)

        resultado.append(superficie)

    return resultado


class Zumbi:
    TAMANHO_SPRITE = (64, 64)
    INTERVALO_ANIMACAO = 150

    _sprites_andando = None
    _sprites_parado = None

    @classmethod
    def carregar_sprites(cls):
        if cls._sprites_andando is not None:
            return

        folha_andando = pygame.image.load(
            achar_imagem("zumbi_andando.png")
        ).convert_alpha()

        folha_parado = pygame.image.load(
            achar_imagem("zumbi_parado.png")
        ).convert_alpha()

        linhas_andando = {
            "baixo": 0,
            "cima": 1,
            "esquerda": 2
        }

        posicoes_parado = {
            "baixo": (0, 0),
            "cima": (1, 0),
            "esquerda": (0, 1)
        }

        originais_andando = []
        direcoes_andando = []

        for direcao, linha in linhas_andando.items():
            for coluna in range(4):
                frame = extrair_frame(
                    folha_andando,
                    coluna,
                    linha,
                    4,
                    4
                )

                originais_andando.append(frame)
                direcoes_andando.append(direcao)

        originais_parado = []
        direcoes_parado = []

        for direcao, posicao in posicoes_parado.items():
            coluna, linha = posicao

            frame = extrair_frame(
                folha_parado,
                coluna,
                linha,
                2,
                2
            )

            originais_parado.append(frame)
            direcoes_parado.append(direcao)

        frames_andando = preparar_frames(
            originais_andando,
            cls.TAMANHO_SPRITE
        )

        frames_parado = preparar_frames(
            originais_parado,
            cls.TAMANHO_SPRITE
        )

        andando = {
            "baixo": [],
            "cima": [],
            "esquerda": []
        }

        parado = {}

        for direcao, frame in zip(
            direcoes_andando, frames_andando
        ):
            andando[direcao].append(frame)

        for direcao, frame in zip(
            direcoes_parado, frames_parado
        ):
            parado[direcao] = frame

        andando["direita"] = [
            pygame.transform.flip(frame, True, False)
            for frame in andando["esquerda"]
        ]

        parado["direita"] = pygame.transform.flip(
            parado["esquerda"], True, False
        )

        cls._sprites_andando = andando
        cls._sprites_parado = parado

    def __init__(self, tela, mapa, x, y):
        self.retangulo = pygame.Rect(x, y, 20, 20)
        self.vida = 100
        self.vivo = True
        self.dano = 10
        self.ultimo_ataque = 0

        self.tela = tela
        self.mapa = mapa
        self.velocidade_zumbi = 1
        self.seguir_personagem = None

        self.carregar_sprites()

        self.sprites_andando = self._sprites_andando
        self.sprites_parado = self._sprites_parado

        self.direcao = "baixo"
        self.andando = False
        self.frame_atual = 0
        self.ultimo_frame = pygame.time.get_ticks()
        self.imagem = self.sprites_parado[self.direcao]

        self.outros_zumbis = []

    def atualizar_animacao(self, dx, dy):
        agora = pygame.time.get_ticks()
        estava_andando = self.andando
        direcao_anterior = self.direcao

        self.andando = dx != 0 or dy != 0

        if not self.andando:
            self.frame_atual = 0
            self.ultimo_frame = agora
            self.imagem = self.sprites_parado[self.direcao]
            return

        if abs(dx) > abs(dy):
            self.direcao = (
                "direita" if dx > 0 else "esquerda"
            )

        elif abs(dy) > abs(dx):
            self.direcao = (
                "baixo" if dy > 0 else "cima"
            )

        elif self.direcao in ("esquerda", "direita"):
            self.direcao = (
                "direita" if dx > 0 else "esquerda"
            )

        else:
            self.direcao = (
                "baixo" if dy > 0 else "cima"
            )

        frames = self.sprites_andando[self.direcao]

        if (
            not estava_andando
            or self.direcao != direcao_anterior
        ):
            self.frame_atual = 0
            self.ultimo_frame = agora

        else:
            passos = (
                agora - self.ultimo_frame
            ) // self.INTERVALO_ANIMACAO

            if passos > 0:
                self.frame_atual = (
                    self.frame_atual + passos
                ) % len(frames)

                self.ultimo_frame += (
                    passos * self.INTERVALO_ANIMACAO
                )

        self.imagem = frames[self.frame_atual]

    def pode_mover(self, novo_retangulo):
        if not self.mapa.pode_andar(novo_retangulo):
            return False

        for outro in self.outros_zumbis:
            if outro is self or not outro.vivo:
                continue

            if novo_retangulo.colliderect(outro.retangulo):
                return False

        return True

    def desenhar(self):
        if not self.vivo:
            return

        posicao = self.imagem.get_rect(
            midbottom=(
                self.retangulo.centerx,
                self.retangulo.bottom
            )
        )

        self.tela.blit(self.imagem, posicao)

    def atualizar(self):
        if self.vida <= 0:
            self.vivo = False

        if not self.vivo:
            return

        if self.seguir_personagem is None:
            self.atualizar_animacao(0, 0)
            return

        if not self.seguir_personagem.vivo:
            self.atualizar_animacao(0, 0)
            return

        x_anterior = self.retangulo.x
        y_anterior = self.retangulo.y

        distancia = math.hypot(
            self.retangulo.x
            - self.seguir_personagem.retangulo.x,
            self.retangulo.y
            - self.seguir_personagem.retangulo.y
        )

        if distancia < 50:
            self.velocidade_zumbi = 0
            agora = pygame.time.get_ticks()

            if agora - self.ultimo_ataque >= 1000:
                personagem = self.seguir_personagem

                personagem.vida = max(
                    0, personagem.vida - self.dano
                )

                self.ultimo_ataque = agora

                if personagem.vida == 0:
                    personagem.vivo = False

        else:
            self.velocidade_zumbi = 1
            self.mover()

        dx = self.retangulo.x - x_anterior
        dy = self.retangulo.y - y_anterior

        self.atualizar_animacao(dx, dy)

    def mover(self):
        tamanho_tile = self.mapa.tamanho_tile

        coluna = self.retangulo.x // tamanho_tile
        linha = self.retangulo.y // tamanho_tile

        coluna_jogador = (
            self.seguir_personagem.retangulo.x
            // tamanho_tile
        )

        linha_jogador = (
            self.seguir_personagem.retangulo.y
            // tamanho_tile
        )

        inicio = (linha, coluna)
        destino = (linha_jogador, coluna_jogador)

        pais = {}
        fila = deque([inicio])
        visitados = {inicio}

        while fila:
            atual = fila.popleft()

            if atual == destino:
                break

            linha_atual, coluna_atual = atual

            vizinhos = [
                (linha_atual - 1, coluna_atual),
                (linha_atual + 1, coluna_atual),
                (linha_atual, coluna_atual - 1),
                (linha_atual, coluna_atual + 1)
            ]

            for vizinho in vizinhos:
                linha_vizinho, coluna_vizinho = vizinho

                if not (
                    0 <= linha_vizinho < len(self.mapa.mapa)
                ):
                    continue

                if not (
                    0 <= coluna_vizinho
                    < len(self.mapa.mapa[linha_vizinho])
                ):
                    continue

                if (
                    self.mapa.mapa[linha_vizinho][coluna_vizinho]
                    != 1
                ):
                    continue

                if vizinho in visitados:
                    continue

                visitados.add(vizinho)
                pais[vizinho] = atual
                fila.append(vizinho)

        if destino == inicio or destino not in pais:
            return

        proxima_celula = destino

        while pais[proxima_celula] != inicio:
            proxima_celula = pais[proxima_celula]

        linha_alvo, coluna_alvo = proxima_celula

        x_alvo = (
            coluna_alvo * tamanho_tile
            + tamanho_tile // 2
        )

        y_alvo = (
            linha_alvo * tamanho_tile
            + tamanho_tile // 2
        )

        movimento_x = 0
        movimento_y = 0

        if x_alvo > self.retangulo.centerx:
            movimento_x = 1
        elif x_alvo < self.retangulo.centerx:
            movimento_x = -1

        if y_alvo > self.retangulo.centery:
            movimento_y = 1
        elif y_alvo < self.retangulo.centery:
            movimento_y = -1

        novo_retangulo = self.retangulo.copy()
        novo_retangulo.x += (
            movimento_x * self.velocidade_zumbi
        )

        if self.pode_mover(novo_retangulo):
            self.retangulo.x = novo_retangulo.x

        novo_retangulo = self.retangulo.copy()
        novo_retangulo.y += (
            movimento_y * self.velocidade_zumbi
        )

        if self.mapa.pode_andar(novo_retangulo):
            self.retangulo.y = novo_retangulo.y

    def seguir(self, personagem):
        self.seguir_personagem = personagem